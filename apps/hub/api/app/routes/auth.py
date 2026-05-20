"""Auth routes — login, logout, status, first-run password setup.

Authority: docs/design/plugin-contract.md (session/identity section)
"""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel

from app.auth import (
    SESSION_COOKIE,
    SESSION_TTL_SECONDS,
    clear_lockout,
    create_session_token,
    hash_password,
    is_locked_out,
    load_password_hash,
    record_failed_attempt,
    save_password_hash,
    verify_password,
    verify_session_token,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

DEFAULT_VAR_DIR = Path(os.getenv("HEARTH_VAR_DIR", "var/hearth"))


def _password_hash_path() -> Path:
    return Path(
        os.getenv("HEARTH_PASSWORD_HASH_PATH", str(DEFAULT_VAR_DIR / "secrets" / "password.hash"))
    )


class LoginRequest(BaseModel):
    password: str


class SetupRequest(BaseModel):
    password: str


@router.post("/login")
def login(body: LoginRequest, request: Request, response: Response) -> dict[str, str]:
    client_key = request.client.host if request.client else "unknown"
    if is_locked_out(client_key):
        raise HTTPException(status_code=429, detail="Too many failed attempts; try again later.")

    stored_hash = load_password_hash(_password_hash_path())
    if stored_hash is None:
        raise HTTPException(status_code=403, detail="No password configured. Use /api/auth/setup.")

    if not verify_password(body.password, stored_hash):
        record_failed_attempt(client_key)
        raise HTTPException(status_code=401, detail="Invalid password.")

    clear_lockout(client_key)
    token = create_session_token()
    response.set_cookie(
        SESSION_COOKIE,
        token,
        max_age=SESSION_TTL_SECONDS,
        httponly=True,
        samesite="lax",
        secure=True,
    )
    return {"status": "ok"}


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    response.delete_cookie(SESSION_COOKIE)
    return {"status": "ok"}


@router.get("/status")
def status(request: Request) -> dict[str, bool]:
    token = request.cookies.get(SESSION_COOKIE)
    authenticated = bool(token and verify_session_token(token))
    return {"authenticated": authenticated}


@router.post("/setup")
def setup(body: SetupRequest) -> dict[str, str]:
    """Set the initial password. Only works when no password is configured."""
    path = _password_hash_path()
    if load_password_hash(path) is not None:
        raise HTTPException(status_code=409, detail="Password already configured.")
    if not body.password or len(body.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters.")
    save_password_hash(path, hash_password(body.password))
    return {"status": "ok"}
