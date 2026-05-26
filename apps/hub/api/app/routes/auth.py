"""Auth routes — login, logout, status, first-run password setup.

Authority: docs/design/plugin-contract.md (session/identity section)
"""

from __future__ import annotations

import os
from pathlib import Path

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app import auth_verify
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
from app.db import get_session
from app.models import Plugin
from app.routes.settings import _auth_settings, _load_settings

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


@router.get("/verify")
async def verify(request: Request, session: AsyncSession = Depends(get_session)) -> Response:
    rows = await _load_settings(session)
    auth_settings = _auth_settings(rows)
    if auth_settings.provider == "builtin":
        if not await _builtin_auth_provider_enabled(session):
            raise HTTPException(status_code=503, detail="Built-in auth provider is disabled.")
        provider_url = auth_verify.builtin_verify_url()
    else:
        provider_url = auth_settings.external_verify_url

    if not provider_url:
        raise HTTPException(status_code=503, detail="Auth provider is not configured.")

    try:
        provider = await auth_verify.fetch_provider_claims(provider_url, request)
        if provider.status_code in {401, 403}:
            raise HTTPException(status_code=provider.status_code, detail="Not authenticated.")
        if provider.status_code != 200 or provider.claims is None:
            raise HTTPException(status_code=503, detail="Auth provider unavailable.")
        headers = auth_verify.normalized_user_headers(provider.claims, request)
    except HTTPException:
        raise
    except (httpx.HTTPError, auth_verify.ProviderUnavailable) as exc:
        raise HTTPException(status_code=503, detail="Auth provider unavailable.") from exc

    return Response(status_code=200, headers=headers)


async def _builtin_auth_provider_enabled(session: AsyncSession) -> bool:
    plugin = await session.get(Plugin, "hearth-users")
    return plugin is None or plugin.state == "enabled"
