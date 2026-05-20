"""Plugin registry CRUD routes — T-FR-0001-02.

Stubs: install/enable/disable/uninstall mutate DB state only; no supervisor
calls yet (those land in T-FR-0001-03 Tinder loader).

MVP policy (plugin-contract.md): kind=widget enable returns 501.
"""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import AuditLog, Plugin
from app.schemas import PluginInstallRequest, PluginResponse

router = APIRouter(prefix="/api/plugins", tags=["plugins"])


@router.get("", response_model=list[PluginResponse])
async def list_plugins(session: AsyncSession = Depends(get_session)) -> list[Plugin]:
    result = await session.execute(select(Plugin))
    return list(result.scalars().all())


@router.post("/install", response_model=PluginResponse)
async def install_plugin(
    body: PluginInstallRequest,
    session: AsyncSession = Depends(get_session),
) -> Plugin:
    existing = await session.get(Plugin, body.slug)
    if existing is not None:
        raise HTTPException(status_code=409, detail=f"Plugin '{body.slug}' is already installed.")

    plugin = Plugin(
        slug=body.slug,
        name=body.name,
        version=body.version,
        kind=body.kind,
        state="disabled",
        installed_at=datetime.now(UTC),
    )
    session.add(plugin)
    session.add(AuditLog(action="install", plugin_slug=body.slug))
    await session.commit()
    await session.refresh(plugin)
    return plugin


@router.post("/{slug}/enable", response_model=PluginResponse)
async def enable_plugin(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> Plugin:
    plugin = await session.get(Plugin, slug)
    if plugin is None:
        raise HTTPException(status_code=404, detail=f"Plugin '{slug}' not found.")

    # MVP policy: widget enable is not yet supported (plugin-contract.md §Plugin kind)
    if plugin.kind == "widget":
        raise HTTPException(
            status_code=501,
            detail="Widget plugins cannot be enabled in MVP. See docs/design/plugin-contract.md.",
        )

    plugin.state = "enabled"
    session.add(AuditLog(action="enable", plugin_slug=slug))
    await session.commit()
    await session.refresh(plugin)
    return plugin


@router.post("/{slug}/disable", response_model=PluginResponse)
async def disable_plugin(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> Plugin:
    plugin = await session.get(Plugin, slug)
    if plugin is None:
        raise HTTPException(status_code=404, detail=f"Plugin '{slug}' not found.")

    plugin.state = "disabled"
    session.add(AuditLog(action="disable", plugin_slug=slug))
    await session.commit()
    await session.refresh(plugin)
    return plugin


@router.post("/{slug}/uninstall", response_model=PluginResponse)
async def uninstall_plugin(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> Plugin:
    plugin = await session.get(Plugin, slug)
    if plugin is None:
        raise HTTPException(status_code=404, detail=f"Plugin '{slug}' not found.")

    plugin.state = "uninstalled"
    session.add(AuditLog(action="uninstall", plugin_slug=slug))
    await session.commit()
    await session.refresh(plugin)
    return plugin
