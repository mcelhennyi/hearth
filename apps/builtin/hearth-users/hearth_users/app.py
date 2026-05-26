"""FastAPI app for the built-in hearth-users plugin."""

from __future__ import annotations

import hashlib
import os
import secrets
import sqlite3
import time
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

APP_ROOT = Path(__file__).resolve().parents[1]
DIST_INDEX = APP_ROOT / "web" / "dist" / "index.html"
SOURCE_INDEX = APP_ROOT / "web" / "index.html"

SESSION_COOKIE = "hearth_session"
SESSION_TTL_SECONDS = 7 * 24 * 3600
LOCKOUT_WINDOW_SECONDS = 60
MAX_FAILED_ATTEMPTS = 5

LOCAL_USER_ID = "local"
LOCAL_DISPLAY_NAME = "Local user"
LOCAL_ROLES = ["user"]

_password_hasher = PasswordHasher()
_lockout: dict[str, tuple[int, float]] = {}


def _default_data_dir() -> Path:
    configured = os.getenv("HEARTH_USERS_DATA_DIR")
    if configured:
        return Path(configured)
    return Path(os.getenv("HEARTH_VAR_DIR", "var/hearth")) / "plugins" / "hearth-users"


def _placeholder_html() -> str:
    if DIST_INDEX.exists():
        return DIST_INDEX.read_text(encoding="utf-8")
    if SOURCE_INDEX.exists():
        return SOURCE_INDEX.read_text(encoding="utf-8")
    return "<!doctype html><title>Hearth Users</title><h1>Hearth Users</h1><button>Login</button>"


def _claims() -> dict[str, object]:
    return {
        "user_id": LOCAL_USER_ID,
        "display_name": LOCAL_DISPLAY_NAME,
        "roles": LOCAL_ROLES,
    }


def _hash_password(plain: str) -> str:
    return _password_hasher.hash(plain)


def _verify_password(plain: str, hashed: str) -> bool:
    try:
        return _password_hasher.verify(hashed, plain)
    except (InvalidHashError, VerifyMismatchError):
        return False


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _client_key(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _record_failed_attempt(client_key: str) -> None:
    now = time.time()
    count, first_ts = _lockout.get(client_key, (0, now))
    if now - first_ts > LOCKOUT_WINDOW_SECONDS:
        count, first_ts = 0, now
    _lockout[client_key] = (count + 1, first_ts)


def _is_locked_out(client_key: str) -> bool:
    count, first_ts = _lockout.get(client_key, (0, 0.0))
    if time.time() - first_ts > LOCKOUT_WINDOW_SECONDS:
        _lockout.pop(client_key, None)
        return False
    return count >= MAX_FAILED_ATTEMPTS


def _clear_lockout(client_key: str) -> None:
    _lockout.pop(client_key, None)


class UsersStore:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.db_path = data_dir / "users.sqlite"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                create table if not exists users (
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
                create table if not exists sessions (
                    token_hash text primary key,
                    user_id text not null references users(id) on delete cascade,
                    created_at integer not null,
                    expires_at integer not null
                )
                """
            )

    def has_user(self) -> bool:
        with self._connect() as conn:
            row = conn.execute("select 1 from users where id = ?", (LOCAL_USER_ID,)).fetchone()
        return row is not None

    def create_user(self, password: str) -> dict[str, object]:
        now = int(time.time())
        with self._connect() as conn:
            if self.has_user():
                raise HTTPException(status_code=409, detail="Password already configured.")
            conn.execute(
                """
                insert into users (id, display_name, roles, password_hash, created_at, updated_at)
                values (?, ?, ?, ?, ?, ?)
                """,
                (
                    LOCAL_USER_ID,
                    LOCAL_DISPLAY_NAME,
                    ",".join(LOCAL_ROLES),
                    _hash_password(password),
                    now,
                    now,
                ),
            )
        return _claims()

    def load_password_hash(self) -> str | None:
        with self._connect() as conn:
            row = conn.execute(
                "select password_hash from users where id = ?", (LOCAL_USER_ID,)
            ).fetchone()
        return str(row["password_hash"]) if row else None

    def create_session(self, user_id: str) -> str:
        token = secrets.token_urlsafe(32)
        now = int(time.time())
        with self._connect() as conn:
            conn.execute(
                """
                insert into sessions (token_hash, user_id, created_at, expires_at)
                values (?, ?, ?, ?)
                """,
                (_hash_token(token), user_id, now, now + SESSION_TTL_SECONDS),
            )
        return token

    def delete_session(self, token: str | None) -> None:
        if not token:
            return
        with self._connect() as conn:
            conn.execute("delete from sessions where token_hash = ?", (_hash_token(token),))

    def session_claims(self, token: str | None) -> dict[str, object] | None:
        if not token:
            return None
        now = int(time.time())
        token_hash = _hash_token(token)
        with self._connect() as conn:
            conn.execute("delete from sessions where expires_at <= ?", (now,))
            row = conn.execute(
                """
                select u.id, u.display_name, u.roles
                from sessions s
                join users u on u.id = s.user_id
                where s.token_hash = ? and s.expires_at > ?
                """,
                (token_hash, now),
            ).fetchone()
        if row is None:
            return None
        return {
            "user_id": str(row["id"]),
            "display_name": str(row["display_name"]),
            "roles": [role for role in str(row["roles"]).split(",") if role],
        }


async def _password_from_request(request: Request) -> str:
    content_type = request.headers.get("content-type", "")
    raw = await request.body()
    if "application/json" in content_type:
        try:
            payload: Any = await request.json()
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid JSON.") from exc
        password = payload.get("password") if isinstance(payload, dict) else None
    else:
        fields = parse_qs(raw.decode("utf-8"))
        password = fields.get("password", [None])[0]
    if not isinstance(password, str) or not password:
        raise HTTPException(status_code=400, detail="Password is required.")
    return password


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        token,
        max_age=SESSION_TTL_SECONDS,
        path="/",
        httponly=True,
        secure=True,
        samesite="lax",
    )


def _delete_session_cookie(response: Response) -> None:
    response.delete_cookie(SESSION_COOKIE, path="/")


def _require_claims(store: UsersStore, request: Request) -> dict[str, object]:
    claims = store.session_claims(request.cookies.get(SESSION_COOKIE))
    if claims is None:
        raise HTTPException(status_code=401, detail="Not authenticated.")
    return claims


def create_app(data_dir: Path | str | None = None) -> FastAPI:
    app = FastAPI(title="Hearth Users", docs_url=None, redoc_url=None)
    store = UsersStore(Path(data_dir) if data_dir is not None else _default_data_dir())
    app.state.users_store = store

    @app.get("/health")
    async def health() -> dict[str, object]:
        return {"ok": True, "service": "hearth-users"}

    @app.post("/api/setup")
    async def setup(request: Request, response: Response) -> dict[str, object]:
        password = await _password_from_request(request)
        if len(password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters.")
        claims = store.create_user(password)
        token = store.create_session(LOCAL_USER_ID)
        _set_session_cookie(response, token)
        return claims

    @app.post("/login")
    async def login(request: Request, response: Response) -> dict[str, object]:
        client_key = _client_key(request)
        if _is_locked_out(client_key):
            raise HTTPException(status_code=429, detail="Too many failed attempts; try again later.")

        stored_hash = store.load_password_hash()
        if stored_hash is None:
            raise HTTPException(status_code=403, detail="No password configured.")

        password = await _password_from_request(request)
        if not _verify_password(password, stored_hash):
            _record_failed_attempt(client_key)
            raise HTTPException(status_code=401, detail="Invalid password.")

        _clear_lockout(client_key)
        token = store.create_session(LOCAL_USER_ID)
        _set_session_cookie(response, token)
        return _claims()

    @app.post("/logout")
    async def logout(request: Request, response: Response) -> dict[str, str]:
        store.delete_session(request.cookies.get(SESSION_COOKIE))
        _delete_session_cookie(response)
        return {"status": "ok"}

    @app.get("/api/session")
    async def session(request: Request) -> dict[str, object]:
        return _require_claims(store, request)

    @app.get("/api/verify")
    async def verify(request: Request) -> dict[str, object]:
        return _require_claims(store, request)

    @app.get("/login", response_class=HTMLResponse)
    async def login_page() -> str:
        return _placeholder_html()

    @app.get("/", response_class=HTMLResponse)
    async def index() -> str:
        return _placeholder_html()

    @app.get("/logout")
    async def logout_redirect(request: Request) -> RedirectResponse:
        response = RedirectResponse(url="/login", status_code=303)
        store.delete_session(request.cookies.get(SESSION_COOKIE))
        _delete_session_cookie(response)
        return response

    @app.get("/{_path:path}", response_class=HTMLResponse)
    async def spa_fallback(_path: str) -> str:
        return _placeholder_html()

    return app
