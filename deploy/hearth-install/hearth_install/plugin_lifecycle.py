"""@HRT-OPS-002 Registry + tree updates for per-plugin lifecycle (T-FR-0003-11)."""

from __future__ import annotations

import shutil
from dataclasses import replace
from pathlib import Path

from hearth_install.plugin_compose import (
    PluginRecord,
    PluginRegistryError,
    generate_plugin_compose,
    load_plugin_registry,
    save_plugin_registry,
)


class PluginLifecycleError(RuntimeError):
    """User-facing lifecycle failure."""


def set_plugin_enabled(heart: Path, slug: str, *, enabled: bool) -> None:
    """Flip ``enabled`` for one plugin row and regenerate compose."""

    heart = heart.resolve()
    rows = load_plugin_registry(heart)
    new_rows: list[PluginRecord] = []
    found = False
    for record in rows:
        if record.slug == slug:
            found = True
            new_rows.append(replace(record, enabled=enabled))
        else:
            new_rows.append(record)
    if not found:
        msg = f"plugin {slug!r} is not listed in {heart / 'state' / 'plugins.yaml'}"
        raise PluginLifecycleError(msg)
    save_plugin_registry(heart, new_rows)
    try:
        generate_plugin_compose(heart)
    except PluginRegistryError as exc:
        raise PluginLifecycleError(str(exc)) from exc


def remove_plugin_from_install(heart: Path, slug: str) -> None:
    """Remove registry row, delete plugin tree, regenerate compose."""

    heart = heart.resolve()
    rows = load_plugin_registry(heart)
    if not any(r.slug == slug for r in rows):
        msg = f"plugin {slug!r} is not in the registry"
        raise PluginLifecycleError(msg)
    new_rows = [r for r in rows if r.slug != slug]
    save_plugin_registry(heart, new_rows)

    plugin_dir = heart / "plugins" / slug
    if plugin_dir.is_dir():
        shutil.rmtree(plugin_dir)

    var_plugin = heart / "var" / "plugins" / slug
    if var_plugin.is_dir():
        shutil.rmtree(var_plugin)

    try:
        generate_plugin_compose(heart)
    except PluginRegistryError as exc:
        raise PluginLifecycleError(str(exc)) from exc
