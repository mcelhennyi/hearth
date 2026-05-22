"""@HRT-OPS-002 Build plugin web UIs in Docker (operator parity with ``hearth pwa build``)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import TextIO

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


def resolve_plugin_root(
    hearth_dir: Path,
    slug: str,
    *,
    repo_root: Path | None = None,
) -> Path:
    """Locate a plugin tree by Tinder slug under install or deploy checkout."""
    normalized = slug.strip()
    if not normalized:
        raise PluginBuildError("plugin slug is required")

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
            return resolved

    locations = f"{hearth_dir / 'plugins' / normalized}"
    if repo_root is not None:
        locations += f" or under {repo_root / 'plugins'}"
    raise PluginBuildError(
        f"plugin {normalized!r} not found ({locations}). "
        "Install with `hearth --plugin --add` or check the slug in tinder.toml.",
    )


def resolve_plugin_web_dir(plugin_root: Path) -> Path:
    web_dir = plugin_root / "web"
    if not (web_dir / "package.json").is_file():
        msg = f"hearth plugin build: no web/package.json under {plugin_root}"
        raise PluginBuildError(msg)
    return web_dir


def npm_install_and_build_script(web_dir: Path) -> str:
    install = "npm ci" if (web_dir / "package-lock.json").is_file() else "npm install"
    return f"{install} && npm run build"


def docker_web_build_command(web_dir: Path, *, image: str) -> list[str]:
    resolved = web_dir.resolve()
    script = npm_install_and_build_script(resolved)
    return [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{resolved}:/work",
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
    runner: subprocess.CompletedProcess[str] | None = None,
) -> int:
    """Run ``npm ci|install`` and ``npm run build`` inside a Node container."""
    image = _node_image(env=env)
    command = docker_web_build_command(web_dir, image=image)
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
) -> int:
    """Build ``web/dist`` for a registered plugin slug."""
    hearth = resolved.hearth_dir
    if not hearth.is_dir():
        print(f"hearth plugin build: missing hearth directory: {hearth}", file=stderr)
        return 1

    repo_root: Path | None = None
    try:
        repo_root = resolve_deploy_repo_root(resolved, env=env)
    except ValueError:
        repo_root = None

    try:
        plugin_root = resolve_plugin_root(hearth, slug, repo_root=repo_root)
        web_dir = resolve_plugin_web_dir(plugin_root)
    except PluginBuildError as exc:
        print(f"hearth plugin build: {exc}", file=stderr)
        return 1

    code = run_plugin_web_build(web_dir, stderr, env=env, runner=runner)
    if code != 0:
        return code

    dist_index = web_dir / "dist" / "index.html"
    if not dist_index.is_file():
        print(f"hearth plugin build: missing build output at {dist_index}", file=stderr)
        return 1

    print(f"hearth plugin build: built {slug} UI at {web_dir / 'dist'}")
    print(
        "hearth plugin build: restart the plugin service to pick up static assets "
        f"(e.g. `hearth restart {slug}` or `hearth compose -- up -d --build {slug}`).",
    )
    return 0
