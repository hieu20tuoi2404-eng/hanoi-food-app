"""Router: zodiac profile & recommendations."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from database import get_db
from models import (
    DishSummary,
    ZODIAC_HINTS,
    ZODIAC_SIGNS,
    ZodiacCreate,
    ZodiacDeleteResult,
    ZodiacProfile,
    ZodiacRecommendation,
    determine_zodiac,
)
from common import _decorate_dish

router = APIRouter()


@router.post("/api/zodiac/profile", status_code=201)
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


@router.delete("/api/zodiac/profile/{profile_id}")
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


@router.get("/api/zodiac/recommendation")
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