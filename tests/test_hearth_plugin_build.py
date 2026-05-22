"""``hearth plugin build`` — Docker npm build for plugin web/ trees."""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from hearth_cli import cli
from hearth_cli.plugin_ops import (
    PluginBuildError,
    docker_web_build_command,
    publish_plugin_dist_to_install,
    resolve_plugin_root,
    resolve_plugin_root_for_build,
    resolve_plugin_web_dir,
)
from hearth_install.layout import ensure_hearth_layout

_TINDER = textwrap.dedent(
    """\
    [plugin]
    slug = "fixture-one"
    name = "Fixture One"
    version = "0.1.0"
    hearth_min = "0.1.0"
    description = "fixture"

    [entrypoint]
    backend = { kind = "none" }
    ui = { kind = "static", path = "web/dist" }
    """,
)


def _write_install(tmp_path: Path, *, repo_root: Path | None = None) -> Path:
    ensure_hearth_layout(tmp_path, hearth_ref="plugin-build-test")
    hearth = tmp_path / "hearth"
    env_lines = []
    if repo_root is not None:
        env_lines.append(f"HEARTH_REPO_ROOT={repo_root.resolve()}")
    (hearth / "compose" / ".env").write_text("\n".join(env_lines) + "\n", encoding="utf-8")
    (hearth / "compose" / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")
    return hearth


def _write_plugin_tree(plug: Path, *, slug: str = "fixture-one", with_dist: bool = False) -> Path:
    plug.mkdir(parents=True, exist_ok=True)
    (plug / "tinder.toml").write_text(_TINDER, encoding="utf-8")
    web = plug / "web"
    web.mkdir()
    (web / "package.json").write_text('{"name":"fixture","scripts":{"build":"true"}}', encoding="utf-8")
    (web / "package-lock.json").write_text("{}\n", encoding="utf-8")
    if with_dist:
        dist = web / "dist"
        dist.mkdir()
        (dist / "index.html").write_text("<!doctype html><title>ok</title>", encoding="utf-8")
    return plug


def test_resolve_plugin_root_from_install_plugins(tmp_path: Path) -> None:
    hearth = _write_install(tmp_path)
    plug = _write_plugin_tree(hearth / "plugins" / "fixture-one")
    assert resolve_plugin_root(hearth, "fixture-one") == plug.resolve()


def test_resolve_plugin_root_from_repo_third_party(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    plug = _write_plugin_tree(repo / "plugins" / "third-party" / "grocery-list")
    hearth = _write_install(tmp_path / "install", repo_root=repo)
    assert resolve_plugin_root(hearth, "fixture-one", repo_root=repo) == plug.resolve()


def test_resolve_plugin_root_for_build_skips_install_stub_without_web(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    full = _write_plugin_tree(repo / "plugins" / "third-party" / "grocery-list")
    hearth = _write_install(tmp_path / "install", repo_root=repo)
    stub = hearth / "plugins" / "fixture-one"
    stub.mkdir(parents=True)
    (stub / "tinder.toml").write_text(_TINDER, encoding="utf-8")

    assert resolve_plugin_root_for_build(hearth, "fixture-one", repo_root=repo) == full.resolve()


def test_publish_plugin_dist_copies_to_install_tree(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    hearth = _write_install(tmp_path)
    build_root = _write_plugin_tree(tmp_path / "src", with_dist=True)
    stub = hearth / "plugins" / "fixture-one"
    stub.mkdir(parents=True)
    (stub / "tinder.toml").write_text(_TINDER, encoding="utf-8")

    publish_plugin_dist_to_install(build_root, hearth, "fixture-one", stdout=sys.stdout)

    assert (stub / "web" / "dist" / "index.html").is_file()
    assert "published UI" in capsys.readouterr().out


def test_resolve_plugin_web_dir_requires_package_json(tmp_path: Path) -> None:
    plug = tmp_path / "plug"
    plug.mkdir()
    with pytest.raises(PluginBuildError, match="package.json"):
        resolve_plugin_web_dir(plug)


def test_docker_web_build_command_uses_ci_when_lockfile_present(tmp_path: Path) -> None:
    web = tmp_path / "web"
    web.mkdir()
    (web / "package-lock.json").write_text("{}\n", encoding="utf-8")
    cmd = docker_web_build_command(web, image="node:20-alpine")
    assert "node:20-alpine" in cmd
    assert "npm ci" in cmd[-1]


def test_plugin_build_runs_docker_and_requires_dist(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    hearth = _write_install(tmp_path)
    _write_plugin_tree(hearth / "plugins" / "fixture-one")
    calls: list[list[str]] = []

    def fake_run(command: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        web = hearth / "plugins" / "fixture-one" / "web"
        dist = web / "dist"
        dist.mkdir(parents=True, exist_ok=True)
        (dist / "index.html").write_text("<!doctype html>", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr("hearth_cli.plugin_ops.subprocess.run", fake_run)

    code = cli.run(["--install-root", str(tmp_path), "plugin", "build", "fixture-one"])

    assert code == 0
    assert calls
    assert calls[0][0] == "docker"
    assert "fixture-one" in capsys.readouterr().out


def test_plugin_build_fails_when_docker_exits_nonzero(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    hearth = _write_install(tmp_path)
    _write_plugin_tree(hearth / "plugins" / "fixture-one")

    def fake_run(command: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 2)

    monkeypatch.setattr("hearth_cli.plugin_ops.subprocess.run", fake_run)

    code = cli.run(["--install-root", str(tmp_path), "plugin", "build", "fixture-one"])

    assert code == 2


def test_plugin_build_via_legacy_plugin_prefix(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    hearth = _write_install(tmp_path)
    _write_plugin_tree(hearth / "plugins" / "fixture-one", with_dist=True)

    def fake_run(command: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr("hearth_cli.plugin_ops.subprocess.run", fake_run)

    code = cli.run(["--install-root", str(tmp_path), "--plugin", "build", "fixture-one"])

    assert code == 0


def test_plugin_build_unknown_slug(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    hearth = _write_install(tmp_path)
    code = cli.run(["--install-root", str(tmp_path), "plugin", "build", "missing"])
    assert code == 1
    assert "not found" in capsys.readouterr().err


def test_plugin_build_publishes_dist_when_using_repo_checkout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_plugin_tree(repo / "plugins" / "third-party" / "grocery-list")
    install_root = tmp_path / "install"
    hearth = _write_install(install_root, repo_root=repo)
    stub = hearth / "plugins" / "fixture-one"
    stub.mkdir(parents=True)
    (stub / "tinder.toml").write_text(_TINDER, encoding="utf-8")

    def fake_run(command: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
        web = repo / "plugins" / "third-party" / "grocery-list" / "web"
        dist = web / "dist"
        dist.mkdir(parents=True, exist_ok=True)
        (dist / "index.html").write_text("<!doctype html>", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr("hearth_cli.plugin_ops.subprocess.run", fake_run)

    code = cli.run(["--install-root", str(install_root), "plugin", "build", "fixture-one"])

    assert code == 0
    assert (stub / "web" / "dist" / "index.html").is_file()
    assert "published UI" in capsys.readouterr().out
