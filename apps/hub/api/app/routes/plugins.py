"""Plugin registry CRUD routes — T-FR-0001-02/03/05.

install: calls Tinder loader when *source* is given; stubs for enable/disable/uninstall
mutate DB state only (no supervisor calls yet).

MVP policy (plugin-contract.md): kind=widget enable returns 501.

Caddy fragment regeneration (T-FR-0001-05): after every state-changing operation
(install, enable, disable, uninstall), regenerate_and_reload() is called to write
a new Caddyfile fragment and signal Caddy to reload.  Errors from the reload are
logged but do not fail the API response.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from app.plugin_paths import resolve_plugin_source_path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import AuditLog, Plugin
from app.schemas import PluginInstallRequest, PluginInstallResponse, PluginResponse
from proxy.caddy import regenerate_and_reload
from tinder.loader import load_tinder

router = APIRouter(prefix="/api/plugins", tags=["plugins"])


@router.get("", response_model=list[PluginResponse])
async def list_plugins(session: AsyncSession = Depends(get_session)) -> list[Plugin]:
    result = await session.execute(select(Plugin))
    return list(result.scalars().all())


@router.post("/install", response_model=PluginInstallResponse)
async def install_plugin(
    body: PluginInstallRequest,
    session: AsyncSession = Depends(get_session),
) -> PluginInstallResponse:
    validation_errors: list[str] = []
    slug = body.slug
    name = body.name
    version = body.version
    kind = body.kind

    if body.source is not None:
        manifest, errors = load_tinder(resolve_plugin_source_path(body.source))
        if errors:
            # Per plugin-contract.md: tinder.toml invalid → install disabled, surface errors
            validation_errors = errors
            if manifest is None:
                # No manifest at all — still need slug/name/version from body or return 422
                if not body.slug or not body.name or not body.version:
                    raise HTTPException(
                        status_code=422,
                        detail={"validation_errors": errors, "message": "tinder.toml invalid"},
                    )
        else:
            assert manifest is not None
            slug = manifest.plugin.slug
            name = manifest.plugin.name
            version = manifest.plugin.version
            kind = manifest.plugin.kind  # type: ignore[assignment]

    if not slug or not name or not version:
        raise HTTPException(
            status_code=422,
            detail="slug, name, and version are required when source is not provided",
        )

    existing = await session.get(Plugin, slug)
    if existing is not None:
        raise HTTPException(status_code=409, detail=f"Plugin '{slug}' is already installed.")

    plugin = Plugin(
        slug=slug,
        name=name,
        version=version,
        kind=kind,
        state="disabled",
        installed_at=datetime.now(UTC),
    )
    session.add(plugin)
    session.add(AuditLog(action="install", plugin_slug=slug))
    await session.commit()
    await session.refresh(plugin)
    await regenerate_and_reload(session)
    return PluginInstallResponse(
        slug=plugin.slug,
        name=plugin.name,
        version=plugin.version,
        kind=plugin.kind,
        state=plugin.state,
        installed_at=plugin.installed_at,
        validation_errors=validation_errors,
    )


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
    await regenerate_and_reload(session)
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
    await regenerate_and_reload(session)
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
    await regenerate_and_reload(session)
    return plugin
