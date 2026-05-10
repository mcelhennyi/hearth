"""@HRT-OPS-002 Core ``hearth`` operator CLI for the Docker profile."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NoReturn, TextIO

from hearth_install.version_manifest import VersionManifestError, VersionManifestV1, read_version_manifest

from hearth_cli import update_cmd
from hearth_cli.install_context import ResolvedInstall, resolve_install


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
    parser.add_argument(
        "--update",
        action="store_true",
        help="Pull deploy checkout, refresh plugin checkouts + compose override, and compose up -d.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="With --update, print planned steps without changing git, compose files, or containers.",
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

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
    if ns.dry_run and not ns.update:
        parser.error("--dry-run requires --update")

    resolved = resolve_install(ns.install_root, env=env)

    if ns.update:
        if ns.command is not None:
            parser.error("--update cannot be combined with subcommands")
        return update_cmd.run_update(resolved, dry_run=ns.dry_run, stdout=stdout, stderr=stderr)

    if ns.command is None:
        parser.print_help()
        return 2

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
