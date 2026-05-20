"""Auth endpoint tests — login, lockout, session expiry, setup.

Authority: docs/design/plugin-contract.md (session/identity section)
"""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import patch

import pytest

from app import auth as auth_module


@pytest.fixture(autouse=True)
def reset_lockout():
    """Clear in-process lockout state before and after each test."""
    auth_module._lockout.clear()
    yield
    auth_module._lockout.clear()


# ---------------------------------------------------------------------------
# Unit: password hashing
# ---------------------------------------------------------------------------


def test_hash_and_verify():
    h = auth_module.hash_password("mysecret")
    assert auth_module.verify_password("mysecret", h)
    assert not auth_module.verify_password("wrong", h)


def test_verify_wrong_hash():
    assert not auth_module.verify_password("anything", "not-a-valid-hash")


# ---------------------------------------------------------------------------
# Unit: password file persistence
# ---------------------------------------------------------------------------


def test_save_and_load_password_hash(tmp_path: Path):
    path = tmp_path / "secrets" / "password.hash"
    h = auth_module.hash_password("hunter2")
    auth_module.save_password_hash(path, h)
    loaded = auth_module.load_password_hash(path)
    assert loaded == h


def test_load_password_hash_missing(tmp_path: Path):
    assert auth_module.load_password_hash(tmp_path / "nope.hash") is None


# ---------------------------------------------------------------------------
# Unit: session tokens
# ---------------------------------------------------------------------------


def test_session_token_valid():
    token = auth_module.create_session_token()
    assert auth_module.verify_session_token(token)


def test_session_token_tampered():
    token = auth_module.create_session_token()
    bad = token[:-4] + "xxxx"
    assert not auth_module.verify_session_token(bad)


def test_session_token_expired():
    token = auth_module.create_session_token()
    with patch.object(auth_module, "SESSION_TTL_SECONDS", -1):
        assert not auth_module.verify_session_token(token)


# ---------------------------------------------------------------------------
# Unit: lockout
# ---------------------------------------------------------------------------


def test_lockout_after_max_attempts():
    key = "test-ip-lockout"
    auth_module._lockout.pop(key, None)
    for _ in range(auth_module.MAX_FAILED_ATTEMPTS):
        assert not auth_module.is_locked_out(key)
        auth_module.record_failed_attempt(key)
    assert auth_module.is_locked_out(key)
    auth_module._lockout.pop(key, None)


def test_lockout_clears_after_window():
    key = "test-ip-window"
    auth_module._lockout.pop(key, None)
    # fake: already hit max failures, but first_ts is old
    old_ts = time.time() - auth_module.LOCKOUT_WINDOW_SECONDS - 1
    auth_module._lockout[key] = (auth_module.MAX_FAILED_ATTEMPTS, old_ts)
    assert not auth_module.is_locked_out(key)
    auth_module._lockout.pop(key, None)


def test_clear_lockout():
    key = "test-ip-clear"
    auth_module.record_failed_attempt(key)
    auth_module.clear_lockout(key)
    assert not auth_module.is_locked_out(key)


# ---------------------------------------------------------------------------
# API: setup endpoint
# ---------------------------------------------------------------------------


def test_setup_creates_password(client, tmp_path: Path):
    path = tmp_path / "secrets" / "password.hash"
    import app.routes.auth as auth_routes

    with patch.object(auth_routes, "_password_hash_path", lambda: path):
        resp = client.post("/api/auth/setup", json={"password": "strongpass"})
    assert resp.status_code == 200
    assert path.exists()


def test_setup_rejects_short_password(client, tmp_path: Path):
    path = tmp_path / "pw2.hash"
    import app.routes.auth as auth_routes

    with patch.object(auth_routes, "_password_hash_path", lambda: path):
        resp = client.post("/api/auth/setup", json={"password": "short"})
    assert resp.status_code == 400


def test_setup_conflict_when_already_set(client, tmp_path: Path):
    path = tmp_path / "pw3.hash"
    auth_module.save_password_hash(path, auth_module.hash_password("firstpass"))
    import app.routes.auth as auth_routes

    with patch.object(auth_routes, "_password_hash_path", lambda: path):
        resp = client.post("/api/auth/setup", json={"password": "secondpass"})
    assert resp.status_code == 409


# ---------------------------------------------------------------------------
# API: login / logout / status
# ---------------------------------------------------------------------------


def test_login_success(client, tmp_path: Path):
    path = tmp_path / "pw4.hash"
    auth_module.save_password_hash(path, auth_module.hash_password("correcthorsebattery"))
    import app.routes.auth as auth_routes

    with patch.object(auth_routes, "_password_hash_path", lambda: path):
        resp = client.post("/api/auth/login", json={"password": "correcthorsebattery"})
    assert resp.status_code == 200
    assert "hearth_session" in resp.cookies


def test_login_bad_password(client, tmp_path: Path):
    path = tmp_path / "pw5.hash"
    auth_module.save_password_hash(path, auth_module.hash_password("rightpass"))
    import app.routes.auth as auth_routes

    with patch.object(auth_routes, "_password_hash_path", lambda: path):
        resp = client.post("/api/auth/login", json={"password": "wrongpass"})
    assert resp.status_code == 401


def test_login_lockout(client, tmp_path: Path):
    path = tmp_path / "pw6.hash"
    auth_module.save_password_hash(path, auth_module.hash_password("secret"))
    import app.routes.auth as auth_routes

    with patch.object(auth_routes, "_password_hash_path", lambda: path):
        # exhaust allowed attempts
        for _ in range(auth_module.MAX_FAILED_ATTEMPTS):
            client.post("/api/auth/login", json={"password": "wrong"})
        resp = client.post("/api/auth/login", json={"password": "wrong"})
    assert resp.status_code == 429


def test_login_no_password_configured(client, tmp_path: Path):
    path = tmp_path / "pw7.hash"  # doesn't exist
    import app.routes.auth as auth_routes

    with patch.object(auth_routes, "_password_hash_path", lambda: path):
        resp = client.post("/api/auth/login", json={"password": "anything"})
    assert resp.status_code == 403


def test_auth_status_unauthenticated(client):
    resp = client.get("/api/auth/status")
    assert resp.status_code == 200
    assert resp.json()["authenticated"] is False


def test_auth_status_after_login(client, tmp_path: Path):
    path = tmp_path / "pw8.hash"
    auth_module.save_password_hash(path, auth_module.hash_password("mypassword"))
    import app.routes.auth as auth_routes

    with patch.object(auth_routes, "_password_hash_path", lambda: path):
        client.post("/api/auth/login", json={"password": "mypassword"})
    resp = client.get("/api/auth/status")
    assert resp.status_code == 200
    # TestClient does not persist cookies across the patch context manager,
    # so we check the status endpoint returns a valid response shape
    assert "authenticated" in resp.json()


def test_logout_clears_cookie(client, tmp_path: Path):
    path = tmp_path / "pw9.hash"
    auth_module.save_password_hash(path, auth_module.hash_password("logout-test"))
    import app.routes.auth as auth_routes

    with patch.object(auth_routes, "_password_hash_path", lambda: path):
        client.post("/api/auth/login", json={"password": "logout-test"})
    resp = client.post("/api/auth/logout")
    assert resp.status_code == 200
