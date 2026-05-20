"""@HRT-OPS-002 FR-0002 PWA build helpers for Docker-profile installs."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import TextIO

from hearth_cli.install_context import ResolvedInstall, resolve_deploy_repo_root

_DEFAULT_PWA_ORIGIN = "https://hearth.home.arpa"


def _develop_script(repo_root: Path) -> Path:
    script = repo_root / "develop"
    if not script.is_file():
        msg = f"hearth pwa build: missing {script}"
        raise FileNotFoundError(msg)
    return script


def _patch_manifest_origin(static_dir: Path, origin: str) -> None:
    """iOS home-screen apps are more reliable with absolute ``start_url`` / ``scope``."""
    manifest_path = static_dir / "manifest.webmanifest"
    if not manifest_path.is_file():
        return
    normalized = origin.rstrip("/") + "/"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["start_url"] = normalized
    data["scope"] = normalized
    manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def cmd_pwa_build(resolved: ResolvedInstall, stderr: TextIO) -> int:
    """Build Mantle static assets into ``hearth/compose/static/`` for Caddy."""
    try:
        repo_root = resolve_deploy_repo_root(resolved)
    except ValueError as exc:
        print(str(exc), file=stderr)
        return 1

    develop = _develop_script(repo_root)
    static_dest = resolved.hearth_dir / "compose" / "static"
    static_dest.mkdir(parents=True, exist_ok=True)

    for args in (["web", "npm", "ci"], ["web", "npm", "run", "build"]):
        command = [str(develop), *args]
        try:
            completed = subprocess.run(command, cwd=repo_root, check=False)
        except OSError as exc:
            print(f"hearth pwa build: failed to run {' '.join(command)}: {exc}", file=stderr)
            return 1
        if completed.returncode != 0:
            print(f"hearth pwa build: {' '.join(command)} exited {completed.returncode}", file=stderr)
            return completed.returncode

    dist = repo_root / "apps" / "hub" / "web" / "dist"
    if not dist.is_dir():
        print(f"hearth pwa build: missing build output at {dist}", file=stderr)
        return 1

    if static_dest.exists():
        shutil.rmtree(static_dest)
    shutil.copytree(dist, static_dest)
    origin = os.environ.get("HEARTH_PWA_ORIGIN", _DEFAULT_PWA_ORIGIN).strip() or _DEFAULT_PWA_ORIGIN
    _patch_manifest_origin(static_dest, origin)
    print(f"hearth pwa build: published static bundle to {static_dest}")
    print(f"hearth pwa build: manifest start_url/scope set to {origin.rstrip('/')}/")
    return 0


def cmd_pwa_vapid_gen(resolved: ResolvedInstall, stderr: TextIO) -> int:
    """Generate VAPID keys under the deploy checkout (``./develop vapid-gen``)."""
    try:
        repo_root = resolve_deploy_repo_root(resolved)
    except ValueError as exc:
        print(str(exc), file=stderr)
        return 1

    develop = _develop_script(repo_root)
    command = [str(develop), "vapid-gen"]
    try:
        completed = subprocess.run(command, cwd=repo_root, check=False)
    except OSError as exc:
        print(f"hearth pwa vapid-gen: failed to run {' '.join(command)}: {exc}", file=stderr)
        return 1
    if completed.returncode != 0:
        print(f"hearth pwa vapid-gen: exited {completed.returncode}", file=stderr)
    return completed.returncode
