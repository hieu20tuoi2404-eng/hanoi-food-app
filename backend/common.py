"""Shared helpers used by the API routers (dishes, fate, groups, etc.)."""

from __future__ import annotations

import json
from typing import Any

from fastapi import HTTPException

from database import get_db
from mascots import ZODIAC_THEMES
from models import THEMES, compute_rarity

# All themes: original 5 + 12 zodiac themes
ALL_THEMES: list[dict[str, Any]] = THEMES + ZODIAC_THEMES
ALL_THEME_MAP: dict[str, dict[str, Any]] = {t["id"]: t for t in ALL_THEMES}

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

# Legacy: favorites on cookies/session
favorite_store: dict[str, list[int]] = {}


def _json_list(raw: str | None) -> list[str]:
    if not raw:
        return []
    try:
        val = json.loads(raw)
        return val if isinstance(val, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def _parse_json_array(raw: str | None) -> list[str]:
    return _json_list(raw)


def _decorate_dish(d: dict[str, Any]) -> dict[str, Any]:
    """Add computed fields (is_demo bool, rarity) to a raw dish row."""
    d = dict(d)
    d["is_demo"] = bool(d["is_demo"])
    d["rarity"] = compute_rarity(d["avg_rating"])
    d["color_tags"] = _json_list(d.get("color_tags"))
    d["key_ingredients"] = _json_list(d.get("key_ingredients"))
    return d


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