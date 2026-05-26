"""Hearth trust-header helpers for generated {{ plugin_name }} routes."""

from __future__ import annotations

import hmac
import os
import time
from dataclasses import dataclass
from hashlib import sha256

from fastapi import HTTPException, Request

MAX_TRUST_HEADER_AGE_SECONDS = 60


@dataclass(frozen=True)
class HearthUser:
    id: str
    name: str | None = None
    roles: tuple[str, ...] = ()


def require_hearth_user(request: Request) -> HearthUser:
    """FastAPI dependency that validates Hearth's signed gateway user headers."""
    user_id = request.headers.get("X-Hearth-User-Id")
    ts = request.headers.get("X-Hearth-User-Ts")
    sig = request.headers.get("X-Hearth-User-Sig")
    if not user_id or not ts or not sig:
        raise HTTPException(status_code=401, detail="missing Hearth user headers")

    try:
        ts_int = int(ts)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="invalid Hearth user timestamp") from exc

    if abs(int(time.time()) - ts_int) > MAX_TRUST_HEADER_AGE_SECONDS:
        raise HTTPException(status_code=401, detail="stale Hearth user headers")

    secret = os.getenv("HEARTH_USER_SIG_SECRET")
    if not secret:
        raise HTTPException(status_code=503, detail="Hearth user trust secret is not configured")

    expected = _sign_user_request(
        secret=secret,
        user_id=user_id,
        ts=ts,
        method=_original_method(request),
        path=_original_path(request),
    )
    if not hmac.compare_digest(expected, sig):
        raise HTTPException(status_code=401, detail="invalid Hearth user signature")

    return HearthUser(
        id=user_id,
        name=request.headers.get("X-Hearth-User-Name"),
        roles=_roles(request.headers.get("X-Hearth-Roles")),
    )


def _sign_user_request(*, secret: str, user_id: str, ts: str, method: str, path: str) -> str:
    payload = f"{user_id}\n{ts}\n{method.upper()}\n{path}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), payload, sha256).hexdigest()


def _original_method(request: Request) -> str:
    value = request.headers.get("X-Forwarded-Method") or request.headers.get("X-Original-Method")
    return (value or request.method).upper()


def _original_path(request: Request) -> str:
    return (
        request.headers.get("X-Forwarded-Uri")
        or request.headers.get("X-Original-Uri")
        or request.url.path
    )


def _roles(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(role.strip() for role in value.split(",") if role.strip())
