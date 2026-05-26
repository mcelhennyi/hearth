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


def test_hearth_users_login_page_renders_setup_form(tmp_path: Path) -> None:
    module = _load_hearth_users_app()
    client = _client(module, tmp_path)

    response = client.get("/login?next=/groceries")

    assert response.status_code == 200
    assert "Hearth Users" in response.text
    assert "Create your Hearth admin" in response.text
    assert 'data-mode="setup"' in response.text
    assert 'data-next="/groceries"' in response.text
    assert "/src/main.ts" not in response.text


def test_hearth_users_login_page_renders_login_after_setup(
    hearth_users: object, tmp_path: Path
) -> None:
    client = _client(hearth_users, tmp_path)
    assert (
        client.post(
            "/api/setup",
            json={
                "username": "local",
                "display_name": "Local user",
                "password": "correcthorsebattery",
            },
        ).status_code
        == 200
    )

    response = client.get("/login?next=https://evil.example/path")

    assert response.status_code == 200
    assert "Sign in to Hearth" in response.text
    assert 'data-mode="login"' in response.text
    assert 'data-next="/"' in response.text


def test_first_run_setup_stores_argon2id_password_in_plugin_sqlite(
    hearth_users: object, tmp_path: Path
) -> None:
    client = _client(hearth_users, tmp_path)

    response = client.post(
        "/api/setup",
        json={
            "username": "Ada",
            "display_name": "Ada Lovelace",
            "password": "correcthorsebattery",
        },
    )

    assert response.status_code == 200
    claims = response.json()
    assert claims["user_id"] != "local"
    assert claims["display_name"] == "Ada Lovelace"
    assert claims["roles"] == ["admin", "user"]
    db_path = tmp_path / "users.sqlite"
    assert db_path.exists()
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "select id, username, display_name, roles, disabled, password_hash from users"
        ).fetchone()
    assert row is not None
    assert row[0] == claims["user_id"]
    assert row[1] == "ada"
    assert row[2] == "Ada Lovelace"
    assert row[3] == "admin,user"
    assert row[4] == 0
    assert row[5].startswith("$argon2id$")
    assert "correcthorsebattery" not in row[5]


def test_setup_requires_username_and_display_name(
    hearth_users: object, tmp_path: Path
) -> None:
    client = _client(hearth_users, tmp_path)

    missing_username = client.post(
        "/api/setup", json={"display_name": "Ada Lovelace", "password": "correcthorsebattery"}
    )
    missing_display_name = client.post(
        "/api/setup", json={"username": "ada", "password": "correcthorsebattery"}
    )

    assert missing_username.status_code == 400
    assert missing_display_name.status_code == 400


def test_setup_rejects_duplicate_normalized_username(
    hearth_users: object, tmp_path: Path
) -> None:
    store = hearth_users.UsersStore(tmp_path)
    store.create_user(
        username="Ada",
        display_name="Ada Lovelace",
        password="correcthorsebattery",
        roles=["admin", "user"],
    )

    with pytest.raises(ValueError, match="Username already exists"):
        store.create_user(
            username=" ada ",
            display_name="Another Ada",
            password="another-password",
            roles=["user"],
        )


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

    login = client.post(
        "/login", json={"username": "local", "password": "dev-default-password"}
    )

    assert login.status_code == 200
    assert login.json() == {
        "user_id": "local",
        "display_name": "Local user",
        "roles": ["admin", "user"],
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
    assert (
        client.post(
            "/api/setup",
            json={"username": "local", "display_name": "Local user", "password": "first-password"},
        ).status_code
        == 200
    )

    restarted = _client(hearth_users, data_dir, bootstrap_password_file=password_file)

    assert (
        restarted.post(
            "/login", json={"username": "local", "password": "bootstrap-password"}
        ).status_code
        == 401
    )
    assert (
        restarted.post(
            "/login", json={"username": "local", "password": "first-password"}
        ).status_code
        == 200
    )


def test_short_bootstrap_password_file_is_ignored_without_crashing(
    hearth_users: object, tmp_path: Path
) -> None:
    password_file = tmp_path / "secrets" / "hearth-users-default-password"
    password_file.parent.mkdir()
    password_file.write_text("short\n", encoding="utf-8")

    client = _client(hearth_users, tmp_path / "data", bootstrap_password_file=password_file)

    assert client.get("/health").status_code == 200
    assert client.post("/login", json={"username": "local", "password": "short"}).status_code == 403
    assert (
        client.post(
            "/api/setup",
            json={"username": "local", "display_name": "Local user", "password": "first-password"},
        ).status_code
        == 200
    )


def test_setup_rejects_second_password(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)
    assert (
        client.post(
            "/api/setup",
            json={"username": "local", "display_name": "Local user", "password": "first-password"},
        ).status_code
        == 200
    )

    response = client.post(
        "/api/setup",
        json={"username": "other", "display_name": "Other user", "password": "second-password"},
    )

    assert response.status_code == 409


def test_login_sets_session_cookie_and_session_returns_claims(
    hearth_users: object, tmp_path: Path
) -> None:
    client = _client(hearth_users, tmp_path)
    client.post(
        "/api/setup",
        json={
            "username": "ada",
            "display_name": "Ada Lovelace",
            "password": "correcthorsebattery",
        },
    )

    login = client.post("/login", json={"username": "ada", "password": "correcthorsebattery"})
    session = client.get("/api/session")

    assert login.status_code == 200
    assert "hearth_session" in login.cookies
    assert session.status_code == 200
    assert login.json()["display_name"] == "Ada Lovelace"
    assert login.json()["roles"] == ["admin", "user"]
    assert session.json() == login.json()


def test_login_requires_username_and_password(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)
    client.post(
        "/api/setup",
        json={"username": "ada", "display_name": "Ada Lovelace", "password": "right-password"},
    )

    response = client.post("/login", json={"password": "right-password"})

    assert response.status_code == 400


def test_multi_user_login_uses_requested_username(hearth_users: object, tmp_path: Path) -> None:
    store = hearth_users.UsersStore(tmp_path)
    ada = store.create_user(
        username="ada",
        display_name="Ada Lovelace",
        password="ada-password",
        roles=["admin", "user"],
    )
    grace = store.create_user(
        username="grace",
        display_name="Grace Hopper",
        password="grace-password",
        roles=["user"],
    )
    client = _client(hearth_users, tmp_path)

    ada_login = client.post("/login", json={"username": "ADA", "password": "ada-password"})
    grace_login = client.post("/login", json={"username": "grace", "password": "grace-password"})

    assert ada_login.status_code == 200
    assert ada_login.json() == ada
    assert grace_login.status_code == 200
    assert grace_login.json() == grace


def test_spark_session_current_returns_claims_for_session_token(
    hearth_users: object, tmp_path: Path
) -> None:
    store = hearth_users.UsersStore(tmp_path)
    claims = store.create_user(
        username="ada",
        display_name="Ada Lovelace",
        password="current-password",
        roles=["admin", "user"],
    )
    token = store.create_session(str(claims["user_id"]))

    result = hearth_users.spark_session_current(store, {"session_token": token})

    assert result == {
        "authenticated": True,
        "user_id": claims["user_id"],
        "display_name": "Ada Lovelace",
        "roles": ["admin", "user"],
    }


def test_sessions_spark_and_audit_distinguish_multiple_users(
    hearth_users: object, tmp_path: Path
) -> None:
    audit_log_path = tmp_path / "auth-session.jsonl"
    store = hearth_users.UsersStore(tmp_path)
    ada = store.create_user(
        username="ada",
        display_name="Ada Lovelace",
        password="ada-password",
        roles=["admin", "user"],
    )
    grace = store.create_user(
        username="grace",
        display_name="Grace Hopper",
        password="grace-password",
        roles=["user"],
    )
    ada_client = _client(hearth_users, tmp_path, audit_log_path)
    grace_client = _client(hearth_users, tmp_path, audit_log_path)

    ada_login = ada_client.post("/login", json={"username": "ada", "password": "ada-password"})
    grace_login = grace_client.post(
        "/login", json={"username": "grace", "password": "grace-password"}
    )
    ada_session = ada_client.get("/api/session")
    grace_session = grace_client.get("/api/session")
    ada_verify = ada_client.get("/api/verify")
    grace_verify = grace_client.get("/api/verify")
    ada_token = ada_login.cookies.get("hearth_session")
    grace_token = grace_login.cookies.get("hearth_session")

    assert ada_login.status_code == 200
    assert grace_login.status_code == 200
    assert ada_session.json() == ada
    assert grace_session.json() == grace
    assert ada_verify.json() == ada
    assert grace_verify.json() == grace
    assert ada_token and grace_token and ada_token != grace_token
    assert hearth_users.spark_session_current(store, {"session_token": ada_token}) == {
        "authenticated": True,
        **ada,
    }
    assert hearth_users.spark_session_current(store, {"session_token": grace_token}) == {
        "authenticated": True,
        **grace,
    }

    grace_client.post("/logout")
    records = [json.loads(line) for line in audit_log_path.read_text().splitlines()]
    login_records = [record for record in records if record["action"] == "auth.login"]
    logout_records = [record for record in records if record["action"] == "auth.logout"]
    assert [record["topic"] for record in login_records] == [
        "hearth-users.session.login",
        "hearth-users.session.login",
    ]
    assert [record["user_id"] for record in login_records] == [
        ada["user_id"],
        grace["user_id"],
    ]
    assert logout_records[-1]["topic"] == "hearth-users.session.logout"
    assert logout_records[-1]["user_id"] == grace["user_id"]


def test_spark_session_current_returns_unauthenticated_without_session(
    hearth_users: object, tmp_path: Path
) -> None:
    store = hearth_users.UsersStore(tmp_path)

    result = hearth_users.spark_session_current(store, {})

    assert result == {"authenticated": False}


def test_bad_password_and_lockout(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)
    client.post(
        "/api/setup",
        json={"username": "local", "display_name": "Local user", "password": "right-password"},
    )

    for _ in range(hearth_users.MAX_FAILED_ATTEMPTS):
        response = client.post("/login", json={"username": "local", "password": "wrong-password"})
        assert response.status_code == 401

    locked = client.post("/login", json={"username": "local", "password": "right-password"})

    assert locked.status_code == 429


def test_logout_clears_session_cookie(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)
    client.post(
        "/api/setup",
        json={"username": "local", "display_name": "Local user", "password": "logout-password"},
    )
    client.post("/login", json={"username": "local", "password": "logout-password"})

    logout = client.post("/logout")
    session = client.get("/api/session")

    assert logout.status_code == 200
    assert session.status_code == 401


def test_login_and_logout_write_session_audit_events(
    hearth_users: object, tmp_path: Path
) -> None:
    audit_log_path = tmp_path / "auth-session.jsonl"
    client = _client(hearth_users, tmp_path, audit_log_path)
    setup = client.post(
        "/api/setup",
        json={"username": "ada", "display_name": "Ada Lovelace", "password": "audit-password"},
    )

    login = client.post("/login", json={"username": "ada", "password": "audit-password"})
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
    assert records[1]["user_id"] == setup.json()["user_id"]
    assert records[1]["roles"] == ["admin", "user"]


def test_verify_returns_401_without_session(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)

    response = client.get("/api/verify")

    assert response.status_code == 401


def test_verify_returns_claims_with_valid_session(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)
    setup = client.post(
        "/api/setup",
        json={"username": "ada", "display_name": "Ada Lovelace", "password": "verify-password"},
    )
    client.post("/login", json={"username": "ada", "password": "verify-password"})

    response = client.get("/api/verify")

    assert response.status_code == 200
    assert response.json() == setup.json()


def test_disabled_user_cannot_log_in_or_verify_existing_session(
    hearth_users: object, tmp_path: Path
) -> None:
    store = hearth_users.UsersStore(tmp_path)
    claims = store.create_user(
        username="grace",
        display_name="Grace Hopper",
        password="grace-password",
        roles=["user"],
    )
    token = store.create_session(str(claims["user_id"]))
    store.set_user_disabled(str(claims["user_id"]), True)
    client = _client(hearth_users, tmp_path)
    client.cookies.set("hearth_session", token)

    login = client.post("/login", json={"username": "grace", "password": "grace-password"})
    verify = client.get("/api/verify")

    assert login.status_code == 403
    assert verify.status_code == 401


def test_legacy_single_user_schema_migrates_to_admin_user(
    hearth_users: object, tmp_path: Path
) -> None:
    db_path = tmp_path / "users.sqlite"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            create table users (
                id text primary key,
                display_name text not null,
                roles text not null,
                password_hash text not null,
                created_at integer not null,
                updated_at integer not null
            )
            """
        )
        conn.execute(
            """
            create table sessions (
                token_hash text primary key,
                user_id text not null references users(id) on delete cascade,
                created_at integer not null,
                expires_at integer not null
            )
            """
        )
        conn.execute(
            """
            insert into users (id, display_name, roles, password_hash, created_at, updated_at)
            values ('local', 'Local user', 'user', ?, 1, 1)
            """,
            (hearth_users._hash_password("legacy-password"),),
        )

    client = _client(hearth_users, tmp_path)
    login = client.post("/login", json={"username": "local", "password": "legacy-password"})

    assert login.status_code == 200
    assert login.json() == {
        "user_id": "local",
        "display_name": "Local user",
        "roles": ["admin", "user"],
    }
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "select username, roles, disabled, last_login_at from users where id = 'local'"
        ).fetchone()
    assert row[0] == "local"
    assert row[1] == "admin,user"
    assert row[2] == 0
    assert row[3] is not None


def test_session_expiry_invalidates_verify(hearth_users: object, tmp_path: Path) -> None:
    client = _client(hearth_users, tmp_path)
    client.post(
        "/api/setup",
        json={"username": "local", "display_name": "Local user", "password": "expiry-password"},
    )

    with patch.object(hearth_users, "SESSION_TTL_SECONDS", -1):
        client.post("/login", json={"username": "local", "password": "expiry-password"})

    response = client.get("/api/verify")

    assert response.status_code == 401
