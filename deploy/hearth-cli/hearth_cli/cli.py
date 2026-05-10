"""@HRT-OPS-002 Core ``hearth`` operator CLI for the Docker profile."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn, TextIO

from hearth_install.version_manifest import VersionManifestError, VersionManifestV1, read_version_manifest

_DEFAULT_COMPOSE_PROJECT = "hearth"
_HUB_HEALTH_PATH = "/api/health"
_HUB_INTERNAL_PORTS = ("8000", "8080", "80")


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
    otherwise ``heart/compose/.env`` when present.
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
        "--project-name",
        compose_project_name(env=env),
    ]
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
