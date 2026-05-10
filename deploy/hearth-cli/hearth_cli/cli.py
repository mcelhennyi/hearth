"""@HRT-OPS-002 Core ``hearth`` operator CLI for the Docker profile."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn, TextIO

from hearth_install.version_manifest import VersionManifestError, VersionManifestV1, read_version_manifest


@dataclass(frozen=True)
class ResolvedInstall:
    """Resolved install paths for a Docker-profile Hearth checkout."""

    install_root: Path
    heart_dir: Path
    version_path: Path
    compose_file: Path


def _looks_like_heart_dir(path: Path) -> bool:
    return (path / "VERSION.json").is_file()


def resolve_install(
    install_root: str | os.PathLike[str] | None = None,
    *,
    env: dict[str, str] | None = None,
) -> ResolvedInstall:
    """Resolve ``<install-root>/heart`` from CLI args, env, or cwd.

    ``HEARTH_INSTALL_ROOT`` and ``--install-root`` may point either at the parent
    install directory or directly at the ``heart/`` directory.
    """
    source_env = env if env is not None else os.environ
    raw_root = install_root or source_env.get("HEARTH_INSTALL_ROOT") or Path.cwd()
    candidate = Path(raw_root).expanduser().resolve()
    if _looks_like_heart_dir(candidate):
        heart_dir = candidate
        root = candidate.parent
    else:
        root = candidate
        heart_dir = root / "heart"
    return ResolvedInstall(
        install_root=root,
        heart_dir=heart_dir,
        version_path=heart_dir / "VERSION.json",
        compose_file=heart_dir / "compose" / "docker-compose.yml",
    )


def load_version(resolved: ResolvedInstall) -> VersionManifestV1:
    """Load the install manifest with a CLI-oriented error boundary."""
    return read_version_manifest(resolved.version_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hearth",
        description="Operate a Hearth Docker-profile install.",
    )
    parser.add_argument(
        "--install-root",
        metavar="PATH",
        help="Install root containing heart/ (or the heart/ directory itself).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version", help="Print the installed Hearth ref.")
    subparsers.add_parser("doctor", help="Check install files and Docker availability.")

    compose = subparsers.add_parser(
        "compose",
        help="Pass arguments through to docker compose for this install.",
    )
    compose.add_argument(
        "compose_args",
        nargs=argparse.REMAINDER,
        help="Arguments after -- are passed to docker compose.",
    )
    return parser


def cmd_version(resolved: ResolvedInstall, stdout: TextIO, stderr: TextIO) -> int:
    try:
        manifest = load_version(resolved)
    except (OSError, VersionManifestError) as exc:
        print(f"hearth version: {exc}", file=stderr)
        return 1
    print(f"Hearth install ref: {manifest.hearth_ref}", file=stdout)
    return 0


def cmd_doctor(resolved: ResolvedInstall, stdout: TextIO) -> int:
    ok = True
    print(f"install root: {resolved.install_root}", file=stdout)
    print(f"heart dir: {resolved.heart_dir}", file=stdout)

    if not resolved.heart_dir.is_dir():
        print("heart dir: missing", file=stdout)
        ok = False

    try:
        manifest = load_version(resolved)
    except (OSError, VersionManifestError) as exc:
        print(f"VERSION.json: {exc}", file=stdout)
        ok = False
    else:
        print(f"VERSION.json: schema={manifest.schema} hearth_ref={manifest.hearth_ref}", file=stdout)

    if resolved.compose_file.is_file():
        print(f"compose file: {resolved.compose_file}", file=stdout)
    else:
        print(f"compose file: missing ({resolved.compose_file})", file=stdout)
        ok = False

    docker = shutil.which("docker")
    if docker is None:
        print("docker: not found on PATH", file=stdout)
        ok = False
    else:
        print(f"docker: {docker}", file=stdout)

    return 0 if ok else 1


def _strip_separator(args: list[str]) -> list[str]:
    if args and args[0] == "--":
        return args[1:]
    return args


def cmd_compose(resolved: ResolvedInstall, args: list[str], stderr: TextIO) -> int:
    compose_args = _strip_separator(args)
    if not compose_args:
        print("hearth compose: expected arguments after --", file=stderr)
        return 2
    if not resolved.compose_file.is_file():
        print(f"hearth compose: missing compose file: {resolved.compose_file}", file=stderr)
        return 1

    command = ["docker", "compose", "-f", str(resolved.compose_file), *compose_args]
    try:
        completed = subprocess.run(command, cwd=resolved.compose_file.parent)
    except FileNotFoundError:
        print("hearth compose: docker not found on PATH", file=stderr)
        return 1
    return completed.returncode


def run(
    argv: list[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    env: dict[str, str] | None = None,
) -> int:
    stdout = stdout if stdout is not None else sys.stdout
    stderr = stderr if stderr is not None else sys.stderr
    parser = build_parser()
    ns = parser.parse_args(argv)
    resolved = resolve_install(ns.install_root, env=env)

    if ns.command == "version":
        return cmd_version(resolved, stdout, stderr)
    if ns.command == "doctor":
        return cmd_doctor(resolved, stdout)
    if ns.command == "compose":
        return cmd_compose(resolved, ns.compose_args, stderr)
    return _unreachable(ns.command)


def _unreachable(command: str) -> NoReturn:
    raise AssertionError(f"unhandled command: {command}")


def main(argv: list[str] | None = None) -> int:
    return run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
