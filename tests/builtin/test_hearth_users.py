"""Tests for the built-in hearth-users plugin."""

from __future__ import annotations

import importlib.util
import json
import sqlite3
from pathlib import Path
from unittest.mock import patch

import pytest
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


@pytest.fixture()
def hearth_users() -> object:
    module = _load_hearth_users_app()
    module._lockout.clear()
    yield module
    module._lockout.clear()


def _client(
    module: object,
    data_dir: Path,
    audit_log_path: Path | None = None,
    bootstrap_password_file: Path | None = None,
) -> TestClient:
    kwargs = {"data_dir": data_dir}
    if audit_log_path is not None:
        kwargs["audit_log_path"] = audit_log_path
    if bootstrap_password_file is not None:
        kwargs["bootstrap_password_file"] = bootstrap_password_file
    return TestClient(module.create_app(**kwargs), base_url="https://testserver")


def test_hearth_users_health(tmp_path: Path) -> None:
    module = _load_hearth_users_app()
    client = _client(module, tmp_path)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True, "service": "hearth-users"}


def test_hearth_users_placeholder_login(tmp_path: Path) -> None:
    module = _load_hearth_users_app()
    client = _client(module, tmp_path)

    response = client.get("/")

    assert response.status_code == 200
    assert "Hearth Users" in response.text
    assert "Login" in response.text


def test_first_run_setup_stores_argon2id_password_in_plugin_sqlite(
    hearth_users: object, tmp_path: Path
) -> None:
    client = _client(hearth_users, tmp_path)

    response = client.post("/api/setup", json={"password": "correcthorsebattery"})

    assert response.status_code == 200
    assert response.json() == {
        "user_id": "local",
        "display_name": "Local user",
        "roles": ["user"],
    }
    db_path = tmp_path / "users.sqlite"
    assert db_path.exists()
    with sqlite3.connect(db_path) as conn:
        row = conn.execute("select password_hash from users where id = 'local'").fetchone()
    assert row is not None
    assert row[0].startswith("$argon2id$")
    assert "correcthorsebattery" not in row[0]


def test_bootstrap_password_file_seeds_local_user(
    hearth_users: object, tmp_path: Path
) -> None:
    password_file = tmp_path / "secrets" / "hearth-users-default-password"
    password_file.parent.mkdir()
    password_file.write_text("dev-default-password\n", encoding="utf-8")
    audit_log_path = tmp_path / "auth-session.jsonl"
    client = _client(
        hearth_users,
        tmp_path / "data",
        audit_log_path,
        bootstrap_password_file=password_file,
    )

    login = client.post("/login", json={"password": "dev-default-password"})

    assert login.status_code == 200
    assert login.json() == {
        "user_id": "local",
        "display_name": "Local user",
        "roles": ["user"],
    }
    records = [json.loads(line) for line in audit_log_path.read_text().splitlines()]
    assert records[0]["action"] == "auth.bootstrap"
    assert records[0]["user_id"] == "local"


def test_bootstrap_password_file_does_not_override_existing_user(
    hearth_users: object, tmp_path: Path
) -> None:
    password_file = tmp_path / "secrets" / "hearth-users-default-password"
    password_file.parent.mkdir()
    password_file.write_text("bootstrap-password\n", encoding="utf-8")
    data_dir = tmp_path / "data"
    client = _client(hearth_users, data_dir)
    assert client.post("/api/setup", json={"password": "first-password"}).status_code == 200

    restarted = _client(hearth_users, data_dir, bootstrap_password_file=password_file)

    assert restarted.post("/login", json={"password": "bootstrap-password"}).status_code == 401
    assert restarted.post("/login", json={"password": "first-password"}).status_code == 200


def test_short_bootstrap_password_file_is_ignored_without_crashing(
    hearth_users: object, tmp_path: Path
) -> None:
    password_file = tmp_path / "secrets" / "hearth-users-default-password"
    password_file.parent.mkdir()
    password_file.write_text("short\n", encoding="utf-8")

    client = _client(hearth_users, tmp_path / "data", bootstrap_password_file=password_file)

    assert client.get("/health").status_code == 200
    assert client.post("/login", json={"password": "short"}).status_code == 403
    assert client.post("/api/setup", json={"password": "first-password"}).status_code == 200


def test_setup_rejects_second_password(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)
    assert client.post("/api/setup", json={"password": "first-password"}).status_code == 200

    response = client.post("/api/setup", json={"password": "second-password"})

    assert response.status_code == 409


def test_login_sets_session_cookie_and_session_returns_claims(
    hearth_users: object, tmp_path: Path
) -> None:
    client = _client(hearth_users, tmp_path)
    client.post("/api/setup", json={"password": "correcthorsebattery"})

    login = client.post("/login", json={"password": "correcthorsebattery"})
    session = client.get("/api/session")

    assert login.status_code == 200
    assert "hearth_session" in login.cookies
    assert session.status_code == 200
    assert session.json() == {
        "user_id": "local",
        "display_name": "Local user",
        "roles": ["user"],
    }


def test_spark_session_current_returns_claims_for_session_token(
    hearth_users: object, tmp_path: Path
) -> None:
    store = hearth_users.UsersStore(tmp_path)
    store.create_user("current-password")
    token = store.create_session("local")

    result = hearth_users.spark_session_current(store, {"session_token": token})

    assert result == {
        "authenticated": True,
        "user_id": "local",
        "display_name": "Local user",
        "roles": ["user"],
    }


def test_spark_session_current_returns_unauthenticated_without_session(
    hearth_users: object, tmp_path: Path
) -> None:
    store = hearth_users.UsersStore(tmp_path)

    result = hearth_users.spark_session_current(store, {})

    assert result == {"authenticated": False}


def test_bad_password_and_lockout(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)
    client.post("/api/setup", json={"password": "right-password"})

    for _ in range(hearth_users.MAX_FAILED_ATTEMPTS):
        response = client.post("/login", json={"password": "wrong-password"})
        assert response.status_code == 401

    locked = client.post("/login", json={"password": "right-password"})

    assert locked.status_code == 429


def test_logout_clears_session_cookie(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)
    client.post("/api/setup", json={"password": "logout-password"})
    client.post("/login", json={"password": "logout-password"})

    logout = client.post("/logout")
    session = client.get("/api/session")

    assert logout.status_code == 200
    assert session.status_code == 401


def test_login_and_logout_write_session_audit_events(
    hearth_users: object, tmp_path: Path
) -> None:
    audit_log_path = tmp_path / "auth-session.jsonl"
    client = _client(hearth_users, tmp_path, audit_log_path)
    client.post("/api/setup", json={"password": "audit-password"})

    login = client.post("/login", json={"password": "audit-password"})
    logout = client.post("/logout")

    assert login.status_code == 200
    assert logout.status_code == 200
    records = [json.loads(line) for line in audit_log_path.read_text().splitlines()]
    assert [record["action"] for record in records] == [
        "auth.setup",
        "auth.login",
        "auth.logout",
    ]
    assert all(record["plugin_slug"] == "hearth-users" for record in records)
    assert records[1]["topic"] == "hearth-users.session.login"
    assert records[2]["topic"] == "hearth-users.session.logout"


def test_verify_returns_401_without_session(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)

    response = client.get("/api/verify")

    assert response.status_code == 401


def test_verify_returns_claims_with_valid_session(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)
    client.post("/api/setup", json={"password": "verify-password"})
    client.post("/login", json={"password": "verify-password"})

    response = client.get("/api/verify")

    assert response.status_code == 200
    assert response.json() == {
        "user_id": "local",
        "display_name": "Local user",
        "roles": ["user"],
    }


def test_session_expiry_invalidates_verify(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)
    client.post("/api/setup", json={"password": "expiry-password"})

    with patch.object(hearth_users, "SESSION_TTL_SECONDS", -1):
        client.post("/login", json={"password": "expiry-password"})

    response = client.get("/api/verify")

    assert response.status_code == 401
