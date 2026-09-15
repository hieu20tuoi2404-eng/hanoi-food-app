"""FastAPI backend for An Gi Ha Noi? - Hanoi Food Discovery App."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from database import init_db
from routers import dishes, exploration, fate, groups, mascots, themes, zodiac
from seed import seed_data

app = FastAPI(title="An Gi Ha Noi? API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"


@app.on_event("startup")
async def startup() -> None:
    await init_db()
    await seed_data()


app.include_router(dishes.router)
app.include_router(zodiac.router)
app.include_router(fate.router)
app.include_router(groups.router)
app.include_router(themes.router)
app.include_router(mascots.router)
app.include_router(exploration.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException) -> JSONResponse:
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