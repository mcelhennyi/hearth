"""GET /api/settings, PUT /api/settings — hub-wide settings — T-FR-0001-02.

Default values (seeded on first GET if not present):
  theme                = "dark"
  hostname             = "hearth.home.arpa"
  notification_channel = "web-push"
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Setting
from app.schemas import SettingsResponse, SettingsUpdateRequest

router = APIRouter(prefix="/api/settings", tags=["settings"])

_DEFAULTS: dict[str, str] = {
    "theme": "dark",
    "hostname": "hearth.home.arpa",
    "notification_channel": "web-push",
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


@router.get("", response_model=SettingsResponse)
async def get_settings(session: AsyncSession = Depends(get_session)) -> SettingsResponse:
    rows = await _load_settings(session)
    return SettingsResponse(
        theme=rows["theme"],
        hostname=rows["hostname"],
        notification_channel=rows["notification_channel"],
    )


@router.put("", response_model=SettingsResponse)
async def update_settings(
    body: SettingsUpdateRequest,
    session: AsyncSession = Depends(get_session),
) -> SettingsResponse:
    rows = await _load_settings(session)
    updates = body.model_dump(exclude_none=True)
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
    return SettingsResponse(
        theme=rows["theme"],
        hostname=rows["hostname"],
        notification_channel=rows["notification_channel"],
    )
