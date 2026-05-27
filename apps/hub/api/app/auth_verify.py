"""Provider-backed auth verification and Hearth trust header signing."""

from __future__ import annotations

import hmac
import os
import secrets
import time
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

import httpx
from fastapi import Request


@dataclass(frozen=True)
class ProviderResult:
    status_code: int
    claims: dict[str, Any] | None


class ProviderUnavailable(RuntimeError):
    """Raised when auth provider output cannot be trusted."""


def builtin_verify_url() -> str:
    return os.getenv("HEARTH_BUILTIN_AUTH_VERIFY_URL", "http://hearth-users:8000/api/verify")


def user_sig_secret_path() -> Path:
    configured = os.getenv("HEARTH_USER_SIG_SECRET_PATH")
    if configured:
        return Path(configured)
    var_dir = Path(os.getenv("HEARTH_VAR_DIR", "/workspace/var/hearth"))
    return var_dir / "secrets" / "user-sig.key"


def load_or_create_user_sig_secret() -> str:
    configured = os.getenv("HEARTH_USER_SIG_SECRET")
    if configured:
        return configured

    path = user_sig_secret_path()
    if path.exists():
        secret = path.read_text(encoding="utf-8").strip()
        if secret:
            return secret

    secret = secrets.token_urlsafe(48)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(secret + "\n", encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return secret


def sign_user_request(*, secret: str, user_id: str, ts: str, method: str, path: str) -> str:
    payload = f"{user_id}\n{ts}\n{method}\n{path}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), payload, sha256).hexdigest()


def normalized_user_headers(claims: dict[str, Any], request: Request) -> dict[str, str]:
    user_id = _claim_text(claims, "user_id", "id", "sub")
    if not user_id:
        raise ProviderUnavailable("auth provider returned no user id")

    ts = str(int(time.time()))
    method = _original_method(request)
    path = _original_path(request)
    secret = load_or_create_user_sig_secret()
    headers = {
        "X-Hearth-User-Id": user_id,
        "X-Hearth-User-Ts": ts,
        "X-Hearth-User-Sig": sign_user_request(
            secret=secret,
            user_id=user_id,
            ts=ts,
            method=method,
            path=path,
        ),
    }

    display_name = _claim_text(claims, "display_name", "name")
    if display_name:
        headers["X-Hearth-User-Name"] = display_name

    roles = _roles_header(claims.get("roles"))
    if roles:
        headers["X-Hearth-Roles"] = roles

    return headers


async def fetch_provider_claims(url: str, request: Request) -> ProviderResult:
    headers = _forwarded_headers(request)
    async with httpx.AsyncClient(follow_redirects=False, timeout=5.0) as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 200:
        try:
            payload = response.json()
        except ValueError as exc:
            raise ProviderUnavailable("auth provider returned invalid JSON") from exc
        if not isinstance(payload, dict):
            raise ProviderUnavailable("auth provider returned non-object claims")
        return ProviderResult(status_code=200, claims=payload)

    return ProviderResult(status_code=response.status_code, claims=None)


def _forwarded_headers(request: Request) -> dict[str, str]:
    allowed = {
        "accept",
        "authorization",
        "cookie",
        "user-agent",
        "x-forwarded-for",
        "x-forwarded-host",
        "x-forwarded-method",
        "x-forwarded-proto",
        "x-forwarded-uri",
        "x-original-method",
        "x-original-uri",
    }
    return {key: value for key, value in request.headers.items() if key.lower() in allowed}


def _claim_text(claims: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = claims.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _roles_header(value: Any) -> str | None:
    if isinstance(value, str):
        return value or None
    if isinstance(value, list):
        roles = [item for item in value if isinstance(item, str) and item]
        return ",".join(roles) if roles else None
    return None


def _original_method(request: Request) -> str:
    value = request.headers.get("X-Forwarded-Method") or request.headers.get("X-Original-Method")
    return (value or request.method).upper()


def _original_path(request: Request) -> str:
    return (
        request.headers.get("X-Forwarded-Uri")
        or request.headers.get("X-Original-Uri")
        or request.url.path
    )
