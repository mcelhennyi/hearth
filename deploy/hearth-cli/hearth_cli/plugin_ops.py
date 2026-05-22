"""@HRT-OPS-002 Build plugin web UIs in Docker (operator parity with ``hearth pwa build``)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import TextIO

from hearth_install.plugin_trees import sync_plugin_install_tree
from hearth_install.tinder_manifest import TinderManifestError, load_tinder_manifest

from hearth_cli.install_context import ResolvedInstall, resolve_deploy_repo_root

_DEFAULT_NODE_IMAGE = "node:20-alpine"


class PluginBuildError(ValueError):
    """User-facing plugin build failure."""


def _node_image(*, env: dict[str, str] | None = None) -> str:
    src = env if env is not None else os.environ
    return src.get("HEARTH_PLUGIN_BUILD_IMAGE", _DEFAULT_NODE_IMAGE).strip() or _DEFAULT_NODE_IMAGE


def _plugin_root_candidates(hearth_dir: Path, repo_root: Path | None, slug: str) -> list[Path]:
    candidates: list[Path] = [hearth_dir / "plugins" / slug]
    if repo_root is None:
        return candidates
    candidates.append(repo_root / "plugins" / slug)
    third_party = repo_root / "plugins" / "third-party"
    if third_party.is_dir():
        for child in sorted(third_party.iterdir()):
            if child.is_dir():
                candidates.append(child)
    return candidates


def _matching_plugin_roots(
    hearth_dir: Path,
    slug: str,
    *,
    repo_root: Path | None = None,
) -> list[Path]:
    """All trees whose ``tinder.toml`` slug matches ``slug``."""
    normalized = slug.strip()
    if not normalized:
        raise PluginBuildError("plugin slug is required")

    matches: list[Path] = []
    seen: set[Path] = set()
    for candidate in _plugin_root_candidates(hearth_dir, repo_root, normalized):
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        manifest_path = resolved / "tinder.toml"
        if not manifest_path.is_file():
            continue
        try:
            manifest = load_tinder_manifest(resolved)
        except (OSError, TinderManifestError) as exc:
            raise PluginBuildError(str(exc)) from exc
        if manifest.slug == normalized:
            matches.append(resolved)
    return matches


def resolve_plugin_root(
    hearth_dir: Path,
    slug: str,
    *,
    repo_root: Path | None = None,
) -> Path:
    """Locate a plugin tree by Tinder slug under install or deploy checkout."""
    matches = _matching_plugin_roots(hearth_dir, slug, repo_root=repo_root)
    if matches:
        return matches[0]

    locations = f"{hearth_dir / 'plugins' / slug.strip()}"
    if repo_root is not None:
        locations += f" or under {repo_root / 'plugins'}"
    raise PluginBuildError(
        f"plugin {slug.strip()!r} not found ({locations}). "
        "Install with `hearth --plugin --add` or check the slug in tinder.toml.",
    )


def resolve_plugin_root_for_build(
    hearth_dir: Path,
    slug: str,
    *,
    repo_root: Path | None = None,
) -> Path:
    """Pick a plugin tree that has ``web/package.json`` for UI builds."""
    matches = _matching_plugin_roots(hearth_dir, slug, repo_root=repo_root)
    if not matches:
        locations = f"{hearth_dir / 'plugins' / slug.strip()}"
        if repo_root is not None:
            locations += f" or under {repo_root / 'plugins'}"
        raise PluginBuildError(
            f"plugin {slug.strip()!r} not found ({locations}). "
            "Install with `hearth --plugin --add` or check the slug in tinder.toml.",
        )

    with_web = [root for root in matches if (root / "web" / "package.json").is_file()]
    if not with_web:
        tried = ", ".join(str(p) for p in matches)
        raise PluginBuildError(
            f"plugin {slug.strip()!r} has no web/package.json in any checkout ({tried}). "
            "Run `git submodule update --init` in HEARTH_REPO_ROOT or re-run "
            "`hearth --plugin --add` from a full plugin tree.",
        )

    install_root = (hearth_dir / "plugins" / slug.strip()).resolve()
    for root in with_web:
        if root == install_root:
            return root
    return with_web[0]


def resolve_plugin_web_dir(plugin_root: Path) -> Path:
    web_dir = plugin_root / "web"
    if not (web_dir / "package.json").is_file():
        msg = f"no web/package.json under {plugin_root}"
        raise PluginBuildError(msg)
    return web_dir


def publish_plugin_dist_to_install(
    build_root: Path,
    hearth_dir: Path,
    slug: str,
    *,
    stdout: TextIO,
) -> None:
    """Copy ``web/dist`` into ``hearth/plugins/<slug>/`` when the build used another checkout."""
    install_root = (hearth_dir / "plugins" / slug.strip()).resolve()
    if build_root.resolve() == install_root:
        return

    src_dist = build_root / "web" / "dist"
    dest_dist = install_root / "web" / "dist"
    if not src_dist.is_dir():
        return

    dest_dist.parent.mkdir(parents=True, exist_ok=True)
    if dest_dist.exists():
        shutil.rmtree(dest_dist)
    shutil.copytree(src_dist, dest_dist)
    print(
        f"hearth plugin build: published UI to {dest_dist} "
        "(compose mounts hearth/plugins/<slug>)",
        file=stdout,
    )


def web_has_file_dependencies(web_dir: Path) -> bool:
    """True when ``package.json`` references ``file:`` paths (needs repo-root mount)."""
    pkg_path = web_dir / "package.json"
    if not pkg_path.is_file():
        return False
    try:
        data = json.loads(pkg_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    for section in ("dependencies", "devDependencies", "optionalDependencies"):
        block = data.get(section)
        if not isinstance(block, dict):
            continue
        for value in block.values():
            if isinstance(value, str) and value.startswith("file:"):
                return True
    return False


def resolve_docker_build_mount(
    web_dir: Path,
    *,
    repo_root: Path | None,
    plugin_root: Path,
) -> tuple[Path, str]:
    """Return ``(host_mount, workdir_relative)`` for the Node container."""
    web_resolved = web_dir.resolve()
    if repo_root is not None and web_has_file_dependencies(web_dir):
        root = repo_root.resolve()
        try:
            return root, web_resolved.relative_to(root).as_posix()
        except ValueError:
            pass
        plugin_resolved = plugin_root.resolve()
        try:
            return plugin_resolved, web_resolved.relative_to(plugin_resolved).as_posix()
        except ValueError:
            pass
    return web_resolved, "."


def lockfile_usable(lock_path: Path) -> bool:
    """True when ``package-lock.json`` is present and valid enough for ``npm ci``."""
    if not lock_path.is_file():
        return False
    try:
        text = lock_path.read_text(encoding="utf-8").strip()
    except OSError:
        return False
    if not text or text == "{}":
        return False
    return '"lockfileVersion"' in text or '"packages"' in text


def npm_install_and_build_script(web_dir: Path, *, env: dict[str, str] | None = None) -> str:
    """Default ``npm install`` — plugins often use ``file:`` deps; opt into ``npm ci`` via env."""
    src = env if env is not None else os.environ
    use_ci = src.get("HEARTH_PLUGIN_BUILD_USE_CI", "").strip().lower() in ("1", "true", "yes")
    lock = web_dir / "package-lock.json"
    install = "npm ci" if use_ci and lockfile_usable(lock) else "npm install"
    return f"{install} && npm run build"


def docker_web_build_command(
    web_dir: Path,
    *,
    image: str,
    repo_root: Path | None = None,
    plugin_root: Path | None = None,
    env: dict[str, str] | None = None,
) -> list[str]:
    mount_host, work_subdir = resolve_docker_build_mount(
        web_dir,
        repo_root=repo_root,
        plugin_root=plugin_root or web_dir.parent,
    )
    inner = npm_install_and_build_script(web_dir, env=env)
    script = f"cd {work_subdir} && {inner}" if work_subdir != "." else inner
    return [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{mount_host}:/work",
        "-w",
        "/work",
        image,
        "sh",
        "-lc",
        script,
    ]


def run_plugin_web_build(
    web_dir: Path,
    stderr: TextIO,
    *,
    env: dict[str, str] | None = None,
    repo_root: Path | None = None,
    plugin_root: Path | None = None,
    runner: subprocess.CompletedProcess[str] | None = None,
) -> int:
    """Run ``npm install`` (or ``npm ci`` when opted in) and ``npm run build`` in Node."""
    image = _node_image(env=env)
    command = docker_web_build_command(
        web_dir,
        image=image,
        repo_root=repo_root,
        plugin_root=plugin_root,
        env=env,
    )
    try:
        if runner is not None:
            completed = runner
        else:
            completed = subprocess.run(command, check=False)
    except OSError as exc:
        print(f"hearth plugin build: failed to run {' '.join(command)}: {exc}", file=stderr)
        return 1
    if completed.returncode != 0:
        print(f"hearth plugin build: {' '.join(command)} exited {completed.returncode}", file=stderr)
        return completed.returncode
    return 0


def cmd_plugin_build(
    resolved: ResolvedInstall,
    slug: str,
    stderr: TextIO,
    *,
    env: dict[str, str] | None = None,
    runner: subprocess.CompletedProcess[str] | None = None,
    stdout: TextIO | None = None,
) -> int:
    """Build ``web/dist`` for a registered plugin slug."""
    out = stdout if stdout is not None else sys.stdout
    hearth = resolved.hearth_dir
    if not hearth.is_dir():
        print(f"hearth plugin build: missing hearth directory: {hearth}", file=stderr)
        return 1

    repo_root: Path | None = None
    try:
        repo_root = resolve_deploy_repo_root(resolved, env=env)
    except ValueError:
        repo_root = None

    if repo_root is not None:
        sync_plugin_install_tree(hearth, repo_root, slug)

    try:
        plugin_root = resolve_plugin_root_for_build(hearth, slug, repo_root=repo_root)
        web_dir = resolve_plugin_web_dir(plugin_root)
    except PluginBuildError as exc:
        print(f"hearth plugin build: {exc}", file=stderr)
        return 1

    if repo_root is not None and web_has_file_dependencies(web_dir):
        mantle = repo_root / "packages" / "mantle" / "package.json"
        if not mantle.is_file():
            print(
                "hearth plugin build: groceries UI depends on file:packages/mantle but "
                f"{mantle.parent} is missing.\n"
                f"  Ensure HEARTH_REPO_ROOT ({repo_root}) includes packages/mantle "
                "(git pull the hearth repo on feat/FR-0006-design-language).",
                file=stderr,
            )
            return 1

    code = run_plugin_web_build(
        web_dir,
        stderr,
        env=env,
        repo_root=repo_root,
        plugin_root=plugin_root,
        runner=runner,
    )
    if code != 0:
        return code

    dist_index = web_dir / "dist" / "index.html"
    if not dist_index.is_file():
        print(f"hearth plugin build: missing build output at {dist_index}", file=stderr)
        return 1

    publish_plugin_dist_to_install(plugin_root, hearth, slug, stdout=out)

    print(f"hearth plugin build: built {slug} UI at {web_dir / 'dist'}", file=out)
    print(
        "hearth plugin build: restart the plugin service to pick up static assets "
        f"(e.g. `hearth restart {slug}` or `hearth compose -- up -d --build {slug}`).",
        file=out,
    )
    return 0
