"""Router: fate roll (Vạn Sự Tùy Duyên)."""

from __future__ import annotations

import random
from typing import Any

from fastapi import APIRouter, Header, HTTPException

from database import get_db
from mascots import FATE_MESSAGES, MASCOTS, get_mascot
from models import DishSummary
from common import _decorate_dish, _fate_query

router = APIRouter()


@router.post("/api/fate/roll")
async def fate_roll(body: dict[str, Any], session_id: str | None = Header(default=None, alias="X-Session-Id")) -> dict[str, Any]:
    meal = body.get("meal")
    diet = body.get("diet")
    occasion = body.get("occasion")
    color = body.get("color")
    likely = body.get("likely", False)
    exclude_slug = body.get("exclude_slug")

    db = await get_db()
    try:
        # Look up user's selected mascot for this session
        user_mascot = None
        if session_id:
            mrow = await db.execute(
                "SELECT mascot_id FROM user_mascots WHERE session_id = ?", (session_id,)
            )
            msel = await mrow.fetchone()
            if msel:
                user_mascot = get_mascot(msel["mascot_id"])

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
                mascot_payload = user_mascot or random.choice(MASCOTS)
                return {
                    "roll": roll,
                    "dish": DishSummary(**_decorate_dish(chosen)).model_dump(),
                    "linh_vat": mascot_payload,
                    "message": random.choice(FATE_MESSAGES),
                    "likely_done": random.choice([True, False]),
                    "limit_reached": True,
                }
            await db.execute(
                "INSERT INTO fate_rolls (session_id, dish_id) VALUES (?, ?)",
                (session_id, chosen["id"]),
            )
            await db.commit()

        mascot_payload = (user_mascot or random.choice(MASCOTS)) if roll == 6 else None
        message = random.choice(FATE_MESSAGES) if roll == 6 else None
        return {
            "roll": roll,
            "dish": DishSummary(**_decorate_dish(chosen)).model_dump(),
            "linh_vat": mascot_payload,
            "message": message,
            "likely_done": False,
            "limit_reached": False,
        }
    finally:
        await db.close()