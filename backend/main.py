"""FastAPI backend for An Gi Ha Noi? - Hanoi Food Discovery App."""

from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from database import get_db, init_db
from models import (
    ACHIEVEMENTS,
    Category,
    COLOR_OPTIONS,
    DishDetail,
    DishSummary,
    FinishResult,
    GroupJoinRequest,
    GroupRoomCreate,
    GroupVoteRequest,
    HEALTHY_OPTIONS,
    LINH_VAT_MESSAGES,
    LINH_VAT_NAMES,
    MEAL_TYPES,
    OCCASION_OPTIONS,
    Recipe,
    Restaurant,
    Review,
    ReviewCreate,
    THEMES,
    ZODIAC_HINTS,
    ZODIAC_SIGNS,
    ZodiacCreate,
    ZodiacDeleteResult,
    ZodiacProfile,
    ZodiacRecommendation,
    compute_rarity,
    determine_zodiac,
    get_exploration_level,
    get_next_level,
)
from seed import seed_data

app = FastAPI(title="An Gi Ha Noi? API", version="2.0.0")

FORTUNE_MESSAGES = [
    "Hôm nay trời đẹp, bụng đã kêu — đừng để dạ dày phải chờ!",
    "Người việt nói 'ăn trưa no để lo việc chiều' — tới bữa rồi đây.",
    "Một bữa Hà Nội ấm lòng hơn ngàn lời an ủi.",
    "Quẻ này bảo: ăn ngon thì nhớ địa chỉ, để mai còn quay lại.",
    "Bụng đang 'xôn xao' — hãy chiều nó một bữa thật tử tế.",
    "Hà Nội có nghìn quán, hôm nay may mắn sẽ gọi tên bạn.",
    "Ăn no rồi mới nói chuyện 'giảm cân từ thứ hai' nhé!",
    "Quán đông chứng tỏ ngon — hôm nay cũng nên thử vận may.",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"


def _json_list(raw: str | None) -> list[str]:
    if not raw:
        return []
    try:
        val = json.loads(raw)
        return val if isinstance(val, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def _decorate_dish(d: dict[str, Any]) -> dict[str, Any]:
    """Add computed fields (is_demo bool, rarity) to a raw dish row."""
    d = dict(d)
    d["is_demo"] = bool(d["is_demo"])
    d["rarity"] = compute_rarity(d["avg_rating"])
    d["color_tags"] = _json_list(d.get("color_tags"))
    d["key_ingredients"] = _json_list(d.get("key_ingredients"))
    return d


@app.on_event("startup")
async def startup() -> None:
    await init_db()
    await seed_data()


def _parse_json_array(raw: str | None) -> list[str]:
    return _json_list(raw)


async def _require_dish(dish_id: int) -> dict[str, Any]:
    db = await get_db()
    try:
        row = await db.execute("SELECT * FROM dishes WHERE id = ?", (dish_id,))
        d = await row.fetchone()
        if d is None:
            raise HTTPException(status_code=404, detail="Khong tim thay mon an")
        return dict(d)
    finally:
        await db.close()


@app.get("/api/health")
async def health() -> dict[str, Any]:
    db = await get_db()
    try:
        row = await db.execute("SELECT COUNT(*) AS cnt FROM dishes")
        count = (await row.fetchone())["cnt"]
    finally:
        await db.close()
    return {
        "status": "healthy",
        "dishes_count": count,
        "demo_mode": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/categories")
async def categories() -> list[dict[str, Any]]:
    db = await get_db()
    try:
        rows = await db.execute("SELECT meal_type, COUNT(*) AS cnt FROM dishes GROUP BY meal_type")
        mapping = {
            "breakfast": "Bữa sáng",
            "lunch": "Bữa trưa",
            "dinner": "Bữa tối",
            "snack": "Ăn vặt",
        }
        result = []
        async for row in rows:
            d = dict(row)
            result.append(
                Category(
                    name=mapping.get(d["meal_type"], d["meal_type"]),
                    slug=d["meal_type"],
                    count=d["cnt"],
                )
            )
        return [c.model_dump() for c in result]
    finally:
        await db.close()


@app.get("/api/dishes")
async def list_dishes(
    meal: str | None = Query(None, description="breakfast|lunch|dinner|snack"),
    district: str | None = Query(None, description="Quận/Huyện"),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
    min_rating: float | None = Query(None, ge=1, le=10),
    search: str | None = Query(None, description="Từ khóa tìm kiếm"),
) -> list[dict[str, Any]]:
    db = await get_db()
    try:
        conds: list[str] = []
        params: list[Any] = []

        if meal:
            conds.append("d.meal_type = ?")
            params.append(meal)
        if search:
            conds.append("(d.name LIKE ? OR d.description LIKE ?)")
            params += [f"%{search}%", f"%{search}%"]
        if min_price is not None:
            conds.append("d.avg_price >= ?")
            params.append(min_price)
        if max_price is not None:
            conds.append("d.avg_price <= ?")
            params.append(max_price)
        if min_rating is not None:
            conds.append("d.avg_rating >= ?")
            params.append(min_rating)
        if district:
            conds.append(
                "EXISTS (SELECT 1 FROM restaurants r WHERE r.dish_id = d.id AND r.district = ?)"
            )
            params.append(district)

        where = " AND ".join(conds) if conds else "1=1"
        query = f"SELECT d.* FROM dishes d WHERE {where} ORDER BY d.avg_rating DESC, d.name"
        rows = await db.execute(query, params)
        out: list[dict[str, Any]] = []
        async for row in rows:
            d = _decorate_dish(dict(row))
            out.append(DishSummary(**d).model_dump())
        return out
    finally:
        await db.close()


@app.get("/api/dishes/random")
async def random_dish(
    meal: str | None = Query(None),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
) -> dict[str, Any]:
    db = await get_db()
    try:
        conds: list[str] = []
        params: list[Any] = []
        if meal:
            conds.append("meal_type = ?")
            params.append(meal)
        if min_price is not None:
            conds.append("avg_price >= ?")
            params.append(min_price)
        if max_price is not None:
            conds.append("avg_price <= ?")
            params.append(max_price)
        where = " AND ".join(conds) if conds else "1=1"
        row = await db.execute(
            f"SELECT * FROM dishes WHERE {where} ORDER BY RANDOM() LIMIT 1", params
        )
        d = await row.fetchone()
        if d is None:
            raise HTTPException(status_code=404, detail="Không có món ăn phù hợp")
        return DishSummary(**_decorate_dish(dict(d))).model_dump()
    finally:
        await db.close()


@app.get("/api/fortunes")
async def lunch_fortune(
    meal: str | None = Query(None, description="breakfast|lunch|dinner|snack"),
) -> dict[str, Any]:
    """Quẻ trưa: a random dish + a fun fortune message (demo)."""
    db = await get_db()
    try:
        conds: list[str] = []
        params: list[Any] = []
        if meal:
            conds.append("meal_type = ?")
            params.append(meal)
        where = " AND ".join(conds) if conds else "1=1"
        row = await db.execute(
            f"SELECT * FROM dishes WHERE {where} ORDER BY RANDOM() LIMIT 1", params
        )
        d = await row.fetchone()
        if d is None:
            raise HTTPException(status_code=404, detail="Không có món ăn phù hợp")
        dish = DishSummary(**_decorate_dish(dict(d)))
        message = random.choice(FORTUNE_MESSAGES)
        return {
            "dish": dish.model_dump(),
            "fortune": message,
            "luck": random.choice(["may_mắn", "bình_thường", "đặc_biệt"]),
        }
    finally:
        await db.close()


@app.get("/api/dishes/by-color")
async def dishes_by_color(
    color: str = Query(..., description="Màu sắc"),
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> list[dict[str, Any]]:
    db = await get_db()
    try:
        rows = await db.execute(
            "SELECT * FROM dishes WHERE dominant_color = ? OR color_tags LIKE ?",
            (color, f"%{color}%"),
        )
        out = []
        async for r in rows:
            d = _decorate_dish(dict(r))
            out.append(DishSummary(**d).model_dump())
        return out
    finally:
        await db.close()


@app.get("/api/dishes/{slug}")
async def get_dish(
    slug: str,
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    db = await get_db()
    try:
        row = await db.execute("SELECT * FROM dishes WHERE slug = ?", (slug,))
        d = await row.fetchone()
        if d is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")
        dish = _decorate_dish(dict(d))
        did = dish["id"]

        # Record view for exploration tracking
        if session_id:
            await db.execute(
                """INSERT OR IGNORE INTO user_views (session_id, dish_id) VALUES (?, ?)""",
                (session_id, did),
            )
            await db.commit()

        r_rows = await db.execute(
            "SELECT * FROM restaurants WHERE dish_id = ? ORDER BY name", (did,)
        )
        restaurants = []
        async for r in r_rows:
            rd = dict(r)
            rd["is_demo"] = bool(rd["is_demo"])
            rd["occasion_tags"] = _json_list(rd.get("occasion_tags"))
            restaurants.append(Restaurant(**rd))

        rec_row = await db.execute("SELECT * FROM recipes WHERE dish_id = ?", (did,))
        rec = await rec_row.fetchone()
        recipe = None
        if rec:
            rc = dict(rec)
            rc["ingredients"] = _parse_json_array(rc["ingredients"])
            rc["steps"] = _parse_json_array(rc["steps"])
            recipe = Recipe(**rc)

        rv_rows = await db.execute(
            "SELECT * FROM reviews WHERE dish_id = ? ORDER BY created_at DESC", (did,)
        )
        reviews = []
        async for rv in rv_rows:
            rv_d = dict(rv)
            rv_d["is_demo"] = bool(rv_d["is_demo"])
            reviews.append(Review(**rv_d))

        result = DishDetail(**dish, restaurants=restaurants, recipe=recipe, reviews=reviews)
        return result.model_dump()
    finally:
        await db.close()


@app.get("/api/dishes/{dish_id}/restaurants")
async def dish_restaurants(dish_id: int) -> list[dict[str, Any]]:
    await _require_dish(dish_id)
    db = await get_db()
    try:
        rows = await db.execute(
            "SELECT * FROM restaurants WHERE dish_id = ? ORDER BY name", (dish_id,)
        )
        out = []
        async for r in rows:
            rd = dict(r)
            rd["is_demo"] = bool(rd["is_demo"])
            rd["occasion_tags"] = _json_list(rd.get("occasion_tags"))
            out.append(Restaurant(**rd).model_dump())
        return out
    finally:
        await db.close()


@app.get("/api/dishes/{dish_id}/recipe")
async def dish_recipe(dish_id: int) -> dict[str, Any]:
    await _require_dish(dish_id)
    db = await get_db()
    try:
        row = await db.execute("SELECT * FROM recipes WHERE dish_id = ?", (dish_id,))
        rec = await row.fetchone()
        if rec is None:
            raise HTTPException(status_code=404, detail="Chưa có công thức cho món này")
        rc = dict(rec)
        rc["ingredients"] = _parse_json_array(rc["ingredients"])
        rc["steps"] = _parse_json_array(rc["steps"])
        return Recipe(**rc).model_dump()
    finally:
        await db.close()


@app.get("/api/dishes/{dish_id}/reviews")
async def dish_reviews(dish_id: int) -> list[dict[str, Any]]:
    await _require_dish(dish_id)
    db = await get_db()
    try:
        rows = await db.execute(
            "SELECT * FROM reviews WHERE dish_id = ? ORDER BY created_at DESC", (dish_id,)
        )
        out = []
        async for r in rows:
            rd = dict(r)
            rd["is_demo"] = bool(rd["is_demo"])
            out.append(Review(**rd).model_dump())
        return out
    finally:
        await db.close()


@app.post("/api/dishes/{dish_id}/reviews", status_code=201)
async def create_review(
    dish_id: int,
    body: ReviewCreate,
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    await _require_dish(dish_id)
    db = await get_db()
    try:
        now = datetime.now(timezone.utc).isoformat()
        cur = await db.execute(
            """INSERT INTO reviews (dish_id, rating, comment, reviewer_name, is_demo, created_at)
               VALUES (?, ?, ?, ?, 0, ?)""",
            (dish_id, body.rating, body.comment, body.reviewer_name, now),
        )
        if session_id:
            await db.execute(
                """INSERT OR IGNORE INTO user_reviews (session_id, dish_id) VALUES (?, ?)""",
                (session_id, dish_id),
            )
        await db.commit()
        return Review(
            id=cur.lastrowid,
            dish_id=dish_id,
            rating=body.rating,
            comment=body.comment,
            reviewer_name=body.reviewer_name,
            is_demo=False,
            created_at=now,
        ).model_dump()
    finally:
        await db.close()


# ============================================================
# 2.0: Preferences / advanced random / by-color / zodiac / fate / groups / themes / exploration
# ============================================================

@app.get("/api/preferences")
async def preferences() -> dict[str, Any]:
    """Filter options used by the advanced random picker."""
    return {
        "healthy_options": HEALTHY_OPTIONS,
        "occasion_options": OCCASION_OPTIONS,
        "color_options": COLOR_OPTIONS,
        "meal_types": MEAL_TYPES,
    }


def _build_filters(
    meal: str | None,
    diet: str | None,
    occasion: str | None,
    color: str | None,
) -> tuple[list[str], list[Any]]:
    """Return (SQL fragments, params) for diet/occasion/color filters. Uses d. alias."""
    conds: list[str] = []
    params: list[Any] = []
    if meal:
        conds.append("d.meal_type = ?")
        params.append(meal)
    if diet:
        diet_map = {
            "healthy": "d.healthy_score >= 6",
            "light_oil": "(d.oil_level = 'low' OR d.oil_level = 'medium')",
            "rich_oil": "d.oil_level = 'high'",
            "high_protein": "d.protein_level = 'high'",
            "vegetarian": "d.vegetarian = 1",
            "spicy": "(d.spicy_level = 'medium' OR d.spicy_level = 'high')",
            "light": "(d.meal_type = 'snack' OR d.meal_type = 'breakfast')",
        }
        if diet in diet_map:
            conds.append(diet_map[diet])
    if occasion:
        conds.append(
            "EXISTS (SELECT 1 FROM restaurants r WHERE r.dish_id = d.id AND r.occasion_tags LIKE ?)"
        )
        params.append(f"%{occasion}%")
    if color:
        conds.append("(d.dominant_color = ? OR d.color_tags LIKE ?)")
        params += [color, f"%{color}%"]
    return conds, params


@app.post("/api/dishes/random/advanced")
async def random_advanced(body: dict[str, Any]) -> dict[str, Any]:
    db = await get_db()
    try:
        meal = body.get("meal")
        diet = body.get("diet")
        occasion = body.get("occasion")
        color = body.get("color")
        min_price = body.get("min_price")
        max_price = body.get("max_price")
        budget = body.get("budget")
        exclude_slug = body.get("exclude_slug")

        conds: list[str] = []
        params: list[Any] = []
        if min_price is not None:
            conds.append("d.avg_price >= ?")
            params.append(min_price)
        if max_price is not None:
            conds.append("d.avg_price <= ?")
            params.append(max_price)
        if budget is not None and budget > 0:
            conds.append("d.avg_price <= ?")
            params.append(budget)
        if exclude_slug:
            conds.append("d.slug != ?")
            params.append(exclude_slug)

        fconds, fparams = _build_filters(meal, diet, occasion, color)
        conds.extend(fconds)
        params.extend(fparams)

        where = " AND ".join(conds) if conds else "1=1"
        row = await db.execute(
            f"SELECT d.* FROM dishes d WHERE {where} ORDER BY RANDOM() LIMIT 1", params
        )
        d = await row.fetchone()
        if d is None:
            raise HTTPException(status_code=404, detail="Không có món ăn phù hợp với bộ lọc này")
        dish = _decorate_dish(dict(d))
        return {"dish": DishSummary(**dish).model_dump(), "matched": True}
    finally:
        await db.close()


# ----- Zodiac -----

@app.post("/api/zodiac/profile", status_code=201)
async def create_zodiac_profile(body: ZodiacCreate) -> dict[str, Any]:
    if body.month in (2,) and body.day > 29:
        raise HTTPException(status_code=422, detail="Ngày/ tháng không hợp lệ")
    sign_key = determine_zodiac(body.day, body.month)
    sign = next((s for s in ZODIAC_SIGNS if s["key"] == sign_key), None)
    db = await get_db()
    try:
        year = body.year if body.consent_save else None
        cur = await db.execute(
            """INSERT INTO zodiac_profiles (birth_day, birth_month, birth_year, consent_save)
               VALUES (?, ?, ?, ?)""",
            (body.day, body.month, year, 1 if body.consent_save else 0),
        )
        await db.commit()
        return ZodiacProfile(
            id=cur.lastrowid,
            day=body.day,
            month=body.month,
            year=year,
            consent_save=body.consent_save,
            sign_key=sign["key"] if sign else "",
            sign_name=sign["name"] if sign else "",
            sign_emoji=sign["emoji"] if sign else "",
        ).model_dump()
    finally:
        await db.close()


@app.delete("/api/zodiac/profile/{profile_id}")
async def delete_zodiac_profile(profile_id: int) -> dict[str, Any]:
    db = await get_db()
    try:
        cur = await db.execute("DELETE FROM zodiac_profiles WHERE id = ?", (profile_id,))
        await db.commit()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ")
        return ZodiacDeleteResult().model_dump()
    finally:
        await db.close()


@app.get("/api/zodiac/recommendation")
async def zodiac_recommendation(day: int, month: int) -> dict[str, Any]:
    sign_key = determine_zodiac(day, month)
    sign = next((s for s in ZODIAC_SIGNS if s["key"] == sign_key), None)
    if sign is None:
        raise HTTPException(status_code=404, detail="Không xác định được cung")
    flavour = ZODIAC_HINTS.get(sign_key, {}).get("flavour", "")
    tags = ZODIAC_HINTS.get(sign_key, {}).get("hint_tags", [])
    db = await get_db()
    try:
        conds = []
        params = []
        if "spicy" in tags:
            conds.append("(spicy_level = 'medium' OR spicy_level = 'high')")
        if "light_oil" in tags:
            conds.append("(oil_level = 'low' OR oil_level = 'medium')")
        if "high_protein" in tags:
            conds.append("protein_level = 'high'")
        if "high_price" in tags:
            conds.append("avg_price >= 80000")
        where = " AND ".join(conds) if conds else "1=1"
        row = await db.execute(
            f"SELECT * FROM dishes WHERE {where} ORDER BY RANDOM() LIMIT 1", params
        )
        d = await row.fetchone()
        dish = None
        if d is not None:
            dish = DishSummary(**_decorate_dish(dict(d))).model_dump()
        return ZodiacRecommendation(
            sign=sign,
            flavour=flavour,
            dish=dish,
        ).model_dump()
    finally:
        await db.close()


# ----- Fate (Van Su Tuy Duyen) -----

async def _fate_query(
    meal, diet, occasion, color, exclude_slug, weighted: bool
) -> list[dict[str, Any]]:
    """Return dishes matching filters, optionally weighted toward higher ratings."""
    db = await get_db()
    try:
        conds, params = _build_filters(meal, diet, occasion, color)
        if exclude_slug:
            conds.append("d.slug != ?")
            params.append(exclude_slug)
        where = " AND ".join(conds) if conds else "1=1"
        order = "d.avg_rating DESC, d.avg_price DESC" if weighted else "RANDOM()"
        rows = await db.execute(
            f"SELECT d.* FROM dishes d WHERE {where} ORDER BY {order} LIMIT 30", params
        )
        return [dict(r) for r in await rows.fetchall()]
    finally:
        await db.close()


@app.post("/api/fate/roll")
async def fate_roll(body: dict[str, Any], session_id: str | None = Header(default=None, alias="X-Session-Id")) -> dict[str, Any]:
    meal = body.get("meal")
    diet = body.get("diet")
    occasion = body.get("occasion")
    color = body.get("color")
    likely = body.get("likely", False)
    exclude_slug = body.get("exclude_slug")

    db = await get_db()
    try:
        roll = random.randint(1, 6)
        candidates = await _fate_query(meal, diet, occasion, color, exclude_slug, weighted=likely)
        if not candidates:
            raise HTTPException(status_code=404, detail="Không có món ăn phù hợp")

        chosen = None
        if likely:
            # Weighted: roll picks from the top-ranked slice.
            idx = min(roll - 1, len(candidates) - 1)
            chosen = candidates[idx]
        else:
            chosen = random.choice(candidates)

        # Rule: at most 3 rolls per session; after that we show a linh vật and ask to pick.
        if session_id:
            c = await db.execute("SELECT COUNT(*) AS c FROM fate_rolls WHERE session_id = ?", (session_id,))
            count = (await c.fetchone())["c"]
            if count >= 3:
                return {
                    "roll": roll,
                    "dish": DishSummary(**_decorate_dish(chosen)).model_dump(),
                    "linh_vat": random.choice(LINH_VAT_NAMES),
                    "message": random.choice(LINH_VAT_MESSAGES),
                    "likely_done": random.choice([True, False]),
                    "limit_reached": True,
                }
            await db.execute(
                "INSERT INTO fate_rolls (session_id, dish_id) VALUES (?, ?)",
                (session_id, chosen["id"]),
            )
            await db.commit()

        linh_vat = random.choice(LINH_VAT_NAMES) if roll == 6 else None
        message = random.choice(LINH_VAT_MESSAGES) if roll == 6 else None
        return {
            "roll": roll,
            "dish": DishSummary(**_decorate_dish(chosen)).model_dump(),
            "linh_vat": linh_vat,
            "message": message,
            "likely_done": False,
            "limit_reached": False,
        }
    finally:
        await db.close()


# ----- Group voting -----

@app.post("/api/group-rooms", status_code=201)
async def create_group_room(
    body: GroupRoomCreate,
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    room_code = "".join(random.choices("ABCDEFGHJKMNPQRSTUVWXYZ23456789", k=6))
    db = await get_db()
    try:
        cur = await db.execute(
            """INSERT INTO group_rooms (room_code, host_name, config, ends_at, status)
               VALUES (?, ?, ?, ?, 'open')""",
            (room_code, body.host_name, json.dumps(body.config), body.ends_at),
        )
        await db.commit()
        return await _room_payload(cur.lastrowid, db)
    finally:
        await db.close()


async def _room_payload(room_id: int, db) -> dict[str, Any]:
    row = await db.execute("SELECT * FROM group_rooms WHERE id = ?", (room_id,))
    room = await row.fetchone()
    if room is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy phòng")
    try:
        config = json.loads(room["config"]) if isinstance(room["config"], str) else room["config"] or {}
    except json.JSONDecodeError:
        config = {}
    # candidate dishes
    candidates = await _fate_query(
        meal=config.get("meal"), diet=config.get("diet"),
        occasion=config.get("occasion"), color=config.get("color"),
        exclude_slug=None, weighted=False,
    )
    dish_payloads = [DishSummary(**_decorate_dish(d)).model_dump() for d in candidates]
    votes_by_dish = {}
    voters_by_dish = {}
    vrows = await db.execute(
        """SELECT gv.dish_id, gv.voter_name FROM group_votes gv WHERE gv.room_id = ?""",
        (room_id,),
    )
    async for v in vrows:
        votes_by_dish[v["dish_id"]] = votes_by_dish.get(v["dish_id"], 0) + 1
        voters_by_dish.setdefault(v["dish_id"], []).append(v["voter_name"])

    # tally
    tally = []
    for d in dish_payloads:
        tally.append({
            "dish": d,
            "votes": votes_by_dish.get(d["id"], 0),
            "voters": voters_by_dish.get(d["id"], []),
        })
    tally.sort(key=lambda x: x["votes"], reverse=True)
    winner = tally[0] if tally and tally[0]["votes"] > 0 else None
    top_votes = winner["votes"] if winner else 0
    tied = [t for t in tally if t["votes"] == top_votes and top_votes > 0]
    total_votes = sum(t["votes"] for t in tally)

    return {
        "room_code": room["room_code"],
        "host_name": room["host_name"],
        "config": config,
        "ends_at": room["ends_at"],
        "status": room["status"],
        "dishes": dish_payloads,
        "vote_tally": {
            "winner": winner["dish"] if winner else None,
            "tied": [t["dish"] for t in tied],
            "tally": tally,
            "total_votes": total_votes,
            "status": room["status"],
        },
    }


@app.get("/api/group-rooms/{room_code}")
async def get_group_room(room_code: str) -> dict[str, Any]:
    db = await get_db()
    try:
        row = await db.execute("SELECT * FROM group_rooms WHERE room_code = ?", (room_code,))
        room = await row.fetchone()
        if room is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy phòng")
        return await _room_payload(room["id"], db)
    finally:
        await db.close()


@app.post("/api/group-rooms/{room_code}/join")
async def join_group_room(room_code: str, body: GroupJoinRequest) -> dict[str, Any]:
    db = await get_db()
    try:
        row = await db.execute("SELECT * FROM group_rooms WHERE room_code = ?", (room_code,))
        room = await row.fetchone()
        if room is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy phòng")
        if room["status"] != "open":
            raise HTTPException(status_code=400, detail="Phòng đã kết thúc")
        return {"room_code": room["room_code"], "joined": True, "voter_name": body.voter_name}
    finally:
        await db.close()


@app.post("/api/group-rooms/{room_code}/votes")
async def cast_group_vote(room_code: str, body: GroupVoteRequest) -> dict[str, Any]:
    db = await get_db()
    try:
        row = await db.execute("SELECT * FROM group_rooms WHERE room_code = ?", (room_code,))
        room = await row.fetchone()
        if room is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy phòng")
        if room["status"] != "open":
            raise HTTPException(status_code=400, detail="Phòng đã kết thúc")
        await _require_dish(body.dish_id)
        try:
            await db.execute(
                """INSERT INTO group_votes (room_id, dish_id, voter_name) VALUES (?, ?, ?)""",
                (room["id"], body.dish_id, body.voter_name),
            )
            await db.commit()
        except Exception:
            raise HTTPException(status_code=409, detail="Người này đã bỏ phiếu")
        return {"voted": True, "voter_name": body.voter_name, "dish_id": body.dish_id}
    finally:
        await db.close()


@app.post("/api/group-rooms/{room_code}/finish")
async def finish_group_room(room_code: str) -> dict[str, Any]:
    db = await get_db()
    try:
        row = await db.execute("SELECT * FROM group_rooms WHERE room_code = ?", (room_code,))
        room = await row.fetchone()
        if room is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy phòng")
        await db.execute(
            "UPDATE group_rooms SET status = 'finished' WHERE id = ?", (room["id"],)
        )
        await db.commit()
        payload = await _room_payload(room["id"], db)
        tally = payload["vote_tally"]
        winner = tally["winner"]
        tied = tally["tied"]
        if tied and len(tied) > 1 and winner is None:
            winner = random.choice(tied)
            tied = [d for d in tied if d["id"] != winner["id"]]
        return FinishResult(
            status="finished",
            winner=winner,
            tied=tied,
            total_votes=tally["total_votes"],
        ).model_dump()
    finally:
        await db.close()


# ----- Themes -----

@app.get("/api/themes")
async def list_themes() -> list[dict[str, Any]]:
    return THEMES


def _resolve_theme_static():
    return THEMES


@app.post("/api/themes/select")
async def select_theme(
    body: dict[str, str],
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    theme_id = body.get("theme_id")
    if not any(t["id"] == theme_id for t in THEMES):
        raise HTTPException(status_code=404, detail="Không tìm thấy theme")
    if not session_id:
        return {"theme_id": theme_id, "persisted": False}
    db = await get_db()
    try:
        await db.execute(
            """INSERT INTO theme_selections (session_id, theme_id, updated_at) VALUES (?, ?, ?)
               ON CONFLICT(session_id) DO UPDATE SET theme_id = excluded.theme_id, updated_at = excluded.updated_at""",
            (session_id, theme_id, datetime.now(timezone.utc).isoformat()),
        )
        await db.commit()
        return {"theme_id": theme_id, "persisted": True}
    finally:
        await db.close()


@app.get("/api/themes/selection")
async def get_theme_selection(
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    if not session_id:
        return {"theme_id": THEMES[0]["id"]}
    db = await get_db()
    try:
        row = await db.execute(
            "SELECT theme_id FROM theme_selections WHERE session_id = ?", (session_id,)
        )
        sel = await row.fetchone()
        return {"theme_id": sel["theme_id"] if sel else THEMES[0]["id"]}
    finally:
        await db.close()


# ----- Exploration -----

@app.get("/api/exploration")
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
                unlocked = viewed_count >= 30
            elif key == "first_review":
                unlocked = reviewed_count >= 1
            elif key == "five_reviews":
                unlocked = reviewed_count >= 5
            elif key == "three_districts":
                unlocked = districts >= 3
            elif key == "all_meals":
                unlocked = meal_types >= 4
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


@app.get("/api/collection")
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


# Legacy: favorites on cookies/session
favorite_store: dict[str, list[int]] = {}


@app.get("/api/favorites")
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


@app.post("/api/favorites")
async def add_favorite(body: dict[str, Any], session_id: str | None = Header(default=None, alias="X-Session-Id")) -> dict[str, Any]:
    sid = session_id or "default"
    dish_id = body.get("dish_id")
    await _require_dish(dish_id)
    favs = favorite_store.setdefault(sid, [])
    if dish_id not in favs:
        favs.append(dish_id)
    return {"favorited": True, "dish_id": dish_id}


@app.delete("/api/favorites/{dish_id}")
async def remove_favorite(dish_id: int, session_id: str | None = Header(default=None, alias="X-Session-Id")) -> dict[str, Any]:
    sid = session_id or "default"
    favs = favorite_store.get(sid, [])
    if dish_id in favs:
        favs.remove(dish_id)
    return {"favorited": False, "dish_id": dish_id}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Any, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail, "code": str(exc.status_code)})


# Serve the built frontend (SPA) after all /api routes.
if FRONTEND_DIST.is_dir():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}", response_class=FileResponse, include_in_schema=False)
    async def spa(full_path: str) -> FileResponse:
        candidate = (FRONTEND_DIST / full_path).resolve()
        if (
            full_path
            and candidate.is_file()
            and candidate.is_relative_to(FRONTEND_DIST.resolve())
        ):
            return FileResponse(candidate)
        return FileResponse(FRONTEND_DIST / "index.html")