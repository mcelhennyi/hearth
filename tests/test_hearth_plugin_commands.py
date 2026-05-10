"""T-FR-0003-07: ``hearth --plugin`` commands and plugin add orchestration."""

from __future__ import annotations

import os
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest
from hearth_cli import cli
from hearth_install.layout import ensure_heart_layout
from hearth_install.plugin_add import PluginAddError, add_plugin_from_source, classify_plugin_source
from hearth_install.plugin_compose import (
    PluginRecord,
    generate_plugin_compose,
    load_plugin_registry,
    save_plugin_registry,
)
from hearth_install.plugin_session import FROM_ENV, STACK_ENV

MINIMAL_TINDER = textwrap.dedent(
    """\
    [plugin]
    slug = "fixture-one"
    name = "Fixture One"
    version = "0.1.0"
    hearth_min = "0.1.0"
    description = "fixture plugin"

    [entrypoint]
    backend = { kind = "none" }
    ui = { kind = "static", path = "web/dist" }
    """,
)


def test_classify_rejects_oci_and_registry_shortcuts() -> None:
    with pytest.raises(PluginAddError, match="not implemented"):
        classify_plugin_source("oci://registry.example/plugin:v1")
    with pytest.raises(PluginAddError, match="relay"):
        classify_plugin_source("just-a-name")


def test_add_plugin_from_local_path_updates_registry_and_compose(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "hearth_install.plugin_add._maybe_start_plugin_services",
        lambda *args, **kwargs: None,
    )

    ensure_heart_layout(tmp_path, hearth_ref="plugin-add-test")
    heart = tmp_path / "heart"
    (heart / "compose" / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")

    src = tmp_path / "upstream-plugin"
    src.mkdir()
    (src / "tinder.toml").write_text(MINIMAL_TINDER, encoding="utf-8")
    scripts = src / "scripts"
    scripts.mkdir()
    stub = scripts / "install"
    stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    stub.chmod(stub.stat().st_mode | 0o111)

    add_plugin_from_source(heart=heart, source_spec=str(src), start_if_enabled=False)

    plug = heart / "plugins" / "fixture-one"
    assert (plug / "tinder.toml").is_file()

    rows = load_plugin_registry(heart)
    assert len(rows) == 1
    assert rows[0].slug == "fixture-one"
    assert rows[0].source_git == str(src.resolve())

    out = generate_plugin_compose(heart)
    yaml_text = out.read_text(encoding="utf-8")
    assert "fixture-one:" in yaml_text


def test_add_plugin_via_cli_list_and_add(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        "hearth_install.plugin_add._maybe_start_plugin_services",
        lambda *args, **kwargs: None,
    )

    root = tmp_path
    ensure_heart_layout(root, hearth_ref="cli-plugin")
    heart = root / "heart"
    (heart / "compose" / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")

    src = tmp_path / "upstream"
    src.mkdir()
    (src / "tinder.toml").write_text(MINIMAL_TINDER, encoding="utf-8")

    code = cli.run(["--install-root", str(root), "--plugin", "--add", str(src)])

    captured = capsys.readouterr()
    assert code == 0
    assert "installed plugin" in captured.out

    code = cli.run(["--install-root", str(root), "--plugin", "list"])
    out = capsys.readouterr().out
    assert code == 0
    assert "fixture-one" in out
    resolved = src.resolve().as_posix()
    assert resolved[:43] in out


@pytest.mark.skipif(not shutil.which("git"), reason="requires git executable")
def test_add_plugin_via_git_clone(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "hearth_install.plugin_add._maybe_start_plugin_services",
        lambda *args, **kwargs: None,
    )

    ensure_heart_layout(tmp_path, hearth_ref="git-clone")
    heart = tmp_path / "heart"
    (heart / "compose" / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")

    remote = tmp_path / "remote.git"
    remote.mkdir()

    subprocess.run(["git", "init", str(remote)], check=True, capture_output=True)

    plugged = remote / "tinder.toml"
    plugged.write_text(MINIMAL_TINDER, encoding="utf-8")

    subprocess.run(["git", "-C", str(remote), "add", "tinder.toml"], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(remote),
            "-c",
            "user.email=pytest@hearth.invalid",
            "-c",
            "user.name=pytest",
            "commit",
            "-m",
            "init",
        ],
        check=True,
    )

    add_plugin_from_source(heart=heart, source_spec=str(remote), start_if_enabled=False)

    loaded = load_plugin_registry(heart)
    assert loaded[0].slug == "fixture-one"
    assert loaded[0].pinned_ref


def test_save_plugin_registry_roundtrips_through_parser(tmp_path: Path) -> None:
    heart = ensure_heart_layout(tmp_path, hearth_ref="roundtrip")
    records = [
        PluginRecord(
            slug="alpha",
            source_git="https://example.test/a.git",
            enabled=True,
            pinned_ref="deadbeef",
            image="ghcr.io/example/a:1",
            port=8300,
        ),
        PluginRecord(
            slug="beta",
            source_git="https://example.test/b.git",
            enabled=False,
        ),
    ]
    save_plugin_registry(heart, records)
    again = load_plugin_registry(heart)
    assert [(r.slug, r.enabled, r.pinned_ref) for r in again] == [
        ("alpha", True, "deadbeef"),
        ("beta", False, None),
    ]


def _heart_with_one_plugin(tmp_path: Path) -> Path:
    ensure_heart_layout(tmp_path, hearth_ref="enter-test")
    heart = tmp_path / "heart"
    (heart / "compose" / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")
    plug = heart / "plugins" / "fixture-one"
    plug.mkdir(parents=True)
    (plug / "tinder.toml").write_text(MINIMAL_TINDER, encoding="utf-8")
    save_plugin_registry(
        heart,
        [
            PluginRecord(
                slug="fixture-one",
                source_git="https://example.test/fixture.git",
                enabled=True,
            ),
        ],
    )
    return heart


def test_plugin_enter_noninteractive_prints_exports(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(cli.sys.stdin, "isatty", lambda: False)
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: False)
    _heart_with_one_plugin(tmp_path)
    monkeypatch.chdir(tmp_path)

    code = cli.run(["--install-root", str(tmp_path), "--plugin", "enter", "--slug", "fixture-one"])
    out = capsys.readouterr().out
    assert code == 0
    assert "cd " in out
    assert "fixture-one" in out
    assert FROM_ENV in out
    assert STACK_ENV in out


def test_plugin_enter_requires_slug_when_non_interactive(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(cli.sys.stdin, "isatty", lambda: False)
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: False)
    _heart_with_one_plugin(tmp_path)
    monkeypatch.chdir(tmp_path)

    code = cli.run(["--install-root", str(tmp_path), "--plugin", "enter"])
    assert code == 2
    assert "--slug" in capsys.readouterr().err


def test_plugin_enter_interactive_prepares_execve(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(cli.sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: True)
    _heart_with_one_plugin(tmp_path)
    shell = tmp_path / "fake-sh"
    shell.write_text("#!/bin/sh\necho noop\n", encoding="utf-8")
    shell.chmod(shell.stat().st_mode | 0o111)
    monkeypatch.setenv("SHELL", str(shell))
    monkeypatch.chdir(tmp_path)

    calls: list[tuple[str, list[str], dict[str, str]]] = []

    def fake_execve(path: str, argv: list[str], env: dict[str, str]) -> None:
        calls.append((path, argv, env))
        raise RuntimeError("stop exec")

    monkeypatch.setattr(os, "execve", fake_execve)

    with pytest.raises(RuntimeError, match="stop exec"):
        cli.run(["--install-root", str(tmp_path), "--plugin", "enter", "--slug", "fixture-one"])

    assert len(calls) == 1
    path, argv, env = calls[0]
    assert path == str(shell)
    assert argv == [str(shell), "-i"]
    assert STACK_ENV in env
    assert FROM_ENV in env
