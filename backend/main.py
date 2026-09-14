"""FastAPI backend for An Gi Ha Noi? - Hanoi Food Discovery App."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from database import get_db, init_db
from models import Category, DishDetail, DishSummary, Recipe, Restaurant, Review, ReviewCreate, compute_rarity
from seed import seed_data

app = FastAPI(title="An Gi Ha Noi? API", version="1.1.0")

# Quẻ trưa fortune messages (demo, fun quotes only).
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

# Quẻ trưa tags auto-added to the suggestion (demo).

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"


def _decorate_dish(d: dict[str, Any]) -> dict[str, Any]:
    """Add computed fields (is_demo bool, rarity) to a raw dish row."""
    d = dict(d)
    d["is_demo"] = bool(d["is_demo"])
    d["rarity"] = compute_rarity(d["avg_rating"])
    return d


@app.on_event("startup")
async def startup() -> None:
    await init_db()
    await seed_data()


def _parse_json_array(raw: str | None) -> list[str]:
    if not raw:
        return []
    try:
        val = json.loads(raw)
        return val if isinstance(val, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


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
async def categories() -> list[Category]:
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
        return result
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
) -> list[DishSummary]:
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
        out: list[DishSummary] = []
        async for row in rows:
            d = _decorate_dish(dict(row))
            out.append(DishSummary(**d))
        return out
    finally:
        await db.close()


@app.get("/api/dishes/random")
async def random_dish(
    meal: str | None = Query(None),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
) -> DishSummary:
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
        return DishSummary(**_decorate_dish(dict(d)))
    finally:
        await db.close()


@app.get("/api/fortunes")
async def lunch_fortune(
    meal: str | None = Query(None, description="breakfast|lunch|dinner|snack"),
) -> dict[str, Any]:
    """Quẻ trưa: a random dish + a fun fortune message (demo)."""
    db = await get_db()
    try:
        import random

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


@app.get("/api/dishes/{slug}")
async def get_dish(slug: str) -> DishDetail:
    db = await get_db()
    try:
        row = await db.execute("SELECT * FROM dishes WHERE slug = ?", (slug,))
        d = await row.fetchone()
        if d is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")
        dish = _decorate_dish(dict(d))
        did = dish["id"]

        r_rows = await db.execute(
            "SELECT * FROM restaurants WHERE dish_id = ? ORDER BY name", (did,)
        )
        restaurants = []
        async for r in r_rows:
            rd = dict(r)
            rd["is_demo"] = bool(rd["is_demo"])
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

        return DishDetail(**dish, restaurants=restaurants, recipe=recipe, reviews=reviews)
    finally:
        await db.close()


@app.get("/api/dishes/{dish_id}/restaurants")
async def dish_restaurants(dish_id: int) -> list[Restaurant]:
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
            out.append(Restaurant(**rd))
        return out
    finally:
        await db.close()


@app.get("/api/dishes/{dish_id}/recipe")
async def dish_recipe(dish_id: int) -> Recipe:
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
        return Recipe(**rc)
    finally:
        await db.close()


@app.get("/api/dishes/{dish_id}/reviews")
async def dish_reviews(dish_id: int) -> list[Review]:
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
            out.append(Review(**rd))
        return out
    finally:
        await db.close()


@app.post("/api/dishes/{dish_id}/reviews", status_code=201)
async def create_review(dish_id: int, body: ReviewCreate) -> Review:
    await _require_dish(dish_id)
    db = await get_db()
    try:
        now = datetime.now(timezone.utc).isoformat()
        cur = await db.execute(
            """INSERT INTO reviews (dish_id, rating, comment, reviewer_name, is_demo, created_at)
               VALUES (?, ?, ?, ?, 0, ?)""",
            (dish_id, body.rating, body.comment, body.reviewer_name, now),
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
        )
    finally:
        await db.close()


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