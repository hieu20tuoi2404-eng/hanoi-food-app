"""Router: themes & theme selection."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Header, HTTPException

from database import get_db
from common import ALL_THEME_MAP, ALL_THEMES

router = APIRouter()


@router.get("/api/themes")
async def list_themes() -> list[dict[str, Any]]:
    return ALL_THEMES


@router.get("/api/themes/selection")
async def get_theme_selection(
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    if not session_id:
        return {"theme_id": ALL_THEMES[0]["id"]}
    db = await get_db()
    try:
        row = await db.execute(
            "SELECT theme_id FROM theme_selections WHERE session_id = ?", (session_id,)
        )
        sel = await row.fetchone()
        return {"theme_id": sel["theme_id"] if sel else ALL_THEMES[0]["id"]}
    finally:
        await db.close()


@router.get("/api/themes/{theme_id}")
async def get_theme(theme_id: str) -> dict[str, Any]:
    theme = ALL_THEME_MAP.get(theme_id)
    if not theme:
        raise HTTPException(status_code=404, detail="Không tìm thấy theme")
    return theme


@router.post("/api/themes/select")
async def select_theme(
    body: dict[str, str],
    session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict[str, Any]:
    theme_id = body.get("theme_id")
    if theme_id not in ALL_THEME_MAP:
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