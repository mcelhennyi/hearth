"""FastAPI app for the built-in hearth-users plugin."""

from __future__ import annotations

import hashlib
import html
import json
import logging
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

SESSION_COOKIE = "hearth_session"
SESSION_TTL_SECONDS = 7 * 24 * 3600
LOCKOUT_WINDOW_SECONDS = 60
MAX_FAILED_ATTEMPTS = 5

LOCAL_USER_ID = "local"
LOCAL_DISPLAY_NAME = "Local user"
LOCAL_ROLES = ["admin", "user"]
PLUGIN_SLUG = "hearth-users"

log = logging.getLogger(__name__)

_password_hasher = PasswordHasher()
_lockout: dict[str, tuple[int, float]] = {}


def _default_data_dir() -> Path:
    configured = os.getenv("HEARTH_USERS_DATA_DIR")
    if configured:
        return Path(configured)
    return Path(os.getenv("HEARTH_VAR_DIR", "var/hearth")) / "plugins" / "hearth-users"


def _safe_next(next_url: str | None) -> str:
    if not next_url or not next_url.startswith("/") or next_url.startswith("//"):
        return "/"
    return next_url


def _auth_html(*, setup_required: bool, next_url: str = "/") -> str:
    mode = "setup" if setup_required else "login"
    title = "Create your Hearth admin" if setup_required else "Sign in to Hearth"
    intro = (
        "This local Hearth needs its first admin account before plugins can open."
        if setup_required
        else "Use your Hearth username and password to continue."
    )
    button = "Create admin" if setup_required else "Sign in"
    helper = (
        "Use at least 8 characters. This account is stored only on this Hearth."
        if setup_required
        else "This signs you into Hearth and all enabled plugins."
    )
    escaped_next = html.escape(_safe_next(next_url), quote=True)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Hearth Users</title>
    <style>
      :root {{
        --hearth-bg: #f7f5ef;
        --hearth-fg: #1f2933;
        --hearth-muted: #697386;
        --hearth-surface: #ffffff;
        --hearth-border: #d9ded8;
        --hearth-accent: #0f766e;
        --hearth-accent-strong: #115e59;
        color: var(--hearth-fg);
        background: var(--hearth-bg);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      * {{ box-sizing: border-box; }}
      body {{ margin: 0; }}
      main {{
        align-items: center;
        display: flex;
        min-height: 100svh;
        padding: 24px;
      }}
      section {{
        background: var(--hearth-surface);
        border: 1px solid var(--hearth-border);
        border-radius: 8px;
        box-shadow: 0 18px 50px rgb(31 41 51 / 10%);
        margin: 0 auto;
        max-width: 392px;
        padding: 28px;
        width: min(100%, 392px);
      }}
      .mark {{
        align-items: center;
        background: var(--hearth-fg);
        border-radius: 8px;
        color: var(--hearth-bg);
        display: inline-flex;
        font-size: 0.9rem;
        font-weight: 800;
        height: 34px;
        justify-content: center;
        letter-spacing: 0;
        width: 34px;
      }}
      .eyebrow {{
        color: var(--hearth-muted);
        font-size: 0.78rem;
        font-weight: 700;
        margin: 18px 0 8px;
        text-transform: uppercase;
      }}
      h1 {{
        font-size: 1.65rem;
        letter-spacing: 0;
        line-height: 1.15;
        margin: 0;
      }}
      p {{
        color: var(--hearth-muted);
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 10px 0 0;
      }}
      form {{
        display: grid;
        gap: 12px;
        margin-top: 22px;
      }}
      label {{
        color: var(--hearth-fg);
        font-size: 0.86rem;
        font-weight: 700;
      }}
      input {{
        border: 1px solid var(--hearth-border);
        border-radius: 6px;
        color: var(--hearth-fg);
        font: inherit;
        min-height: 44px;
        padding: 0 12px;
        width: 100%;
      }}
      input:focus {{
        border-color: var(--hearth-accent);
        box-shadow: 0 0 0 3px rgb(15 118 110 / 16%);
        outline: none;
      }}
      button {{
        background: var(--hearth-accent);
        border: 0;
        border-radius: 6px;
        color: #ffffff;
        cursor: pointer;
        font: inherit;
        font-weight: 800;
        min-height: 44px;
        padding: 0 16px;
      }}
      button:hover {{ background: var(--hearth-accent-strong); }}
      button:disabled {{ cursor: wait; opacity: 0.7; }}
      .message {{
        border-radius: 6px;
        display: none;
        font-size: 0.88rem;
        margin-top: 14px;
        padding: 10px 12px;
      }}
      .message[data-visible="true"] {{ display: block; }}
      .message[data-kind="error"] {{
        background: #fef2f2;
        color: #991b1b;
      }}
      .message[data-kind="ok"] {{
        background: #ecfdf5;
        color: #065f46;
      }}
      .helper {{ font-size: 0.84rem; }}
    </style>
  </head>
  <body>
    <main>
      <section>
        <span class="mark">H</span>
        <p class="eyebrow">Hearth Users</p>
        <h1>{html.escape(title)}</h1>
        <p>{html.escape(intro)}</p>
        <form id="auth-form" data-mode="{mode}" data-next="{escaped_next}">
          <label for="username">Username</label>
          <input
            id="username"
            name="username"
            type="text"
            autocomplete="username"
            required
            autofocus
          />
          <label for="display-name" data-setup-only>Display name</label>
          <input
            id="display-name"
            name="display_name"
            type="text"
            autocomplete="name"
            data-setup-only
          />
          <label for="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            minlength="8"
            autocomplete="current-password"
            required
          />
          <button type="submit">{html.escape(button)}</button>
        </form>
        <p class="helper">{html.escape(helper)}</p>
        <div id="message" class="message" role="status" aria-live="polite"></div>
      </section>
    </main>
    <script>
      const form = document.querySelector("#auth-form");
      const message = document.querySelector("#message");
      const username = document.querySelector("#username");
      const displayName = document.querySelector("#display-name");
      const password = document.querySelector("#password");
      const button = form.querySelector("button");
      const base = window.location.pathname.startsWith("/hearth-users") ? "/hearth-users" : "";
      const endpoint = form.dataset.mode === "setup" ? `${{base}}/api/setup` : `${{base}}/login`;
      if (form.dataset.mode !== "setup") {{
        document.querySelectorAll("[data-setup-only]").forEach((element) => element.remove());
      }}

      function showMessage(kind, text) {{
        message.dataset.kind = kind;
        message.dataset.visible = "true";
        message.textContent = text;
      }}

      form.addEventListener("submit", async (event) => {{
        event.preventDefault();
        button.disabled = true;
        showMessage("ok", form.dataset.mode === "setup" ? "Creating password..." : "Signing in...");
        try {{
          const response = await fetch(endpoint, {{
            method: "POST",
            credentials: "include",
            headers: {{ "content-type": "application/json" }},
            body: JSON.stringify({{
              username: username.value,
              display_name: displayName && displayName.isConnected ? displayName.value : undefined,
              password: password.value,
            }}),
          }});
          if (!response.ok) {{
            let detail = "Sign in failed.";
            try {{
              const payload = await response.json();
              if (payload && payload.detail) detail = payload.detail;
            }} catch (_error) {{}}
            throw new Error(detail);
          }}
          window.location.assign(form.dataset.next || "/");
        }} catch (error) {{
          showMessage("error", error instanceof Error ? error.message : "Sign in failed.");
          button.disabled = false;
          username.focus();
        }}
      }});
    </script>
  </body>
</html>"""

def _new_user_id() -> str:
    return f"user_{secrets.token_urlsafe(16)}"


def _normalize_username(username: str) -> str:
    return username.strip().lower()


def _parse_roles(roles: str) -> list[str]:
    return [role for role in roles.split(",") if role]


def _serialize_roles(roles: list[str]) -> str:
    return ",".join(dict.fromkeys(roles))


def _default_audit_log_path(data_dir: Path) -> Path:
    configured = os.getenv("HEARTH_USERS_AUDIT_LOG")
    if configured:
        return Path(configured)
    return data_dir / "auth-session.jsonl"


def _default_bootstrap_password_file() -> Path:
    configured = os.getenv("HEARTH_USERS_BOOTSTRAP_PASSWORD_FILE")
    if configured:
        return Path(configured)
    return (
        Path(os.getenv("HEARTH_VAR_DIR", "var/hearth"))
        / "secrets"
        / "hearth-users-default-password"
    )


def _write_audit_event(
    audit_log_path: Path,
    *,
    action: str,
    claims: dict[str, object] | None = None,
    topic: str | None = None,
    ok: bool = True,
) -> None:
    audit_log_path.parent.mkdir(parents=True, exist_ok=True)
    record: dict[str, object] = {
        "ts": time.time(),
        "plugin_slug": PLUGIN_SLUG,
        "action": action,
        "ok": ok,
    }
    if topic is not None:
        record["topic"] = topic
    if claims is not None:
        record["user_id"] = claims.get("user_id", "")
        record["roles"] = claims.get("roles", [])
    with audit_log_path.open("a", encoding="utf-8") as log:
        log.write(json.dumps(record, sort_keys=True) + "\n")


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
                    username text,
                    display_name text not null,
                    roles text not null,
                    disabled integer not null default 0,
                    password_hash text not null,
                    created_at integer not null,
                    updated_at integer not null,
                    last_login_at integer
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
            self._migrate_users(conn)

    def _migrate_users(self, conn: sqlite3.Connection) -> None:
        columns = {
            str(row["name"])
            for row in conn.execute("pragma table_info(users)").fetchall()
        }
        if "username" not in columns:
            conn.execute("alter table users add column username text")
        if "disabled" not in columns:
            conn.execute("alter table users add column disabled integer not null default 0")
        if "last_login_at" not in columns:
            conn.execute("alter table users add column last_login_at integer")

        now = int(time.time())
        conn.execute(
            """
            update users
            set username = lower(trim(id)),
                updated_at = ?
            where username is null or trim(username) = ''
            """,
            (now,),
        )
        conn.execute(
            """
            update users
            set roles = ?,
                display_name = case
                    when trim(display_name) = '' then ?
                    else display_name
                end,
                disabled = 0,
                updated_at = ?
            where id = ?
            """,
            (_serialize_roles(LOCAL_ROLES), LOCAL_DISPLAY_NAME, now, LOCAL_USER_ID),
        )
        conn.execute("create unique index if not exists users_username_unique on users(username)")

    def has_user(self) -> bool:
        with self._connect() as conn:
            row = conn.execute("select 1 from users limit 1").fetchone()
        return row is not None

    def create_user(
        self,
        *,
        username: str,
        display_name: str,
        password: str,
        roles: list[str],
        user_id: str | None = None,
    ) -> dict[str, object]:
        normalized_username = _normalize_username(username)
        display_name = display_name.strip()
        if not normalized_username:
            raise ValueError("Username is required.")
        if not display_name:
            raise ValueError("Display name is required.")
        now = int(time.time())
        user_id = user_id or _new_user_id()
        with self._connect() as conn:
            existing = conn.execute(
                "select 1 from users where username = ?", (normalized_username,)
            ).fetchone()
            if existing is not None:
                raise ValueError("Username already exists.")
            conn.execute(
                """
                insert into users (
                    id,
                    username,
                    display_name,
                    roles,
                    disabled,
                    password_hash,
                    created_at,
                    updated_at,
                    last_login_at
                )
                values (?, ?, ?, ?, 0, ?, ?, ?, null)
                """,
                (
                    user_id,
                    normalized_username,
                    display_name,
                    _serialize_roles(roles),
                    _hash_password(password),
                    now,
                    now,
                ),
            )
        return {
            "user_id": user_id,
            "display_name": display_name,
            "roles": list(dict.fromkeys(roles)),
        }

    def create_first_admin(
        self, username: str, display_name: str, password: str
    ) -> dict[str, object]:
        if self.has_user():
            raise HTTPException(status_code=409, detail="First admin already configured.")
        try:
            return self.create_user(
                username=username,
                display_name=display_name,
                password=password,
                roles=LOCAL_ROLES,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    def bootstrap_user_from_password_file(
        self, password_file: Path
    ) -> dict[str, object] | None:
        if self.has_user() or not password_file.exists():
            return None
        password = password_file.read_text(encoding="utf-8").strip()
        if len(password) < 8:
            log.warning(
                "hearth-users bootstrap password file ignored: must contain at least "
                "8 characters (%s)",
                password_file,
            )
            return None
        return self.create_user(
            user_id=LOCAL_USER_ID,
            username=LOCAL_USER_ID,
            display_name=LOCAL_DISPLAY_NAME,
            password=password,
            roles=LOCAL_ROLES,
        )

    def load_user_for_login(self, username: str) -> sqlite3.Row | None:
        normalized_username = _normalize_username(username)
        if not normalized_username:
            return None
        with self._connect() as conn:
            row = conn.execute(
                """
                select id, display_name, roles, disabled, password_hash
                from users
                where username = ?
                """,
                (normalized_username,),
            ).fetchone()
        return row

    def record_login(self, user_id: str) -> None:
        now = int(time.time())
        with self._connect() as conn:
            conn.execute(
                "update users set last_login_at = ?, updated_at = ? where id = ?",
                (now, now, user_id),
            )

    def set_user_disabled(self, user_id: str, disabled: bool) -> None:
        now = int(time.time())
        with self._connect() as conn:
            conn.execute(
                "update users set disabled = ?, updated_at = ? where id = ?",
                (1 if disabled else 0, now, user_id),
            )

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
                where s.token_hash = ? and s.expires_at > ? and u.disabled = 0
                """,
                (token_hash, now),
            ).fetchone()
        if row is None:
            return None
        return {
            "user_id": str(row["id"]),
            "display_name": str(row["display_name"]),
            "roles": _parse_roles(str(row["roles"])),
        }


async def _fields_from_request(request: Request) -> dict[str, str]:
    content_type = request.headers.get("content-type", "")
    raw = await request.body()
    if "application/json" in content_type:
        try:
            payload: Any = await request.json()
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid JSON.") from exc
        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="Invalid JSON.")
        fields = {
            key: value
            for key, value in payload.items()
            if isinstance(key, str) and isinstance(value, str)
        }
    else:
        parsed = parse_qs(raw.decode("utf-8"))
        fields = {
            key: values[0]
            for key, values in parsed.items()
            if values and isinstance(values[0], str)
        }
    return fields


async def _setup_fields_from_request(request: Request) -> tuple[str, str, str]:
    fields = await _fields_from_request(request)
    username = fields.get("username")
    display_name = fields.get("display_name")
    password = fields.get("password")
    if not isinstance(username, str) or not username.strip():
        raise HTTPException(status_code=400, detail="Username is required.")
    if not isinstance(display_name, str) or not display_name.strip():
        raise HTTPException(status_code=400, detail="Display name is required.")
    if not isinstance(password, str) or not password:
        raise HTTPException(status_code=400, detail="Password is required.")
    return username, display_name, password


async def _login_fields_from_request(request: Request) -> tuple[str, str]:
    fields = await _fields_from_request(request)
    username = fields.get("username")
    password = fields.get("password")
    if not isinstance(username, str) or not username.strip():
        raise HTTPException(status_code=400, detail="Username is required.")
    if not isinstance(password, str) or not password:
        raise HTTPException(status_code=400, detail="Password is required.")
    return username, password


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


def spark_session_current(store: UsersStore, params: dict[str, Any]) -> dict[str, object]:
    token = params.get("session_token")
    claims = store.session_claims(token if isinstance(token, str) else None)
    if claims is None:
        return {"authenticated": False}
    return {"authenticated": True, **claims}


def create_app(
    data_dir: Path | str | None = None,
    audit_log_path: Path | str | None = None,
    bootstrap_password_file: Path | str | None = None,
) -> FastAPI:
    app = FastAPI(title="Hearth Users", docs_url=None, redoc_url=None)
    store = UsersStore(Path(data_dir) if data_dir is not None else _default_data_dir())
    audit_path = (
        Path(audit_log_path)
        if audit_log_path is not None
        else _default_audit_log_path(store.data_dir)
    )
    bootstrap_path = (
        Path(bootstrap_password_file)
        if bootstrap_password_file is not None
        else _default_bootstrap_password_file()
    )
    bootstrapped_claims = store.bootstrap_user_from_password_file(bootstrap_path)
    if bootstrapped_claims is not None:
        _write_audit_event(audit_path, action="auth.bootstrap", claims=bootstrapped_claims)
    app.state.users_store = store
    app.state.audit_log_path = audit_path

    @app.get("/health")
    async def health() -> dict[str, object]:
        return {"ok": True, "service": "hearth-users"}

    @app.post("/api/setup")
    async def setup(request: Request, response: Response) -> dict[str, object]:
        username, display_name, password = await _setup_fields_from_request(request)
        if len(password) < 8:
            raise HTTPException(
                status_code=400, detail="Password must be at least 8 characters."
            )
        claims = store.create_first_admin(username, display_name, password)
        token = store.create_session(str(claims["user_id"]))
        _set_session_cookie(response, token)
        _write_audit_event(audit_path, action="auth.setup", claims=claims)
        return claims

    @app.post("/login")
    async def login(request: Request, response: Response) -> dict[str, object]:
        client_key = _client_key(request)
        if _is_locked_out(client_key):
            raise HTTPException(
                status_code=429, detail="Too many failed attempts; try again later."
            )

        username, password = await _login_fields_from_request(request)
        user = store.load_user_for_login(username)
        if user is None:
            if not store.has_user():
                raise HTTPException(status_code=403, detail="No password configured.")
            _record_failed_attempt(client_key)
            raise HTTPException(status_code=401, detail="Invalid username or password.")
        if int(user["disabled"]) != 0:
            raise HTTPException(status_code=403, detail="User is disabled.")

        stored_hash = str(user["password_hash"])
        if not stored_hash:
            raise HTTPException(status_code=403, detail="No password configured.")

        if not _verify_password(password, stored_hash):
            _record_failed_attempt(client_key)
            raise HTTPException(status_code=401, detail="Invalid username or password.")

        _clear_lockout(client_key)
        user_id = str(user["id"])
        token = store.create_session(user_id)
        _set_session_cookie(response, token)
        store.record_login(user_id)
        claims = {
            "user_id": user_id,
            "display_name": str(user["display_name"]),
            "roles": _parse_roles(str(user["roles"])),
        }
        _write_audit_event(
            audit_path,
            action="auth.login",
            claims=claims,
            topic="hearth-users.session.login",
        )
        return claims

    @app.post("/logout")
    async def logout(request: Request, response: Response) -> dict[str, str]:
        claims = store.session_claims(request.cookies.get(SESSION_COOKIE))
        store.delete_session(request.cookies.get(SESSION_COOKIE))
        _delete_session_cookie(response)
        _write_audit_event(
            audit_path,
            action="auth.logout",
            claims=claims,
            topic="hearth-users.session.logout",
        )
        return {"status": "ok"}

    @app.get("/api/session")
    async def session(request: Request) -> dict[str, object]:
        return _require_claims(store, request)

    @app.get("/api/verify")
    async def verify(request: Request) -> dict[str, object]:
        return _require_claims(store, request)

    @app.get("/login", response_class=HTMLResponse)
    async def login_page(request: Request) -> str:
        return _auth_html(
            setup_required=not store.has_user(),
            next_url=_safe_next(request.query_params.get("next")),
        )

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request) -> str:
        return _auth_html(
            setup_required=not store.has_user(),
            next_url=_safe_next(request.query_params.get("next")),
        )

    @app.get("/logout")
    async def logout_redirect(request: Request) -> RedirectResponse:
        response = RedirectResponse(url="/login", status_code=303)
        claims = store.session_claims(request.cookies.get(SESSION_COOKIE))
        store.delete_session(request.cookies.get(SESSION_COOKIE))
        _delete_session_cookie(response)
        _write_audit_event(
            audit_path,
            action="auth.logout",
            claims=claims,
            topic="hearth-users.session.logout",
        )
        return response

    @app.get("/{_path:path}", response_class=HTMLResponse)
    async def spa_fallback(_path: str, request: Request) -> str:
        return _auth_html(
            setup_required=not store.has_user(),
            next_url=_safe_next(request.query_params.get("next")),
        )

    return app
