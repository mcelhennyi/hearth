"""Gateway-to-plugin identity contract tests for FR-0004 capstone."""

from __future__ import annotations

import importlib
import sys
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

from fastapi import Request
from fastapi.testclient import TestClient

from app import auth_verify
from hearth_kindling_contract import render_plugin_template


FetchFn = Callable[[str, Request], Awaitable[auth_verify.ProviderResult]]


def _rendered_plugin_client(tmp_path: Path, monkeypatch: Any) -> TestClient:
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")
    monkeypatch.syspath_prepend(str(plugin_root))
    for module_name in ["sample_plugin.app", "sample_plugin.trust", "sample_plugin"]:
        sys.modules.pop(module_name, None)
    app_module = importlib.import_module("sample_plugin.app")
    return TestClient(app_module.create_app())


def test_gateway_signed_identity_is_accepted_by_generated_plugin(
    client: TestClient,
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("HEARTH_USER_SIG_SECRET", "capstone-secret")

    async def fake_fetch(_url: str, _request: Request) -> auth_verify.ProviderResult:
        return auth_verify.ProviderResult(
            status_code=200,
            claims={
                "user_id": "local-owner",
                "display_name": "Local Owner",
                "roles": ["owner"],
            },
        )

    monkeypatch.setattr(auth_verify, "fetch_provider_claims", fake_fetch)

    verify_response = client.get(
        "/api/auth/verify",
        cookies={"hearth_session": "session-token"},
        headers={
            "X-Forwarded-Method": "GET",
            "X-Forwarded-Uri": "/sample-plugin/api/me",
        },
    )
    assert verify_response.status_code == 200

    plugin_client = _rendered_plugin_client(tmp_path, monkeypatch)
    gateway_headers = {
        "X-Hearth-User-Id": verify_response.headers["X-Hearth-User-Id"],
        "X-Hearth-User-Ts": verify_response.headers["X-Hearth-User-Ts"],
        "X-Hearth-User-Sig": verify_response.headers["X-Hearth-User-Sig"],
        "X-Hearth-User-Name": verify_response.headers["X-Hearth-User-Name"],
        "X-Hearth-Roles": verify_response.headers["X-Hearth-Roles"],
        "X-Original-Method": "GET",
        "X-Original-Uri": "/sample-plugin/api/me",
    }

    direct_response = plugin_client.get("/api/me")
    assert direct_response.status_code == 401

    missing_original_uri = plugin_client.get(
        "/api/me",
        headers={key: value for key, value in gateway_headers.items() if key != "X-Original-Uri"},
    )
    assert missing_original_uri.status_code == 401
    assert missing_original_uri.json()["detail"] == "invalid Hearth user signature"

    proxied_response = plugin_client.get("/api/me", headers=gateway_headers)

    assert proxied_response.status_code == 200
    assert proxied_response.json() == {
        "id": "local-owner",
        "name": "Local Owner",
        "roles": ["owner"],
    }


def test_gateway_and_kindling_trust_accept_distinct_real_user_claims(
    client: TestClient,
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("HEARTH_USER_SIG_SECRET", "real-user-secret")
    claims_by_cookie = {
        "ada-session": {
            "user_id": "user_ada_123",
            "display_name": "Ada Lovelace",
            "roles": ["admin", "user"],
        },
        "grace-session": {
            "user_id": "user_grace_456",
            "display_name": "Grace Hopper",
            "roles": ["user"],
        },
    }

    async def fake_fetch(_url: str, request: Request) -> auth_verify.ProviderResult:
        token = request.headers.get("cookie", "").removeprefix("hearth_session=")
        return auth_verify.ProviderResult(status_code=200, claims=claims_by_cookie[token])

    monkeypatch.setattr(auth_verify, "fetch_provider_claims", fake_fetch)
    plugin_client = _rendered_plugin_client(tmp_path, monkeypatch)

    results: list[dict[str, object]] = []
    for token in ["ada-session", "grace-session"]:
        verify_response = client.get(
            "/api/auth/verify",
            cookies={"hearth_session": token},
            headers={
                "X-Forwarded-Method": "GET",
                "X-Forwarded-Uri": "/sample-plugin/api/me",
            },
        )
        assert verify_response.status_code == 200
        proxied_response = plugin_client.get(
            "/api/me",
            headers={
                "X-Hearth-User-Id": verify_response.headers["X-Hearth-User-Id"],
                "X-Hearth-User-Ts": verify_response.headers["X-Hearth-User-Ts"],
                "X-Hearth-User-Sig": verify_response.headers["X-Hearth-User-Sig"],
                "X-Hearth-User-Name": verify_response.headers["X-Hearth-User-Name"],
                "X-Hearth-Roles": verify_response.headers["X-Hearth-Roles"],
                "X-Original-Method": "GET",
                "X-Original-Uri": "/sample-plugin/api/me",
            },
        )
        assert proxied_response.status_code == 200
        results.append(proxied_response.json())

    assert results == [
        {"id": "user_ada_123", "name": "Ada Lovelace", "roles": ["admin", "user"]},
        {"id": "user_grace_456", "name": "Grace Hopper", "roles": ["user"]},
    ]
