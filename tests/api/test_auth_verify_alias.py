"""Hub auth verify alias tests — T-FR-0004-04."""

from __future__ import annotations

import hmac
import time
from collections.abc import Awaitable, Callable
from hashlib import sha256
from pathlib import Path
from typing import Any

import httpx
import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from app import auth_verify


FetchFn = Callable[[str, Request], Awaitable[auth_verify.ProviderResult]]


def _signature(secret: str, *, user_id: str, ts: str, method: str, path: str) -> str:
    payload = f"{user_id}\n{ts}\n{method}\n{path}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), payload, sha256).hexdigest()


@pytest.fixture()
def sig_secret(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> str:
    path = tmp_path / "secrets" / "user-sig.key"
    monkeypatch.setenv("HEARTH_USER_SIG_SECRET_PATH", str(path))
    return "unit-test-secret"


def test_builtin_verify_forwards_cookie_and_returns_signed_headers(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    sig_secret: str,
) -> None:
    monkeypatch.setenv("HEARTH_USER_SIG_SECRET", sig_secret)
    monkeypatch.setenv("HEARTH_BUILTIN_AUTH_VERIFY_URL", "http://hearth-users.test/api/verify")
    captured: dict[str, Any] = {}

    async def fake_fetch(url: str, request: Request) -> auth_verify.ProviderResult:
        captured["url"] = url
        captured["cookie"] = request.headers.get("cookie")
        return auth_verify.ProviderResult(
            status_code=200,
            claims={"user_id": "local", "display_name": "Local user", "roles": ["user"]},
        )

    monkeypatch.setattr(auth_verify, "fetch_provider_claims", fake_fetch)

    resp = client.get(
        "/api/auth/verify",
        cookies={"hearth_session": "session-token"},
        headers={
            "X-Forwarded-Method": "POST",
            "X-Forwarded-Uri": "/groceries/api/items",
        },
    )

    assert resp.status_code == 200
    assert captured == {
        "url": "http://hearth-users.test/api/verify",
        "cookie": "hearth_session=session-token",
    }
    assert resp.headers["X-Hearth-User-Id"] == "local"
    assert resp.headers["X-Hearth-User-Name"] == "Local user"
    assert resp.headers["X-Hearth-Roles"] == "user"
    assert abs(int(resp.headers["X-Hearth-User-Ts"]) - int(time.time())) <= 5
    assert resp.headers["X-Hearth-User-Sig"] == _signature(
        sig_secret,
        user_id="local",
        ts=resp.headers["X-Hearth-User-Ts"],
        method="POST",
        path="/groceries/api/items",
    )


def test_external_verify_uses_configured_url(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    sig_secret: str,
) -> None:
    monkeypatch.setenv("HEARTH_USER_SIG_SECRET", sig_secret)
    client.put(
        "/api/settings",
        json={
            "auth": {
                "provider": "external",
                "external_verify_url": "http://external-auth.test/verify",
            }
        },
    )
    captured: dict[str, str] = {}

    async def fake_fetch(url: str, _request: Request) -> auth_verify.ProviderResult:
        captured["url"] = url
        return auth_verify.ProviderResult(
            status_code=200,
            claims={"user_id": "external-user", "roles": "admin,user"},
        )

    monkeypatch.setattr(auth_verify, "fetch_provider_claims", fake_fetch)

    resp = client.get("/api/auth/verify")

    assert resp.status_code == 200
    assert captured["url"] == "http://external-auth.test/verify"
    assert resp.headers["X-Hearth-User-Id"] == "external-user"
    assert resp.headers["X-Hearth-Roles"] == "admin,user"


def test_external_verify_round_trips_to_mock_http_provider(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    sig_secret: str,
) -> None:
    monkeypatch.setenv("HEARTH_USER_SIG_SECRET", sig_secret)
    client.put(
        "/api/settings",
        json={
            "auth": {
                "provider": "external",
                "external_verify_url": "http://external-auth.test/verify",
            }
        },
    )
    seen: dict[str, str | None] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["cookie"] = request.headers.get("cookie")
        return httpx.Response(200, json={"user_id": "mock-user", "roles": ["user"]})

    transport = httpx.MockTransport(handler)
    real_async_client = httpx.AsyncClient

    def mock_client(*_args: Any, **_kwargs: Any) -> httpx.AsyncClient:
        return real_async_client(transport=transport)

    monkeypatch.setattr(auth_verify.httpx, "AsyncClient", mock_client)

    resp = client.get("/api/auth/verify", cookies={"hearth_session": "external-session"})

    assert resp.status_code == 200
    assert seen == {
        "url": "http://external-auth.test/verify",
        "cookie": "hearth_session=external-session",
    }
    assert resp.headers["X-Hearth-User-Id"] == "mock-user"


def test_verify_returns_401_without_signed_headers_when_provider_rejects(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_fetch(_url: str, _request: Request) -> auth_verify.ProviderResult:
        return auth_verify.ProviderResult(status_code=401, claims=None)

    monkeypatch.setattr(auth_verify, "fetch_provider_claims", fake_fetch)

    resp = client.get("/api/auth/verify")

    assert resp.status_code == 401
    assert "X-Hearth-User-Id" not in resp.headers
    assert "X-Hearth-User-Sig" not in resp.headers


def test_external_verify_without_url_fails_closed(client: TestClient) -> None:
    client.put("/api/settings", json={"auth": {"provider": "external"}})

    resp = client.get("/api/auth/verify")

    assert resp.status_code == 503


def test_unreachable_provider_fails_closed(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_fetch(_url: str, _request: Request) -> auth_verify.ProviderResult:
        raise httpx.ConnectError("provider down")

    monkeypatch.setattr(auth_verify, "fetch_provider_claims", fake_fetch)

    resp = client.get("/api/auth/verify")

    assert resp.status_code == 503
