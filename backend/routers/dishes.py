"""Router: health, categories, dishes, fortunes, reviews, preferences."""

from __future__ import annotations

import random
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Query

from database import get_db
from models import (
    COLOR_OPTIONS,
    Category,
    DishDetail,
    DishSummary,
    HEALTHY_OPTIONS,
    MEAL_TYPES,
    OCCASION_OPTIONS,
    Recipe,
    Restaurant,
    Review,
    ReviewCreate,
)
from common import FORTUNE_MESSAGES, _build_filters, _decorate_dish, _json_list, _parse_json_array, _require_dish

router = APIRouter()


@router.get("/api/health")
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


@router.get("/api/categories")
async def categories() -> list[dict[str, Any]]:
    db = await get_db()
    try:
        rows = await db.execute("SELECT meal_type, COUNT(*) AS cnt FROM dishes GROUP BY meal_type")
        mapping = {
            "breakfast": "Bữa sáng",
            "lunch": "Bữa trưa",
            "dinner": "Bữa tối",
            "snack": "Ăn vặt",
            "drinking": "Món nhậu",
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


@router.get("/api/dishes")
async def list_dishes(
    meal: str | None = Query(None, description="breakfast|lunch|dinner|snack|drinking"),
    district: str | None = Query(None, description="Quận/Huyện"),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
    min_rating: float | None = Query(None, ge=1, le=10),
    search: str | None = Query(None, description="Từ khóa tìm kiếm"),
    diet: str | None = Query(None, description="healthy|light_oil|rich_oil|high_protein|vegetarian|spicy|light"),
    occasion: str | None = Query(None, description="Hoàn cảnh đi ăn (tag quán)"),
    color: str | None = Query(None, description="Màu món ăn"),
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

        fconds, fparams = _build_filters(meal=None, diet=diet, occasion=occasion, color=color)
        conds += fconds
        params += fparams

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


@router.get("/api/dishes/random")
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


@router.get("/api/fortunes")
async def lunch_fortune(
    meal: str | None = Query(None, description="breakfast|lunch|dinner|snack|drinking"),
    budget: int | None = Query(None, description="Tối đa ngân sách (avg_price)"),
) -> dict[str, Any]:
    """Quẻ trưa: a random dish + a fun fortune message (demo)."""
    db = await get_db()
    try:
        conds: list[str] = []
        params: list[Any] = []
        if meal:
            conds.append("meal_type = ?")
            params.append(meal)
        if budget is not None and budget > 0:
            conds.append("avg_price > 0 AND avg_price <= ?")
            params.append(budget)
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


@router.get("/api/dishes/by-color")
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


@router.get("/api/dishes/{slug}")
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


@router.get("/api/dishes/{dish_id}/restaurants")
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


@router.get("/api/dishes/{dish_id}/recipe")
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


@router.get("/api/dishes/{dish_id}/reviews")
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


@router.post("/api/dishes/{dish_id}/reviews", status_code=201)
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


@router.get("/api/preferences")
async def preferences() -> dict[str, Any]:
    """Filter options used by the advanced random picker."""
    return {
        "healthy_options": HEALTHY_OPTIONS,
        "occasion_options": OCCASION_OPTIONS,
        "color_options": COLOR_OPTIONS,
        "meal_types": MEAL_TYPES,
    }


@router.post("/api/dishes/random/advanced")
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