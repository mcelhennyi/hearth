"""Smoke tests for the built-in hearth-users scaffold."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_hearth_users_app() -> object:
    app_path = REPO_ROOT / "apps" / "builtin" / "hearth-users" / "hearth_users" / "app.py"
    spec = importlib.util.spec_from_file_location("hearth_users_app", app_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_hearth_users_health() -> None:
    module = _load_hearth_users_app()
    client = TestClient(module.create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True, "service": "hearth-users"}


def test_hearth_users_placeholder_login() -> None:
    module = _load_hearth_users_app()
    client = TestClient(module.create_app())

    response = client.get("/")

    assert response.status_code == 200
    assert "Hearth Users" in response.text
    assert "Login" in response.text
