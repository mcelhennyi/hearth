"""T-FR-0003-11: per-plugin ``plugin`` executable (lifecycle + passthrough)."""

from __future__ import annotations

import os
import subprocess
import textwrap
from pathlib import Path

import pytest

from hearth_install.layout import ensure_hearth_layout
from hearth_install.plugin_compose import PluginRecord, generate_plugin_compose, save_plugin_registry
from hearth_kindling_contract import render_plugin_template

_MIN_TINDER = textwrap.dedent(
    """\
    [plugin]
    slug = "sample-plugin"
    name = "Sample"
    version = "0.1.0"
    hearth_min = "0.1.0"
    description = "fixture"

    [entrypoint]
    backend = { kind = "none" }
    ui = { kind = "static", path = "web/dist" }
    """,
)


def _layout_with_plugin(tmp_path: Path) -> tuple[Path, Path]:
    """Returns ``(install_root, plugin_executable)``."""

    ensure_hearth_layout(tmp_path, hearth_ref="plugin-exe-test")
    plugins_parent = tmp_path / "hearth" / "plugins"
    render_plugin_template(plugins_parent, slug="sample-plugin")
    (tmp_path / "hearth" / "compose" / "docker-compose.yml").write_text(
        textwrap.dedent(
            """\
            services:
              hub:
                image: alpine:3.20
                command: ["sleep", "infinity"]
            """,
        ),
        encoding="utf-8",
    )
    plugin_root = plugins_parent / "sample-plugin"
    (plugin_root / "tinder.toml").write_text(_MIN_TINDER, encoding="utf-8")

    save_plugin_registry(
        tmp_path / "hearth",
        [
            PluginRecord(
                slug="sample-plugin",
                source_git="https://example.test/plugin.git",
                enabled=True,
            ),
        ],
    )
    generate_plugin_compose(tmp_path / "hearth")
    return tmp_path, plugin_root / "plugin"


def test_plugin_help_succeeds(tmp_path: Path) -> None:
    _root, plugin_exe = _layout_with_plugin(tmp_path)
    proc = subprocess.run(
        [str(plugin_exe), "--help"],
        cwd=tmp_path / "hearth" / "plugins" / "sample-plugin",
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "sample-plugin" in proc.stdout


@pytest.mark.parametrize(
    "flag",
    [
        "--update",
        "--enable",
        "--disable",
        "--start",
        "--stop",
        "--reset",
        "--exit",
    ],
)
def test_plugin_flags_invoke_without_crash_when_docker_stubbed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    flag: str,
) -> None:
    """Smoke: each lifecycle flag is accepted (docker / update stubbed in-process)."""

    from hearth_plugin_cli.cli import run_plugin_cli

    _root, _exe = _layout_with_plugin(tmp_path)
    plugin_root = tmp_path / "hearth" / "plugins" / "sample-plugin"

    monkeypatch.setattr(
        "hearth_plugin_cli.cli.subprocess.run",
        lambda *a, **k: type("P", (), {"returncode": 0})(),
    )
    monkeypatch.setattr("hearth_cli.update_cmd.run_update", lambda *a, **k: 0)

    extra: list[str] = []
    env = dict(os.environ)
    if flag == "--reset":
        extra.append("--yes")
    if flag == "--exit":
        env["HEARTH_PLUGIN_ENTER_FROM"] = str(tmp_path.resolve())

    code = run_plugin_cli(plugin_root, [flag, *extra], env=env)
    assert code == 0


def test_plugin_disable_updates_generated_compose(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from hearth_plugin_cli.cli import run_plugin_cli

    _root, _plugin_exe = _layout_with_plugin(tmp_path)
    hearth = tmp_path / "hearth"
    plugin_root = hearth / "plugins" / "sample-plugin"
    gen = hearth / "compose" / "overrides" / "generated.plugins.yml"
    assert "sample-plugin:" in gen.read_text(encoding="utf-8")

    monkeypatch.setattr(
        "hearth_plugin_cli.cli.subprocess.run",
        lambda *a, **k: type("P", (), {"returncode": 0})(),
    )

    assert run_plugin_cli(plugin_root, ["--disable"]) == 0
    text = gen.read_text(encoding="utf-8")
    assert "sample-plugin:" not in text


def test_plugin_disable_then_enable_roundtrip(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """VAL: disable removes service from generated override; enable restores."""

    from hearth_plugin_cli.cli import run_plugin_cli

    _root, _plugin_exe = _layout_with_plugin(tmp_path)
    hearth = tmp_path / "hearth"
    plugin_root = hearth / "plugins" / "sample-plugin"
    gen = hearth / "compose" / "overrides" / "generated.plugins.yml"

    monkeypatch.setattr(
        "hearth_plugin_cli.cli.subprocess.run",
        lambda *a, **k: type("P", (), {"returncode": 0})(),
    )

    assert run_plugin_cli(plugin_root, ["--disable"]) == 0
    assert "sample-plugin:" not in gen.read_text(encoding="utf-8")

    assert run_plugin_cli(plugin_root, ["--enable"]) == 0
    assert "sample-plugin:" in gen.read_text(encoding="utf-8")


def test_plugin_passthrough_admin(tmp_path: Path) -> None:
    _root, plugin_exe = _layout_with_plugin(tmp_path)
    proc = subprocess.run(
        [str(plugin_exe), "--", "hello", "world"],
        cwd=tmp_path / "hearth" / "plugins" / "sample-plugin",
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "admin passthrough: hello world" in proc.stdout


def test_plugin_exit_emits_cd(tmp_path: Path) -> None:
    _root, plugin_exe = _layout_with_plugin(tmp_path)
    back = tmp_path / "hearth"
    env = {**os.environ, "HEARTH_PLUGIN_ENTER_FROM": str(back)}
    proc = subprocess.run(
        [str(plugin_exe), "--exit"],
        cwd=tmp_path / "hearth" / "plugins" / "sample-plugin",
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert proc.stdout.strip().startswith("cd ")
    assert str(back.resolve()) in proc.stdout


def test_plugin_remove_requires_confirmation_flag(tmp_path: Path) -> None:
    _root, plugin_exe = _layout_with_plugin(tmp_path)
    proc = subprocess.run(
        [str(plugin_exe), "--remove"],
        cwd=tmp_path / "hearth" / "plugins" / "sample-plugin",
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2


def test_plugin_remove_with_yes_deletes_tree(
    tmp_path: Path,
) -> None:
    _root, plugin_exe = _layout_with_plugin(tmp_path)
    plug = tmp_path / "hearth" / "plugins" / "sample-plugin"
    proc = subprocess.run(
        [str(plugin_exe), "--remove", "--yes"],
        cwd=plug,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert not plug.exists()


def test_plugin_reset_clears_var_data(tmp_path: Path) -> None:
    _root, plugin_exe = _layout_with_plugin(tmp_path)
    hearth = tmp_path / "hearth"
    data = hearth / "var" / "plugins" / "sample-plugin"
    data.mkdir(parents=True, exist_ok=True)
    (data / "x").write_text("y", encoding="utf-8")

    proc = subprocess.run(
        [str(plugin_exe), "--reset", "--yes"],
        cwd=hearth / "plugins" / "sample-plugin",
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert not data.exists()
