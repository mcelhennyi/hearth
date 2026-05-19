"""Contract tests for the Hearth-side Kindling plugin template mirror (T-FR-0003-10)."""

from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path

import pytest
from hearth_kindling_contract import KindlingTemplateError, render_plugin_template


def _is_executable(path: Path) -> bool:
    return bool(path.stat().st_mode & stat.S_IXUSR)


def test_render_plugin_template_creates_plugin_executable_and_install_hook(
    tmp_path: Path,
) -> None:
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")

    assert plugin_root == tmp_path / "sample-plugin"
    assert (plugin_root / "tinder.toml").read_text(encoding="utf-8").startswith(
        '[plugin]\nslug = "sample-plugin"'
    )
    assert _is_executable(plugin_root / "plugin")
    assert _is_executable(plugin_root / "scripts" / "install")
    assert (plugin_root / "sample_plugin" / "admin.py").is_file()


def test_rendered_plugin_help_works_without_hearth_layout(tmp_path: Path) -> None:
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")

    proc = subprocess.run(
        [str(plugin_root / "plugin"), "--help"],
        cwd=plugin_root,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "sample-plugin" in proc.stdout


def test_rendered_plugin_ops_fail_without_registry(tmp_path: Path) -> None:
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")
    proc = subprocess.run(
        [str(plugin_root / "plugin"), "--disable"],
        cwd=plugin_root,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1
    assert "hearth/plugins" in proc.stderr or "registered" in proc.stderr


def test_rendered_plugin_passthrough_with_hearth_layout(tmp_path: Path) -> None:
    from test_plugin_executable import _layout_with_plugin

    _root, plugin_exe = _layout_with_plugin(tmp_path)
    proc = subprocess.run(
        [str(plugin_exe), "--", "doctor"],
        cwd=tmp_path / "hearth" / "plugins" / "sample-plugin",
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "admin passthrough: doctor" in proc.stdout


def test_rendered_plugin_exit_errors_without_enter_session(tmp_path: Path) -> None:
    import hearth_install

    pkg_parent = str(Path(hearth_install.__file__).resolve().parents[1])
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")
    env = os.environ.copy()
    env["PYTHONPATH"] = pkg_parent
    completed = subprocess.run(
        [str(plugin_root / "plugin"), "--exit"],
        cwd=plugin_root,
        env=env,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 1
    assert "not inside" in completed.stderr


def test_rendered_install_hook_delegates_to_admin_install(tmp_path: Path) -> None:
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")
    env = os.environ.copy()
    env["HEARTH_PLUGIN_DIR"] = str(plugin_root)

    installed = subprocess.run(
        [str(plugin_root / "scripts" / "install"), "--dry-run"],
        check=True,
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert "sample-plugin admin install hook: --dry-run" in installed.stdout


def test_render_plugin_template_rejects_invalid_slug(tmp_path: Path) -> None:
    with pytest.raises(KindlingTemplateError):
        render_plugin_template(tmp_path, slug="Bad_Plugin")
