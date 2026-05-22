"""Per-user preferences API — T-FR-0006-04.

GET  /api/user/preferences → theme and future toggles.
PUT  /api/user/preferences → merge body; 200.

Authority: docs/design/mantle-ui.md § Settings modal, § Theme persistence.

MVP single-user: rows keyed by user_id == "local".
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import models_user  # noqa: F401 — register table on Base.metadata
from app.db import get_session
from app.models_user import UserPreferences
from app.schemas_user import UserPreferencesResponse, UserPreferencesUpdateRequest

router = APIRouter(prefix="/api/user", tags=["user"])

_MVP_USER_ID = "local"
_DEFAULT_THEME = "system"


@router.get("/preferences", response_model=UserPreferencesResponse)
async def get_preferences(
    session: AsyncSession = Depends(get_session),
) -> UserPreferencesResponse:
    row = await session.get(UserPreferences, _MVP_USER_ID)
    if row is None:
        return UserPreferencesResponse(theme=_DEFAULT_THEME)
    return UserPreferencesResponse(theme=row.theme)  # type: ignore[arg-type]


@router.put("/preferences", response_model=UserPreferencesResponse)
async def put_preferences(
    body: UserPreferencesUpdateRequest,
    session: AsyncSession = Depends(get_session),
) -> UserPreferencesResponse:
    row = await session.get(UserPreferences, _MVP_USER_ID)
    if row is None:
        row = UserPreferences(user_id=_MVP_USER_ID, theme=_DEFAULT_THEME)
        session.add(row)

    if body.theme is not None:
        row.theme = body.theme

    await session.commit()
    await session.refresh(row)
    return UserPreferencesResponse(theme=row.theme)  # type: ignore[arg-type]
