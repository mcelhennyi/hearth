"""@HRT-OPS-002 Core ``hearth`` operator CLI for the Docker profile."""

from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import NoReturn, TextIO

from hearth_install.plugin_add import (
    PluginAddError,
    add_plugin_from_source,
    format_plugin_list_lines,
)
from hearth_install.plugin_compose import PluginRegistryError, load_plugin_registry
from hearth_install.plugin_session import (
    FROM_ENV,
    STACK_ENV,
    prepare_enter_environment,
)
from hearth_install.tinder_manifest import TinderManifestError
from hearth_install.version_manifest import (
    VersionManifestError,
    VersionManifestV1,
    read_version_manifest,
)

from hearth_cli import update_cmd
from hearth_cli.install_context import ResolvedInstall, resolve_install

_DEFAULT_COMPOSE_PROJECT = "hearth"
_HUB_HEALTH_PATH = "/api/health"
_HUB_INTERNAL_PORTS = ("8000", "8080", "80")


def load_version(resolved: ResolvedInstall) -> VersionManifestV1:
    """Load the install manifest with a CLI-oriented error boundary."""
    return read_version_manifest(resolved.version_path)


def compose_project_name(*, env: dict[str, str] | None = None) -> str:
    """Compose project name; override with ``HEARTH_COMPOSE_PROJECT_NAME``."""
    src = env if env is not None else os.environ
    return src.get("HEARTH_COMPOSE_PROJECT_NAME", _DEFAULT_COMPOSE_PROJECT)


def resolve_compose_env_file(
    resolved: ResolvedInstall,
    *,
    env: dict[str, str] | None = None,
) -> Path | None:
    """Optional ``--env-file`` for docker compose.

    Preference: ``HEARTH_COMPOSE_ENV_FILE`` when set and the path exists;
    otherwise ``hearth/compose/.env`` when present.
    """
    src = env if env is not None else os.environ
    explicit = src.get("HEARTH_COMPOSE_ENV_FILE")
    if explicit:
        path = Path(explicit).expanduser().resolve()
        return path if path.is_file() else None
    candidate = resolved.compose_file.parent / ".env"
    return candidate if candidate.is_file() else None


def assemble_docker_compose_command(
    resolved: ResolvedInstall,
    compose_tail: list[str],
    *,
    env: dict[str, str] | None = None,
) -> tuple[list[str], Path]:
    """Build ``docker compose`` argv with stable project/env-file and return cwd."""
    cwd = resolved.compose_file.parent
    cmd: list[str] = [
        "docker",
        "compose",
        "-f",
        str(resolved.compose_file),
    ]
    overrides = resolved.hearth_dir / "compose" / "overrides" / "generated.plugins.yml"
    if overrides.is_file():
        cmd.extend(["-f", str(overrides)])
    cmd.extend(
        [
            "--project-name",
            compose_project_name(env=env),
        ],
    )
    env_file = resolve_compose_env_file(resolved, env=env)
    if env_file is not None:
        cmd.extend(["--env-file", str(env_file)])
    cmd.extend(compose_tail)
    return cmd, cwd


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hearth",
        description="Operate a Hearth Docker-profile install.",
    )
    parser.add_argument(
        "--install-root",
        metavar="PATH",
        help="Install root containing hearth/ (or the hearth/ directory itself).",
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

    start = subparsers.add_parser("start", help="Start stack in the background (docker compose up -d).")
    start.add_argument("services", nargs="*", help="Optional service names.")

    stop = subparsers.add_parser("stop", help="Stop stack containers (docker compose stop).")
    stop.add_argument("services", nargs="*", help="Optional service names.")

    restart = subparsers.add_parser("restart", help="Restart services (docker compose restart).")
    restart.add_argument("services", nargs="*", help="Optional service names.")

    status = subparsers.add_parser(
        "status",
        help="Show docker compose ps -a and optionally probe hub /api/health.",
    )
    status.add_argument(
        "--skip-health",
        action="store_true",
        help="Do not probe hub HTTP /api/health after ps (see HEARTH_HUB_HEALTH_URL).",
    )

    logs = subparsers.add_parser("logs", help="Tail or fetch container logs (docker compose logs).")
    logs.add_argument("-f", "--follow", action="store_true", help="Follow log output.")
    logs.add_argument("services", nargs="*", help="Optional service names.")
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
    print(f"hearth dir: {resolved.hearth_dir}", file=stdout)

    if not resolved.hearth_dir.is_dir():
        print("hearth dir: missing", file=stdout)
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


def _run_compose(
    resolved: ResolvedInstall,
    compose_tail: list[str],
    stderr: TextIO,
    *,
    env: dict[str, str] | None = None,
) -> int:
    if not resolved.compose_file.is_file():
        print(f"hearth: missing compose file: {resolved.compose_file}", file=stderr)
        return 1

    command, cwd = assemble_docker_compose_command(resolved, compose_tail, env=env)
    try:
        completed = subprocess.run(command, cwd=cwd)
    except FileNotFoundError:
        print("hearth: docker not found on PATH", file=stderr)
        return 1
    return completed.returncode


def cmd_compose(
    resolved: ResolvedInstall,
    args: list[str],
    stderr: TextIO,
    *,
    env: dict[str, str] | None = None,
) -> int:
    compose_args = _strip_separator(args)
    if not compose_args:
        print("hearth compose: expected arguments after --", file=stderr)
        return 2
    return _run_compose(resolved, compose_args, stderr, env=env)


def cmd_start(
    resolved: ResolvedInstall,
    services: list[str],
    stderr: TextIO,
    *,
    env: dict[str, str] | None = None,
) -> int:
    return _run_compose(resolved, ["up", "-d", *services], stderr, env=env)


def cmd_stop(
    resolved: ResolvedInstall,
    services: list[str],
    stderr: TextIO,
    *,
    env: dict[str, str] | None = None,
) -> int:
    tail = ["stop", *services] if services else ["stop"]
    return _run_compose(resolved, tail, stderr, env=env)


def cmd_restart(
    resolved: ResolvedInstall,
    services: list[str],
    stderr: TextIO,
    *,
    env: dict[str, str] | None = None,
) -> int:
    tail = ["restart", *services] if services else ["restart"]
    return _run_compose(resolved, tail, stderr, env=env)


def _parse_docker_port_mapping(text: str) -> tuple[str, int] | None:
    text = text.strip()
    if not text:
        return None
    if "]:" in text:
        _left, right = text.rsplit(":", 1)
    else:
        parts = text.rsplit(":", 1)
        if len(parts) != 2:
            return None
        _left, right = parts
    try:
        port = int(right)
    except ValueError:
        return None
    return "127.0.0.1", port


def _compose_port_mapping(
    resolved: ResolvedInstall,
    service: str,
    internal_port: str,
    *,
    env: dict[str, str] | None = None,
) -> tuple[str, int] | None:
    argv, cwd = assemble_docker_compose_command(resolved, ["port", service, internal_port], env=env)
    try:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    if completed.returncode != 0:
        return None
    return _parse_docker_port_mapping(completed.stdout)


def _hub_health_url_from_env(*, env: dict[str, str] | None) -> str | None:
    src = env if env is not None else os.environ
    raw = src.get("HEARTH_HUB_HEALTH_URL", "").strip()
    return raw or None


def _discover_hub_health_url(
    resolved: ResolvedInstall,
    *,
    env: dict[str, str] | None = None,
) -> str | None:
    explicit = _hub_health_url_from_env(env=env)
    if explicit is not None:
        return explicit

    for internal in _HUB_INTERNAL_PORTS:
        mapping = _compose_port_mapping(resolved, "hub", internal, env=env)
        if mapping is None:
            continue
        host, port = mapping
        return f"http://{host}:{port}{_HUB_HEALTH_PATH}"
    return None


def _print_hub_health(
    resolved: ResolvedInstall,
    stdout: TextIO,
    *,
    env: dict[str, str] | None = None,
) -> None:
    url = _discover_hub_health_url(resolved, env=env)
    if url is None:
        print("hub /api/health: (skipped — set HEARTH_HUB_HEALTH_URL or publish hub ports)", file=stdout)
        return

    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            code = resp.status
    except urllib.error.HTTPError as exc:
        code = exc.code
    except urllib.error.URLError as exc:
        print(f"hub /api/health: unreachable ({exc.reason})", file=stdout)
        return
    except Exception as exc:  # pragma: no cover - defensive
        print(f"hub /api/health: unreachable ({exc})", file=stdout)
        return

    print(f"hub /api/health: HTTP {code} ({url})", file=stdout)


def cmd_status(
    resolved: ResolvedInstall,
    stdout: TextIO,
    stderr: TextIO,
    *,
    env: dict[str, str] | None = None,
    skip_health: bool = False,
) -> int:
    code = _run_compose(resolved, ["ps", "-a"], stderr, env=env)
    if code != 0:
        return code
    if not skip_health:
        _print_hub_health(resolved, stdout, env=env)
    return 0


def cmd_logs(
    resolved: ResolvedInstall,
    services: list[str],
    stderr: TextIO,
    *,
    env: dict[str, str] | None = None,
    follow: bool = False,
) -> int:
    tail = ["logs"]
    if follow:
        tail.append("-f")
    tail.extend(services)
    return _run_compose(resolved, tail, stderr, env=env)


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
    hearth = resolved.hearth_dir
    if not hearth.is_dir():
        print(f"hearth plugin list: missing hearth directory: {hearth}", file=stderr)
        return 1
    try:
        rows = format_plugin_list_lines(hearth)
    except (PluginRegistryError, OSError) as exc:
        print(f"hearth plugin list: {exc}", file=stderr)
        return 1
    print("\n".join(rows), file=stdout)
    return 0


def _plugin_enter_candidates(hearth: Path) -> list[str]:
    try:
        rows = load_plugin_registry(hearth)
    except (PluginRegistryError, OSError):
        rows = []
    if rows:
        return [record.slug for record in rows]

    root = hearth / "plugins"
    if not root.is_dir():
        return []
    slugs: list[str] = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / "tinder.toml").is_file():
            slugs.append(child.name)
    return slugs


def _prompt_plugin_slug(hearth: Path, stdout: TextIO, stderr: TextIO) -> str | None:
    candidates = _plugin_enter_candidates(hearth)
    if not candidates:
        print(
            "hearth --plugin enter: no plugins found "
            "(expected registry rows or hearth/plugins/*/tinder.toml).",
            file=stderr,
        )
        return None

    print("Select a plugin (number):", file=stdout)
    for idx, slug in enumerate(candidates, start=1):
        print(f"  [{idx}] {slug}", file=stdout)
    try:
        raw = input().strip()
    except EOFError:
        print("hearth --plugin enter: unexpected EOF while reading selection.", file=stderr)
        return None
    if not raw.isdigit():
        print(f"hearth --plugin enter: expected a number, got {raw!r}.", file=stderr)
        return None
    choice = int(raw, 10)
    if choice < 1 or choice > len(candidates):
        print(f"hearth --plugin enter: selection out of range: {choice}.", file=stderr)
        return None
    return candidates[choice - 1]


def _emit_noninteractive_enter_instructions(plugin_dir: Path, stdout: TextIO) -> int:
    env = os.environ.copy()
    prepare_enter_environment(env, from_dir=Path.cwd())
    print(
        "hearth --plugin enter: non-interactive terminal; run:\n"
        f"  cd {plugin_dir}\n"
        f"  export {FROM_ENV}={shlex.quote(env[FROM_ENV])}\n"
        f"  export {STACK_ENV}={shlex.quote(env[STACK_ENV])}\n",
        file=stdout,
    )
    print(
        "Use `./plugin --exit` from the plugin directory once `hearth-ops` "
        "is on `PYTHONPATH` (same as the `hearth` CLI).",
        file=stdout,
    )
    return 0


def cmd_plugin_enter(
    resolved: ResolvedInstall,
    slug: str | None,
    *,
    stdout: TextIO,
    stderr: TextIO,
) -> int:
    hearth = resolved.hearth_dir
    if not hearth.is_dir():
        print(f"hearth --plugin enter: missing hearth directory: {hearth}", file=stderr)
        return 1

    chosen = slug
    if chosen is None:
        if not sys.stdin.isatty() or not sys.stdout.isatty():
            print(
                "hearth --plugin enter: --slug is required when stdin/stdout is not a TTY.",
                file=stderr,
            )
            print(
                "(Interactive bash/zsh: omit --slug for a numbered picker.)",
                file=stderr,
            )
            return 2
        chosen = _prompt_plugin_slug(hearth, stdout, stderr)
        if chosen is None:
            return 1

    plugin_dir = (hearth / "plugins" / chosen).resolve()
    if not plugin_dir.is_dir() or not (plugin_dir / "tinder.toml").is_file():
        print(f"hearth --plugin enter: not a plugin directory: {plugin_dir}", file=stderr)
        return 1

    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return _emit_noninteractive_enter_instructions(plugin_dir, stdout)

    env = os.environ.copy()
    prepare_enter_environment(env, from_dir=Path.cwd())
    try:
        os.chdir(plugin_dir)
    except OSError as exc:
        print(f"hearth --plugin enter: cannot cd to {plugin_dir}: {exc}", file=stderr)
        return 1

    shell = os.environ.get("SHELL") or "/bin/bash"
    if not Path(shell).is_file():
        print(
            f"hearth --plugin enter: SHELL {shell!r} is not an executable file; "
            "set SHELL to bash or zsh.",
            file=stderr,
        )
        return 1

    try:
        os.execve(shell, [shell, "-i"], env)
    except OSError as exc:
        print(f"hearth --plugin enter: cannot exec {shell!r}: {exc}", file=stderr)
        return 1
    return 0


def cmd_plugin_add(
    resolved: ResolvedInstall,
    source: str,
    *,
    stdout: TextIO,
    stderr: TextIO,
    start_if_enabled: bool,
) -> int:
    hearth = resolved.hearth_dir
    if not hearth.is_dir():
        print(f"hearth --plugin --add: missing hearth directory: {hearth}", file=stderr)
        return 1
    try:
        add_plugin_from_source(
            hearth=hearth,
            source_spec=source,
            start_if_enabled=start_if_enabled,
        )
    except PluginAddError as exc:
        print(f"hearth --plugin --add: {exc}", file=stderr)
        return exc.exit_code
    except (PluginRegistryError, TinderManifestError) as exc:
        print(f"hearth --plugin --add: {exc}", file=stderr)
        return 1
    print(f"installed plugin into {hearth / 'plugins'} from {source!r}", file=stdout)
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
        print(
            "hearth --plugin requires `list`, `enter`, `--add GIT_URL_OR_PATH`, or similar.",
            file=stderr,
        )
        return 2

    if suffix[0] == "list":
        if len(suffix) != 1:
            print("hearth --plugin list: unexpected extra arguments.", file=stderr)
            return 2
        resolved = resolve_install(install_raw)
        return cmd_plugin_list(resolved, stdout, stderr)

    if suffix[0] == "enter":
        rest = suffix[1:]
        slug: str | None = None
        idx = 0
        while idx < len(rest):
            if rest[idx] == "--slug":
                if idx + 1 >= len(rest):
                    print("hearth --plugin enter: `--slug` requires a value.", file=stderr)
                    return 2
                slug = rest[idx + 1]
                idx += 2
                continue
            print(f"hearth --plugin enter: unknown argument {rest[idx]!r}.", file=stderr)
            return 2

        resolved = resolve_install(install_raw)
        return cmd_plugin_enter(resolved, slug, stdout=stdout, stderr=stderr)

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

    print(
        "hearth --plugin: expected `list`, `enter [--slug SLUG]`, or `--add GIT_URL_OR_PATH`.",
        file=stderr,
    )
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
        return cmd_compose(resolved, ns.compose_args, stderr, env=env)
    if ns.command == "start":
        return cmd_start(resolved, ns.services, stderr, env=env)
    if ns.command == "stop":
        return cmd_stop(resolved, ns.services, stderr, env=env)
    if ns.command == "restart":
        return cmd_restart(resolved, ns.services, stderr, env=env)
    if ns.command == "status":
        return cmd_status(resolved, stdout, stderr, env=env, skip_health=ns.skip_health)
    if ns.command == "logs":
        return cmd_logs(resolved, ns.services, stderr, env=env, follow=ns.follow)
    return _unreachable(ns.command)


def _unreachable(command: str) -> NoReturn:
    raise AssertionError(f"unhandled command: {command}")


def main(argv: list[str] | None = None) -> int:
    return run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
