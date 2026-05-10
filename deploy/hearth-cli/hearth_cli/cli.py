"""@HRT-OPS-002 Core ``hearth`` operator CLI for the Docker profile."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NoReturn, TextIO

from hearth_install.plugin_add import PluginAddError, add_plugin_from_source, format_plugin_list_lines
from hearth_install.plugin_compose import PluginRegistryError
from hearth_install.tinder_manifest import TinderManifestError
from hearth_install.version_manifest import VersionManifestError, VersionManifestV1, read_version_manifest

from hearth_cli import update_cmd
from hearth_cli.install_context import ResolvedInstall, resolve_install


def load_version(resolved: ResolvedInstall) -> VersionManifestV1:
    """Load the install manifest with a CLI-oriented error boundary."""
    return read_version_manifest(resolved.version_path)


def build_parser(command_required: bool = True) -> argparse.ArgumentParser:
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


def split_plugin_argv(argv: list[str]) -> tuple[list[str], list[str]]:
    """Split argv at ``--plugin`` if present."""

    if "--plugin" not in argv:
        return argv, []
    idx = argv.index("--plugin")
    prefix = argv[:idx]
    suffix = argv[idx + 1 :]
    return prefix, suffix


def parse_install_only(argv: list[str]) -> str | None:
    """Parse optional ``--install-root`` prefix for plugin invocation."""

    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--install-root", dest="install_root", metavar="PATH", default=None)
    ns, leftover = pre.parse_known_args(argv)
    if leftover:
        extra = ", ".join(leftover)
        raise SystemExit(f"unexpected arguments next to hearth --plugin: {extra}")
    return ns.install_root


def cmd_plugin_list(resolved: ResolvedInstall, stdout: TextIO, stderr: TextIO) -> int:
    heart = resolved.heart_dir
    if not heart.is_dir():
        print(f"hearth plugin list: missing heart directory: {heart}", file=stderr)
        return 1
    try:
        rows = format_plugin_list_lines(heart)
    except (PluginRegistryError, OSError) as exc:
        print(f"hearth plugin list: {exc}", file=stderr)
        return 1
    print("\n".join(rows), file=stdout)
    return 0


def cmd_plugin_add(
    resolved: ResolvedInstall,
    source: str,
    *,
    stdout: TextIO,
    stderr: TextIO,
    start_if_enabled: bool,
) -> int:
    heart = resolved.heart_dir
    if not heart.is_dir():
        print(f"hearth --plugin --add: missing heart directory: {heart}", file=stderr)
        return 1
    try:
        add_plugin_from_source(
            heart=heart,
            source_spec=source,
            start_if_enabled=start_if_enabled,
        )
    except PluginAddError as exc:
        print(f"hearth --plugin --add: {exc}", file=stderr)
        return exc.exit_code
    except (PluginRegistryError, TinderManifestError) as exc:
        print(f"hearth --plugin --add: {exc}", file=stderr)
        return 1
    print(f"installed plugin into {heart / 'plugins'} from {source!r}", file=stdout)
    return 0


def cmd_plugin_argv(
    prefix: list[str],
    suffix: list[str],
    *,
    stdout: TextIO,
    stderr: TextIO,
) -> int:
    install_raw = parse_install_only(prefix)
    if not suffix:
        print("hearth --plugin requires --add GIT_URL [...] or the list verb.", file=stderr)
        return 2

    if suffix[0] == "list":
        if len(suffix) != 1:
            print("hearth --plugin list: unexpected extra arguments.", file=stderr)
            return 2
        resolved = resolve_install(install_raw)
        return cmd_plugin_list(resolved, stdout, stderr)

    if len(suffix) >= 2 and suffix[0] == "--add":
        source = suffix[1]
        if len(suffix) > 2:
            print("hearth --plugin --add: unexpected extra arguments after source URL.", file=stderr)
            return 2

        resolved = resolve_install(install_raw)
        return cmd_plugin_add(
            resolved,
            source,
            stdout=stdout,
            stderr=stderr,
            start_if_enabled=True,
        )

    print("hearth --plugin: expected `list` or `--add GIT_URL_OR_PATH`.", file=stderr)
    return 2


def run(
    argv: list[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    env: dict[str, str] | None = None,
) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    stdout = stdout if stdout is not None else sys.stdout
    stderr = stderr if stderr is not None else sys.stderr

    prefix, plugin_suffix = split_plugin_argv(argv)
    if plugin_suffix:
        try:
            return cmd_plugin_argv(prefix, plugin_suffix, stdout=stdout, stderr=stderr)
        except SystemExit as exc:
            raw_code = exc.code
            if isinstance(raw_code, str):
                print(raw_code, file=stderr)
                return 2
            if raw_code is None:
                return 0
            return int(raw_code)

    parser = build_parser(command_required=True)
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
