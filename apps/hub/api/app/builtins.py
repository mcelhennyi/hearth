"""Built-in platform plugin registration for Hearth."""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AuditLog, Plugin
from tinder.loader import load_tinder

log = logging.getLogger(__name__)

DEFAULT_BUILTIN_ROOT = Path(os.getenv("HEARTH_BUILTIN_ROOT", "/workspace/apps/builtin"))


async def register_builtin_plugins(
    session: AsyncSession,
    *,
    builtin_root: Path = DEFAULT_BUILTIN_ROOT,
) -> list[str]:
    """Register built-in Tinder plugins found under ``apps/builtin``.

    Built-ins are platform services, not normal external plugins under ``apps/<slug>``.
    New rows are enabled immediately so the dev gateway can route them on first boot.
    """
    registered: list[str] = []
    if not builtin_root.exists():
        log.info("built-in plugin root not found: %s", builtin_root)
        return registered

    for plugin_dir in sorted(p for p in builtin_root.iterdir() if p.is_dir()):
        manifest, errors = load_tinder(plugin_dir)
        if errors:
            log.warning("skipping built-in plugin at %s: %s", plugin_dir, "; ".join(errors))
            continue
        assert manifest is not None
        if not manifest.plugin.builtin:
            log.warning("skipping %s: manifest is not marked builtin", plugin_dir)
            continue

        existing = await session.get(Plugin, manifest.plugin.slug)
        if existing is None:
            plugin = Plugin(
                slug=manifest.plugin.slug,
                name=manifest.plugin.name,
                version=manifest.plugin.version,
                kind=manifest.plugin.kind,
                state="enabled",
                builtin=True,
                installed_at=datetime.now(UTC),
            )
            session.add(plugin)
            session.add(AuditLog(action="builtin-register", plugin_slug=manifest.plugin.slug))
        else:
            changed = False
            for attr, value in (
                ("name", manifest.plugin.name),
                ("version", manifest.plugin.version),
                ("kind", manifest.plugin.kind),
                ("builtin", True),
            ):
                if getattr(existing, attr) != value:
                    setattr(existing, attr, value)
                    changed = True
            if existing.state == "uninstalled":
                existing.state = "enabled"
                changed = True
            if changed:
                session.add(existing)
                session.add(AuditLog(action="builtin-refresh", plugin_slug=manifest.plugin.slug))
        registered.append(manifest.plugin.slug)

    await session.commit()
    return registered
