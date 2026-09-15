"""Router: group voting rooms."""

from __future__ import annotations

import json
import random
from typing import Any

from fastapi import APIRouter, Header, HTTPException

from database import get_db
from models import DishSummary, FinishResult, GroupJoinRequest, GroupRoomCreate, GroupVoteRequest
from common import _decorate_dish, _fate_query, _require_dish

router = APIRouter()


@router.post("/api/group-rooms", status_code=201)
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
    # ensure any dish that received a vote appears in the tally even if it
    # fell outside the random candidate window (max 30)
    extra_ids = [vid for vid in votes_by_dish if vid not in {p["id"] for p in dish_payloads}]
    if extra_ids:
        ph = ",".join("?" * len(extra_ids))
        erows = await db.execute(
            f"SELECT d.* FROM dishes d WHERE d.id IN ({ph})", extra_ids
        )
        for er in await erows.fetchall():
            dish_payloads.append(DishSummary(**_decorate_dish(dict(er))).model_dump())

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


@router.get("/api/group-rooms/{room_code}")
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


@router.post("/api/group-rooms/{room_code}/join")
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


@router.post("/api/group-rooms/{room_code}/votes")
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


@router.post("/api/group-rooms/{room_code}/finish")
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