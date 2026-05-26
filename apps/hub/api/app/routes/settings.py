"""GET /api/settings, PUT /api/settings — hub-wide settings — T-FR-0001-02.

Default values (seeded on first GET if not present):
  theme                = "dark"
  hostname             = "hearth.home.arpa"
  notification_channel = "web-push"
  auth.provider        = "builtin"
  auth.external_verify_url = ""
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Setting
from app.schemas import AuthSettings, SettingsResponse, SettingsUpdateRequest

router = APIRouter(prefix="/api/settings", tags=["settings"])

_DEFAULTS: dict[str, str] = {
    "theme": "dark",
    "hostname": "hearth.home.arpa",
    "notification_channel": "web-push",
    "auth.provider": "builtin",
    "auth.external_verify_url": "",
}


async def _load_settings(session: AsyncSession) -> dict[str, str]:
    """Return the current settings map, seeding defaults if missing."""
    result = await session.execute(select(Setting))
    rows = {row.key: row.value for row in result.scalars().all()}
    seeded = False
    for key, default in _DEFAULTS.items():
        if key not in rows:
            session.add(Setting(key=key, value=default))
            rows[key] = default
            seeded = True
    if seeded:
        await session.commit()
    return rows


def _auth_settings(rows: dict[str, str]) -> AuthSettings:
    return AuthSettings(
        provider=rows["auth.provider"],  # type: ignore[arg-type]
        external_verify_url=rows["auth.external_verify_url"] or None,
    )


def _response_from_rows(rows: dict[str, str]) -> SettingsResponse:
    return SettingsResponse(
        theme=rows["theme"],
        hostname=rows["hostname"],
        notification_channel=rows["notification_channel"],
        auth=_auth_settings(rows),
    )


def _updates_from_body(body: SettingsUpdateRequest) -> dict[str, str]:
    updates: dict[str, str] = {}
    for key in ("theme", "hostname", "notification_channel"):
        value = getattr(body, key)
        if value is not None:
            updates[key] = value

    if body.auth is not None:
        auth_updates = body.auth.model_dump(exclude_unset=True)
        if "provider" in auth_updates and auth_updates["provider"] is not None:
            updates["auth.provider"] = auth_updates["provider"]
        if "external_verify_url" in auth_updates:
            updates["auth.external_verify_url"] = auth_updates["external_verify_url"] or ""

    return updates


@router.get("", response_model=SettingsResponse)
async def get_settings(session: AsyncSession = Depends(get_session)) -> SettingsResponse:
    rows = await _load_settings(session)
    return _response_from_rows(rows)


@router.put("", response_model=SettingsResponse)
async def update_settings(
    body: SettingsUpdateRequest,
    session: AsyncSession = Depends(get_session),
) -> SettingsResponse:
    rows = await _load_settings(session)
    updates = _updates_from_body(body)
    for key, value in updates.items():
        setting = await session.get(Setting, key)
        if setting is None:
            setting = Setting(key=key, value=value)
            session.add(setting)
        else:
            setting.value = value
        rows[key] = value
    if updates:
        await session.commit()
    return _response_from_rows(rows)
