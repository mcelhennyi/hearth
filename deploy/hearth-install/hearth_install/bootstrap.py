"""@HRT-OPS-003 Repo-root ``./install`` bootstrap (layout, shim, compose, first ``up``)."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TextIO

from hearth_install.layout import ensure_hearth_layout
from hearth_install.plugin_compose import generate_plugin_compose
from hearth_install.plugin_trees import sync_enabled_plugins_from_repo

_DOCKER_HINT_PI = """\
Docker Engine is required for the non-dry-run bootstrap.

Raspberry Pi OS (64-bit) quick path:
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker "$USER"
Then log out and back in so the docker group applies (non-root operator).

Other distros: https://docs.docker.com/engine/install/
"""


def _package_templates() -> Path:
    return Path(__file__).resolve().parent / "templates"


def _resolve_install_root(raw: str | None, env: dict[str, str]) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    env_root = env.get("HEARTH_INSTALL_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    msg = "install root: pass INSTALL_DIR or set HEARTH_INSTALL_ROOT"
    raise SystemExit(msg)


@dataclass(frozen=True)
class BootstrapPaths:
    repo_root: Path
    install_root: Path


def plan_bootstrap(
    paths: BootstrapPaths,
    *,
    hearth_ref: str,
    dry_run: bool,
    skip_compose_up: bool,
) -> list[str]:
    """Human-readable plan lines (used by ``--dry-run`` and logging)."""

    hearth = paths.install_root / "hearth"
    lines = [
        f"repo root: {paths.repo_root}",
        f"install root: {paths.install_root}",
        f"VERSION.json hearth_ref (when created): {hearth_ref}",
        f"ensure layout under {hearth}",
        f"write {hearth / 'compose' / 'docker-compose.yml'} from packaged template",
        f"write {hearth / 'compose' / '.env'} with HEARTH_REPO_ROOT={paths.repo_root}",
        f"copy Caddy configs to {hearth / 'compose' / 'caddy'}",
        f"ensure static publish dir at {hearth / 'compose' / 'static'}",
        f"sync enabled plugins from repo into {hearth / 'plugins'} (symlink when stubs)",
        f"generate {hearth / 'compose' / 'overrides' / 'generated.plugins.yml'}",
        f"symlink {hearth / 'bin' / 'hearth'} -> {paths.repo_root / 'bin' / 'hearth'}",
    ]
    if dry_run:
        lines.append("dry-run: no filesystem or compose changes")
    elif skip_compose_up:
        lines.append("skip: docker compose up -d (Docker Engine not validated)")
        lines.append(f"will still write compose files under {hearth / 'compose'}")
    else:
        lines.append("verify Docker Engine (docker info)")
        lines.append(
            f"run: docker compose -f docker-compose.yml "
            f"[-f overrides/generated.plugins.yml] --project-name hearth up -d "
            f"(cwd {hearth / 'compose'})",
        )
    lines.append(
        "PATH: add hearth/bin to your shell profile, e.g. "
        f'export PATH="{hearth}/bin:$PATH"',
    )
    return lines


def verify_docker_engine(stderr: TextIO) -> bool:
    """Return True when the CLI exists and the daemon answers ``docker info``."""

    if shutil.which("docker") is None:
        print("bootstrap: docker CLI not found on PATH.", file=stderr)
        print(_DOCKER_HINT_PI, file=stderr)
        return False
    try:
        proc = subprocess.run(
            ["docker", "info"],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"bootstrap: docker info failed: {exc}", file=stderr)
        print(_DOCKER_HINT_PI, file=stderr)
        return False
    if proc.returncode != 0:
        print("bootstrap: docker daemon not reachable (docker info failed).", file=stderr)
        if proc.stderr.strip():
            print(proc.stderr.strip(), file=stderr)
        print(_DOCKER_HINT_PI, file=stderr)
        return False
    return True


def install_hearth_shim(hearth_bin: Path, target: Path, *, dry_run: bool) -> None:
    """Place ``hearth/bin/hearth`` pointing at the repo launcher."""

    hearth_bin.mkdir(parents=True, exist_ok=True)
    shim = hearth_bin / "hearth"
    target_abs = target.resolve()
    if dry_run:
        return
    if shim.is_symlink() and shim.resolve() == target_abs:
        return
    if shim.exists() or shim.is_symlink():
        shim.unlink()
    shim.symlink_to(target_abs)


def materialize_compose_template(hearth: Path, *, dry_run: bool) -> Path:
    """Copy the packaged install compose template into ``hearth/compose/``."""

    src = _package_templates() / "docker-compose.install.yml"
    dest_dir = hearth / "compose"
    dest = dest_dir / "docker-compose.yml"
    if dry_run:
        return dest
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    return dest


def write_compose_env_file(hearth: Path, repo_root: Path, *, dry_run: bool) -> Path:
    """Write ``compose/.env`` with ``HEARTH_REPO_ROOT`` for image build contexts."""

    dest = hearth / "compose" / ".env"
    body = (
        f"HEARTH_REPO_ROOT={repo_root.resolve()}\n"
        "HEARTH_COMPOSE_PROJECT_NAME=hearth\n"
    )
    if dry_run:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body, encoding="utf-8")
    return dest


def materialize_compose_assets(repo_root: Path, hearth: Path, *, dry_run: bool) -> None:
    """Copy Caddy dev configs and ensure a static publish directory exists."""

    caddy_src = repo_root / "deploy" / "caddy"
    caddy_dest = hearth / "compose" / "caddy"
    static_dest = hearth / "compose" / "static"
    if dry_run:
        return
    if not caddy_src.is_dir():
        msg = f"bootstrap: missing Caddy config directory: {caddy_src}"
        raise FileNotFoundError(msg)
    if caddy_dest.exists():
        shutil.rmtree(caddy_dest)
    shutil.copytree(caddy_src, caddy_dest)
    static_dest.mkdir(parents=True, exist_ok=True)
    placeholder = repo_root / "deploy" / "static" / "index.html"
    index_dest = static_dest / "index.html"
    if placeholder.is_file() and not index_dest.is_file():
        shutil.copyfile(placeholder, index_dest)


def run_compose_up(
    hearth: Path,
    *,
    dry_run: bool,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> int:
    """``docker compose up -d`` from ``hearth/compose`` (same flags as ``hearth start``)."""

    if dry_run:
        return 0
    compose_dir = hearth / "compose"
    compose_file = compose_dir / "docker-compose.yml"
    overrides = compose_dir / "overrides" / "generated.plugins.yml"
    command: list[str] = [
        "docker",
        "compose",
        "-f",
        compose_file.name,
    ]
    if overrides.is_file():
        command.extend(["-f", "overrides/generated.plugins.yml"])
    command.extend(["--project-name", "hearth"])
    env_file = compose_dir / ".env"
    if env_file.is_file():
        command.extend(["--env-file", ".env"])
    command.extend(["up", "-d"])
    proc = runner(
        command,
        cwd=str(compose_dir),
        check=False,
    )
    return int(proc.returncode)


def run_bootstrap(
    argv: list[str] | None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    env: dict[str, str] | None = None,
    compose_runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> int:
    """CLI entry for ``python -m hearth_install.bootstrap``."""

    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    source_env = env if env is not None else dict(os.environ)
    compose_runner = compose_runner or subprocess.run

    parser = argparse.ArgumentParser(
        description="Bootstrap a Hearth Docker-profile install (hearth/ layout + compose + first up).",
    )
    parser.add_argument(
        "install_dir",
        nargs="?",
        default=None,
        help="Install root (parent of hearth/). Defaults to HEARTH_INSTALL_ROOT.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Hearth deploy checkout (directory containing bin/hearth). Default: infer from module location.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions only; do not write files or run Docker.",
    )
    parser.add_argument(
        "--skip-compose-up",
        action="store_true",
        help="Skip docker compose up -d after generating compose files.",
    )
    parser.add_argument(
        "--skip-docker-check",
        action="store_true",
        help="Skip docker info validation (for tests or air-gapped planning).",
    )
    parser.add_argument(
        "--hearth-ref",
        default="unknown",
        help='Git ref recorded in VERSION.json when created (default: "%(default)s").',
    )
    ns = parser.parse_args(argv)

    repo_root = ns.repo_root
    if repo_root is None:
        # deploy/hearth-install/hearth_install/bootstrap.py -> parents[2] = repo root
        repo_root = Path(__file__).resolve().parents[3]
    repo_root = repo_root.resolve()

    try:
        install_root = _resolve_install_root(ns.install_dir, source_env)
    except SystemExit as exc:
        print(str(exc), file=stderr)
        return 2

    paths = BootstrapPaths(repo_root=repo_root, install_root=install_root)
    for line in plan_bootstrap(
        paths,
        hearth_ref=ns.hearth_ref,
        dry_run=ns.dry_run,
        skip_compose_up=ns.skip_compose_up,
    ):
        print(line, file=stdout)

    if ns.dry_run:
        print("dry-run: no changes applied.", file=stdout)
        return 0

    hearth = ensure_hearth_layout(install_root, hearth_ref=ns.hearth_ref)
    materialize_compose_template(hearth, dry_run=False)
    write_compose_env_file(hearth, repo_root, dry_run=False)
    materialize_compose_assets(repo_root, hearth, dry_run=False)
    sync_enabled_plugins_from_repo(hearth, repo_root)
    generate_plugin_compose(hearth)
    launcher = repo_root / "bin" / "hearth"
    if not launcher.is_file():
        print(f"bootstrap: missing repo launcher {launcher}", file=stderr)
        return 1
    install_hearth_shim(hearth / "bin", launcher, dry_run=False)

    compose_file = hearth / "compose" / "docker-compose.yml"
    if ns.skip_compose_up:
        print(f"bootstrap: compose files ready at {compose_file.parent}", file=stdout)
        return 0

    if not ns.skip_docker_check:
        if not verify_docker_engine(stderr):
            return 1

    code = run_compose_up(hearth, dry_run=False, runner=compose_runner)
    if code != 0:
        print(f"bootstrap: docker compose up exited {code}", file=stderr)
    else:
        print("bootstrap: docker compose up -d finished.", file=stdout)
    return code


def main() -> None:
    raise SystemExit(run_bootstrap(sys.argv[1:]))


if __name__ == "__main__":
    main()
