"""Multi-user end-to-end auth proof for FR-0004 closeout."""

from __future__ import annotations

import importlib
import importlib.util
import sys
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

from fastapi import Request
from fastapi.testclient import TestClient

from app import auth_verify
from hearth_kindling_contract import render_plugin_template

REPO_ROOT = Path(__file__).resolve().parents[2]
FetchFn = Callable[[str, Request], Awaitable[auth_verify.ProviderResult]]


def _load_hearth_users_app() -> object:
    app_path = REPO_ROOT / "apps" / "builtin" / "hearth-users" / "hearth_users" / "app.py"
    spec = importlib.util.spec_from_file_location("hearth_users_app_e2e", app_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _hearth_users_client(module: object, data_dir: Path) -> TestClient:
    return TestClient(module.create_app(data_dir=data_dir), base_url="https://hearth-users.test")


def _rendered_plugin_client(tmp_path: Path, monkeypatch: Any) -> TestClient:
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")
    monkeypatch.syspath_prepend(str(plugin_root))
    for module_name in ["sample_plugin.app", "sample_plugin.trust", "sample_plugin"]:
        sys.modules.pop(module_name, None)
    app_module = importlib.import_module("sample_plugin.app")
    return TestClient(app_module.create_app())


def _gateway_headers(response: Any) -> dict[str, str]:
    return {
        "X-Hearth-User-Id": response.headers["X-Hearth-User-Id"],
        "X-Hearth-User-Ts": response.headers["X-Hearth-User-Ts"],
        "X-Hearth-User-Sig": response.headers["X-Hearth-User-Sig"],
        "X-Hearth-User-Name": response.headers["X-Hearth-User-Name"],
        "X-Hearth-Roles": response.headers["X-Hearth-Roles"],
        "X-Original-Method": "GET",
        "X-Original-Uri": "/sample-plugin/api/me",
    }


def test_first_admin_second_user_and_plugin_identity_switch(
    client: TestClient,
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("HEARTH_USER_SIG_SECRET", "multi-user-e2e-secret")
    users_module = _load_hearth_users_app()
    users_module._lockout.clear()
    users_data = tmp_path / "users"
    admin_client = _hearth_users_client(users_module, users_data)

    setup = admin_client.post(
        "/api/setup",
        json={
            "username": "ada",
            "display_name": "Ada Lovelace",
            "password": "ada-password",
        },
    )
    created = admin_client.post(
        "/api/admin/users",
        json={
            "username": "grace",
            "display_name": "Grace Hopper",
            "password": "grace-password",
            "roles": ["user"],
        },
    )
    assert setup.status_code == 200
    assert created.status_code == 201

    ada_client = _hearth_users_client(users_module, users_data)
    grace_client = _hearth_users_client(users_module, users_data)
    ada_login = ada_client.post("/login", json={"username": "ada", "password": "ada-password"})
    grace_login = grace_client.post(
        "/login", json={"username": "grace", "password": "grace-password"}
    )
    assert ada_login.status_code == 200
    assert grace_login.status_code == 200

    async def fetch_from_real_hearth_users(
        _url: str, request: Request
    ) -> auth_verify.ProviderResult:
        verifier = _hearth_users_client(users_module, users_data)
        response = verifier.get("/api/verify", headers={"cookie": request.headers["cookie"]})
        return auth_verify.ProviderResult(
            status_code=response.status_code,
            claims=response.json() if response.status_code == 200 else None,
        )

    monkeypatch.setattr(auth_verify, "fetch_provider_claims", fetch_from_real_hearth_users)
    plugin_client = _rendered_plugin_client(tmp_path, monkeypatch)

    results: list[dict[str, object]] = []
    for token in [
        ada_login.cookies["hearth_session"],
        grace_login.cookies["hearth_session"],
    ]:
        verified = client.get(
            "/api/auth/verify",
            cookies={"hearth_session": token},
            headers={
                "X-Forwarded-Method": "GET",
                "X-Forwarded-Uri": "/sample-plugin/api/me",
            },
        )
        assert verified.status_code == 200
        plugin_response = plugin_client.get("/api/me", headers=_gateway_headers(verified))
        assert plugin_response.status_code == 200
        results.append(plugin_response.json())

    assert results == [
        {"id": setup.json()["user_id"], "name": "Ada Lovelace", "roles": ["admin", "user"]},
        {"id": created.json()["user_id"], "name": "Grace Hopper", "roles": ["user"]},
    ]
