"""Plugin install-tree sync and compose path generation."""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

from hearth_install.layout import ensure_hearth_layout
from hearth_install.plugin_compose import generate_plugin_compose, save_plugin_registry
from hearth_install.plugin_compose import PluginRecord
from hearth_install.plugin_trees import find_repo_plugin_root, sync_plugin_install_tree
from hearth_cli.plugin_ops import (
    docker_web_build_command,
    ensure_file_dependencies_built,
    iter_file_dependency_roots,
    lockfile_usable,
    npm_install_and_build_script,
    package_publish_entry_ready,
)

_TINDER = textwrap.dedent(
    """\
    [plugin]
    slug = "groceries"
    name = "Groceries"
    version = "0.1.0"
    hearth_min = "0.1.0"
    description = "fixture"

    [entrypoint]
    backend = { kind = "none" }
    ui = { kind = "static", path = "web/dist" }
    """,
)


def test_generate_plugin_compose_uses_override_relative_paths(tmp_path: Path) -> None:
    ensure_hearth_layout(tmp_path, hearth_ref="compose-paths")
    hearth = tmp_path / "hearth"
    plug = hearth / "plugins" / "groceries"
    plug.mkdir(parents=True)
    (plug / "tinder.toml").write_text(_TINDER, encoding="utf-8")
    (plug / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
    (hearth / "compose" / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")

    save_plugin_registry(
        hearth,
        [
            PluginRecord(
                slug="groceries",
                source_git="https://example.test/groceries.git",
                enabled=True,
            ),
        ],
    )

    out = generate_plugin_compose(hearth)
    yaml_text = out.read_text(encoding="utf-8")
    assert "context: ../../plugins/groceries" in yaml_text
    assert "../../plugins/groceries:/app:ro" in yaml_text


def test_sync_plugin_install_tree_symlinks_from_repo(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    src = repo / "plugins" / "third-party" / "grocery-list"
    src.mkdir(parents=True)
    (src / "tinder.toml").write_text(_TINDER, encoding="utf-8")
    (src / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")

    hearth = tmp_path / "install" / "hearth"
    stub = hearth / "plugins" / "groceries"
    stub.mkdir(parents=True)
    (stub / "tinder.toml").write_text(_TINDER, encoding="utf-8")

    dest = sync_plugin_install_tree(hearth, repo, "groceries")
    assert dest.is_symlink()
    assert dest.resolve() == src.resolve()
    assert find_repo_plugin_root(repo, "groceries") == src.resolve()


def test_npm_script_uses_install_without_valid_lockfile(tmp_path: Path) -> None:
    web = tmp_path / "web"
    web.mkdir()
    (web / "package-lock.json").write_text("{}\n", encoding="utf-8")
    assert not lockfile_usable(web / "package-lock.json")
    assert "npm install" in npm_install_and_build_script(web)
    cmd = docker_web_build_command(web, image="node:20-alpine")
    assert "npm install" in cmd[-1]


def test_package_publish_entry_ready_requires_built_dist(tmp_path: Path) -> None:
    mantle = tmp_path / "mantle"
    mantle.mkdir()
    (mantle / "package.json").write_text(
        '{"name":"@kindling/mantle","module":"./dist/index.js","exports":{".":{"import":"./dist/index.js"}}}\n',
        encoding="utf-8",
    )
    assert not package_publish_entry_ready(mantle)
    dist = mantle / "dist"
    dist.mkdir()
    (dist / "index.js").write_text("export {};\n", encoding="utf-8")
    assert package_publish_entry_ready(mantle)


def test_ensure_file_dependencies_builds_mantle_first(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo = tmp_path / "repo"
    mantle = repo / "packages" / "mantle"
    mantle.mkdir(parents=True)
    (mantle / "package.json").write_text(
        '{"name":"@kindling/mantle","scripts":{"build":"true"},"module":"./dist/index.js",'
        '"exports":{".":{"import":"./dist/index.js"}}}\n',
        encoding="utf-8",
    )
    web = repo / "plugins" / "third-party" / "grocery-list" / "web"
    web.mkdir(parents=True)
    (web / "package.json").write_text(
        '{"dependencies":{"@kindling/mantle":"file:../../../../packages/mantle"}}\n',
        encoding="utf-8",
    )
    assert iter_file_dependency_roots(web) == [mantle.resolve()]

    calls: list[list[str]] = []

    def fake_run(command: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if len(calls) == 1:
            dist = mantle / "dist"
            dist.mkdir(exist_ok=True)
            (dist / "index.js").write_text("export {};\n", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr("hearth_cli.plugin_ops.subprocess.run", fake_run)

    code = ensure_file_dependencies_built(
        web,
        sys.stderr,
        sys.stdout,
        repo_root=repo,
    )

    assert code == 0
    assert len(calls) == 1
    assert "packages/mantle" in calls[0][-1]
    assert "building file dependency" in capsys.readouterr().out


def test_docker_build_mounts_repo_root_for_file_dependencies(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    web = repo / "plugins" / "third-party" / "grocery-list" / "web"
    web.mkdir(parents=True)
    (web / "package.json").write_text(
        '{"dependencies":{"@kindling/mantle":"file:../../../../packages/mantle"}}\n',
        encoding="utf-8",
    )
    plugin_root = web.parent
    cmd = docker_web_build_command(
        web,
        image="node:20-alpine",
        repo_root=repo,
        plugin_root=plugin_root,
    )
    assert f"{repo.resolve()}:/work" in cmd
    assert "cd plugins/third-party/grocery-list/web" in cmd[-1]
