"""Single-user auth for Hearth hub.

Authority: docs/design/plugin-contract.md (session/identity section)

Contract:
  - One password hash file at var/hearth/secrets/password.hash (argon2id).
  - Sessions are signed cookies using itsdangerous; secret key in var/hearth/secrets/session.key.
  - Lockout: 5 consecutive bad-password attempts → 60s lockout (in-process counter).
  - Session TTL: 7 days.
"""

from __future__ import annotations

import os
import secrets
import time
from pathlib import Path

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from fastapi import Cookie, HTTPException
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

_ph = PasswordHasher()

SESSION_TTL_SECONDS = 7 * 24 * 3600
LOCKOUT_WINDOW_SECONDS = 60
MAX_FAILED_ATTEMPTS = 5

# in-process lockout tracker: {client_ip: (fail_count, first_fail_ts)}
_lockout: dict[str, tuple[int, float]] = {}


def hash_password(plain: str) -> str:
    return _ph.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return _ph.verify(hashed, plain)
    except (VerifyMismatchError, InvalidHashError):
        return False


def load_password_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip() or None


def save_password_hash(path: Path, hashed: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(hashed + "\n", encoding="utf-8")


def _load_or_create_session_key(path: Path) -> str:
    if path.exists():
        key = path.read_text(encoding="utf-8").strip()
        if key:
            return key
    key = secrets.token_hex(32)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(key + "\n", encoding="utf-8")
    return key


def _get_serializer() -> URLSafeTimedSerializer:
    key_path = Path(os.getenv("HEARTH_SESSION_KEY_PATH", "var/hearth/secrets/session.key"))
    return URLSafeTimedSerializer(_load_or_create_session_key(key_path))


def create_session_token() -> str:
    return _get_serializer().dumps("authenticated")


def verify_session_token(token: str) -> bool:
    try:
        _get_serializer().loads(token, max_age=SESSION_TTL_SECONDS)
        return True
    except (SignatureExpired, BadSignature):
        return False


def record_failed_attempt(client_key: str) -> None:
    now = time.time()
    count, first_ts = _lockout.get(client_key, (0, now))
    if now - first_ts > LOCKOUT_WINDOW_SECONDS:
        count, first_ts = 0, now
    _lockout[client_key] = (count + 1, first_ts)


def is_locked_out(client_key: str) -> bool:
    count, first_ts = _lockout.get(client_key, (0, 0.0))
    if time.time() - first_ts > LOCKOUT_WINDOW_SECONDS:
        _lockout.pop(client_key, None)
        return False
    return count >= MAX_FAILED_ATTEMPTS


def clear_lockout(client_key: str) -> None:
    _lockout.pop(client_key, None)


SESSION_COOKIE = "hearth_session"


def require_user(hearth_session: str | None = Cookie(default=None)) -> str:
    """FastAPI dependency — raises 401 if session cookie is absent or invalid."""
    if hearth_session is None or not verify_session_token(hearth_session):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return "user"


def optional_user(hearth_session: str | None = Cookie(default=None)) -> str | None:
    """Like require_user but returns None instead of raising."""
    if hearth_session and verify_session_token(hearth_session):
        return "user"
    return None
