"""Router: exploration profile, collection, and legacy favorites."""

from __future__ import annotations

from uuid import uuid4
from typing import Any

from fastapi import APIRouter, Header

from database import get_db
from models import ACHIEVEMENTS, DishSummary, get_exploration_level, get_next_level
from common import _decorate_dish, _require_dish, favorite_store

router = APIRouter()


@router.get("/api/exploration")
async def exploration_profile(
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    if not session_id:
        session_id = str(uuid4())
    db = await get_db()
    try:
        vrow = await db.execute(
            "SELECT COUNT(*) AS c FROM user_views WHERE session_id = ?", (session_id,)
        )
        viewed_count = (await vrow.fetchone())["c"]

        rrow = await db.execute(
            "SELECT COUNT(*) AS c FROM user_reviews WHERE session_id = ?", (session_id,)
        )
        reviewed_count = (await rrow.fetchone())["c"]

        drow = await db.execute(
            """SELECT COUNT(DISTINCT r.district) AS c
               FROM user_views uv JOIN restaurants r ON r.dish_id = uv.dish_id
               WHERE uv.session_id = ?""",
            (session_id,),
        )
        districts = (await drow.fetchone())["c"]

        mrow = await db.execute(
            """SELECT COUNT(DISTINCT d.meal_type) AS c
               FROM user_views uv JOIN dishes d ON d.id = uv.dish_id
               WHERE uv.session_id = ?""",
            (session_id,),
        )
        meal_types = (await mrow.fetchone())["c"]

        # Max rarity tier among viewed dishes
        xrow = await db.execute(
            """SELECT MAX(CASE WHEN d.avg_rating >= 9.5 THEN 4
                              WHEN d.avg_rating >= 8.5 THEN 3
                              WHEN d.avg_rating >= 7.5 THEN 2
                              ELSE 1 END) AS tier
               FROM user_views uv JOIN dishes d ON d.id = uv.dish_id
               WHERE uv.session_id = ?""",
            (session_id,),
        )
        best_tier = (await xrow.fetchone())["tier"] or 0

        # Achievements
        achieved = []
        for ach in ACHIEVEMENTS:
            key = ach["key"]
            unlocked = False
            if key == "first_bite":
                unlocked = viewed_count >= 1
            elif key == "five_dishes":
                unlocked = viewed_count >= 5
            elif key == "ten_dishes":
                unlocked = viewed_count >= 10
            elif key == "all_dishes":
                unlocked = viewed_count >= 60
            elif key == "first_review":
                unlocked = reviewed_count >= 1
            elif key == "five_reviews":
                unlocked = reviewed_count >= 5
            elif key == "three_districts":
                unlocked = districts >= 3
            elif key == "all_meals":
                unlocked = meal_types >= 5
            elif key == "rare_finder":
                unlocked = best_tier >= 2
            elif key == "legendary_finder":
                unlocked = best_tier >= 4
            if unlocked:
                achieved.append({**ach, "unlocked": True})
        xp = sum(a["xp"] for a in achieved)
        level = get_exploration_level(xp)
        next_level = get_next_level(xp)

        return {
            "session_id": session_id,
            "level": level,
            "next_level": next_level,
            "xp": xp,
            "viewed_count": viewed_count,
            "reviewed_count": reviewed_count,
            "districts_explored": districts,
            "meal_types_explored": meal_types,
            "achievements": achieved,
            "unlocked_count": len(achieved),
            "total_achievements": len(ACHIEVEMENTS),
        }
    finally:
        await db.close()


@router.get("/api/collection")
async def collection(
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    """Card-collection view: all dishes w/ rarity + whether user has seen them."""
    if not session_id:
        session_id = f"anon-{uuid4()}"
    db = await get_db()
    try:
        rows = await db.execute("SELECT * FROM dishes ORDER BY avg_rating DESC, name")
        seen_ids = set()
        srow = await db.execute(
            "SELECT dish_id FROM user_views WHERE session_id = ?", (session_id,)
        )
        async for s in srow:
            seen_ids.add(s["dish_id"])
        cards = []
        async for r in rows:
            d = _decorate_dish(dict(r))
            cards.append({
                **DishSummary(**d).model_dump(),
                "collected": d["id"] in seen_ids,
            })
        return {"cards": cards, "total": len(cards), "collected": len(seen_ids)}
    finally:
        await db.close()


@router.get("/api/favorites")
async def get_favorites(
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    sid = session_id or "default"
    favs = favorite_store.get(sid, [])
    db = await get_db()
    try:
        out = []
        for fid in favs:
            row = await db.execute("SELECT * FROM dishes WHERE id = ?", (fid,))
            d = await row.fetchone()
            if d:
                out.append(DishSummary(**_decorate_dish(dict(d))).model_dump())
        return {"favorites": out}
    finally:
        await db.close()


@router.post("/api/favorites")
async def add_favorite(body: dict[str, Any], session_id: str | None = Header(default=None, alias="X-Session-Id")) -> dict[str, Any]:
    sid = session_id or "default"
    dish_id = body.get("dish_id")
    await _require_dish(dish_id)
    favs = favorite_store.setdefault(sid, [])
    if dish_id not in favs:
        favs.append(dish_id)
    return {"favorited": True, "dish_id": dish_id}


@router.delete("/api/favorites/{dish_id}")
async def remove_favorite(dish_id: int, session_id: str | None = Header(default=None, alias="X-Session-Id")) -> dict[str, Any]:
    sid = session_id or "default"
    favs = favorite_store.get(sid, [])
    if dish_id in favs:
        favs.remove(dish_id)
    return {"favorited": False, "dish_id": dish_id}