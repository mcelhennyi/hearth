"""FastAPI scaffold for the built-in hearth-users plugin."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

APP_ROOT = Path(__file__).resolve().parents[1]
DIST_INDEX = APP_ROOT / "web" / "dist" / "index.html"
SOURCE_INDEX = APP_ROOT / "web" / "index.html"


def _placeholder_html() -> str:
    if DIST_INDEX.exists():
        return DIST_INDEX.read_text(encoding="utf-8")
    if SOURCE_INDEX.exists():
        return SOURCE_INDEX.read_text(encoding="utf-8")
    return "<!doctype html><title>Hearth Users</title><h1>Hearth Users</h1><button>Login</button>"


def create_app() -> FastAPI:
    app = FastAPI(title="Hearth Users", docs_url=None, redoc_url=None)

    @app.get("/health")
    async def health() -> dict[str, object]:
        return {"ok": True, "service": "hearth-users"}

    @app.get("/", response_class=HTMLResponse)
    async def index() -> str:
        return _placeholder_html()

    @app.get("/{_path:path}", response_class=HTMLResponse)
    async def spa_fallback(_path: str) -> str:
        return _placeholder_html()

    return app
