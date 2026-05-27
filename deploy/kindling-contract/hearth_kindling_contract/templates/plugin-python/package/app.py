"""FastAPI entrypoint for the generated {{ plugin_name }} plugin."""

from __future__ import annotations

from fastapi import Depends, FastAPI

from .trust import HearthUser, require_hearth_user


def create_app() -> FastAPI:
    app = FastAPI(title="{{ plugin_name }}")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "plugin": "{{ plugin_slug }}"}

    @app.get("/api/me")
    def current_user(user: HearthUser = Depends(require_hearth_user)) -> dict[str, object]:
        return {
            "id": user.id,
            "name": user.name,
            "roles": list(user.roles),
        }

    return app
