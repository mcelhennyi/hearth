"""Tests for Docker host → /workspace plugin source path resolution."""

from __future__ import annotations

import os
from pathlib import Path

from app.plugin_paths import resolve_plugin_source_path


def test_host_repo_root_maps_to_workspace(monkeypatch: object, tmp_path: Path) -> None:
    host = tmp_path / "hearth"
    plugin = host / "apps" / "groceries"
    plugin.mkdir(parents=True)
    (plugin / "tinder.toml").write_text("", encoding="utf-8")

    monkeypatch.setenv("HEARTH_REPO_ROOT", str(host))
    got = resolve_plugin_source_path(str(plugin))
    assert got == Path("/workspace/apps/groceries")


def test_workspace_path_unchanged_when_exists(monkeypatch: object, tmp_path: Path) -> None:
    monkeypatch.delenv("HEARTH_REPO_ROOT", raising=False)
    ws = tmp_path / "workspace" / "apps" / "groceries"
    ws.mkdir(parents=True)
    (ws / "tinder.toml").write_text("", encoding="utf-8")

    # Patch workspace root for test (function uses /workspace constant)
    import app.plugin_paths as mod

    monkeypatch.setattr(mod, "_WORKSPACE_ROOT", tmp_path / "workspace")
    got = resolve_plugin_source_path("apps/groceries")
    assert got == tmp_path / "workspace" / "apps" / "groceries"


def test_unrelated_host_path_not_rewritten(monkeypatch: object) -> None:
    monkeypatch.setenv("HEARTH_REPO_ROOT", "/home/pi/hearth")
    got = resolve_plugin_source_path("/opt/other/plugin")
    assert got == Path("/opt/other/plugin")
