"""Router: mascots & per-user mascot selection."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Header, HTTPException

from database import get_db
from mascots import MASCOTS, get_mascot

router = APIRouter()


@router.get("/api/mascots")
async def list_mascots() -> list[dict[str, Any]]:
    return MASCOTS


@router.get("/api/mascots/{mascot_id}")
async def get_mascot_endpoint(mascot_id: str) -> dict[str, Any]:
    m = get_mascot(mascot_id)
    if not m:
        raise HTTPException(status_code=404, detail="Không tìm thấy linh vật")
    return m


@router.post("/api/user/mascot")
async def set_user_mascot(
    body: dict[str, Any],
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    mascot_id = body.get("mascot_id")
    if mascot_id and not get_mascot(mascot_id):
        raise HTTPException(status_code=404, detail="Không tìm thấy linh vật")
    if not session_id:
        return {"mascot_id": mascot_id, "persisted": False}
    db = await get_db()
    try:
        if mascot_id:
            await db.execute(
                """INSERT INTO user_mascots (session_id, mascot_id, updated_at)
                   VALUES (?, ?, ?)
                   ON CONFLICT(session_id) DO UPDATE
                   SET mascot_id = excluded.mascot_id, updated_at = excluded.updated_at""",
                (session_id, mascot_id, datetime.now(timezone.utc).isoformat()),
            )
        else:
            await db.execute("DELETE FROM user_mascots WHERE session_id = ?", (session_id,))
        await db.commit()
        return {"mascot_id": mascot_id, "persisted": True}
    finally:
        await db.close()


@router.get("/api/user/mascot")
async def get_user_mascot(
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    if not session_id:
        return {"mascot_id": None}
    db = await get_db()
    try:
        row = await db.execute(
            "SELECT mascot_id, birthday_day, birthday_month FROM user_mascots WHERE session_id = ?",
            (session_id,),
        )
        sel = await row.fetchone()
        if sel:
            result: dict[str, Any] = {"mascot_id": sel["mascot_id"]}
            if sel["birthday_day"]:
                result["suggested_by_birthday"] = True
            return result
        return {"mascot_id": None}
    finally:
        await db.close()


@router.delete("/api/user/mascot")
async def delete_user_mascot(
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    if not session_id:
        return {"deleted": False}
    db = await get_db()
    try:
        await db.execute("DELETE FROM user_mascots WHERE session_id = ?", (session_id,))
        await db.commit()
        return {"deleted": True}
    finally:
        await db.close()