"""@HRT-OPS-002 Per-plugin ``plugin`` executable (T-FR-0003-11)."""

from __future__ import annotations

import os
import re
import runpy
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import TextIO

from hearth_cli.cli import assemble_docker_compose_command
from hearth_cli.install_context import ResolvedInstall, resolve_install
from hearth_install.plugin_compose import PluginRegistryError, load_plugin_registry
from hearth_install.plugin_lifecycle import (
    PluginLifecycleError,
    remove_plugin_from_install,
    set_plugin_enabled,
)

_SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{0,31}$")
_ENTER_ENV = "HEARTH_PLUGIN_ENTER_FROM"

class PluginCliError(RuntimeError):
    """Operator-facing plugin CLI failure."""



def resolve_plugin_context(plugin_root: Path, env: dict[str, str] | None) -> tuple[ResolvedInstall, str]:
    """Resolve install paths; ``plugin_root`` is ``heart/plugins/<slug>``."""

    plugin_root = plugin_root.resolve()
    slug = plugin_root.name
    if not _SLUG_RE.fullmatch(slug):
        msg = f"invalid plugin directory name {slug!r}"
        raise PluginCliError(msg)
    if plugin_root.parent.name != "plugins":
        msg = f"plugin must live under heart/plugins/<slug>/ (got {plugin_root})"
        raise PluginCliError(msg)

    heart = plugin_root.parent.parent
    if not (heart / "VERSION.json").is_file():
        msg = f"heart directory missing VERSION.json ({heart})"
        raise PluginCliError(msg)

    resolved = resolve_install(str(heart), env=env)
    try:
        rows = load_plugin_registry(resolved.heart_dir)
    except PluginRegistryError as exc:
        raise PluginCliError(str(exc)) from exc

    if not any(r.slug == slug for r in rows):
        msg = f"plugin {slug!r} is not registered in plugins.yaml"
        raise PluginCliError(msg)

    return resolved, slug


def _run_compose_slug(
    resolved: ResolvedInstall,
    slug: str,
    compose_tail: list[str],
    *,
    stderr: TextIO,
    env: dict[str, str] | None,
) -> int:
    if not resolved.compose_file.is_file():
        print(f"plugin: missing compose file {resolved.compose_file}", file=stderr)
        return 1
    cmd, cwd = assemble_docker_compose_command(resolved, compose_tail, env=env)
    try:
        proc = subprocess.run(cmd, cwd=cwd, text=True)
    except FileNotFoundError:
        print("plugin: docker not found on PATH", file=stderr)
        return 1
    return proc.returncode


def _run_hearth_update(resolved: ResolvedInstall, *, stdout: TextIO, stderr: TextIO) -> int:
    """Invoke ``hearth --update`` in-process via ``update_cmd``."""

    from hearth_cli import update_cmd

    def run_proc(argv: list[str], cwd: Path | None) -> subprocess.CompletedProcess[str]:
        if argv and argv[0] == "docker":
            return subprocess.run(argv, cwd=cwd, check=False, text=True)
        return subprocess.run(argv, cwd=cwd, check=False, text=True, capture_output=True)

    return update_cmd.run_update(resolved, dry_run=False, stdout=stdout, stderr=stderr, run_proc=run_proc)


def _confirm_or_abort(
    prompt: str,
    *,
    argv_rest: list[str],
    stdin: TextIO,
    stderr: TextIO,
) -> bool:
    if "--yes" in argv_rest:
        return True
    if not stdin.isatty():
        print(f"plugin: {prompt} (re-run with --yes for non-interactive use)", file=stderr)
        return False
    print(f"{prompt} [yN] ", file=sys.stderr, end="", flush=True)
    reply = stdin.readline()
    return reply.strip().lower() in {"y", "yes"}


def run_plugin_cli(
    plugin_root: Path,
    argv: list[str],
    *,
    env: dict[str, str] | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    stdin: TextIO | None = None,
) -> int:
    """Dispatch Kindling ``plugin`` commands for one plugin checkout."""

    src_env = env if env is not None else os.environ
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    sin = stdin if stdin is not None else sys.stdin

    if not argv or argv[0] in {"-h", "--help", "help"}:
        slug_try = plugin_root.name
        print(
            f"{slug_try} plugin operator CLI\n\n"
            "Lifecycle:\n"
            "  --update     Run hearth --update for this install\n"
            "  --remove --yes   Unregister and delete this plugin (requires --yes)\n"
            "  --enable | --disable   Toggle registry enabled + regenerate compose\n"
            "  --start | --stop   docker compose up -d/stop for this service\n"
            "  --reset [--yes]  Delete mutable data under heart/var/plugins/<slug>/\n"
            "  --exit           Emit `cd` for HEARTH_PLUGIN_ENTER_FROM (from hearth enter)\n"
            "Admin passthrough:\n"
            "  plugin -- <args>   python -m <package>.admin\n",
            file=out,
        )
        return 0

    try:
        resolved, slug = resolve_plugin_context(plugin_root, src_env)
    except PluginCliError as exc:
        print(f"plugin: {exc}", file=err)
        return 1

    if argv[0] == "--":
        return _run_admin(plugin_root, argv[1:], err)

    head, *rest = argv
    if head == "--remove":
        if "--yes" not in rest:
            print("plugin: --remove requires --yes", file=err)
            return 2
        try:
            remove_plugin_from_install(resolved.heart_dir, slug)
        except PluginLifecycleError as exc:
            print(f"plugin: {exc}", file=err)
            return 1
        print(f"plugin: removed {slug}", file=out)
        return 0

    if head == "--update":
        return _run_hearth_update(resolved, stdout=out, stderr=err)

    if head == "--enable":
        try:
            set_plugin_enabled(resolved.heart_dir, slug, enabled=True)
        except PluginLifecycleError as exc:
            print(f"plugin: {exc}", file=err)
            return 1
        return 0

    if head == "--disable":
        try:
            set_plugin_enabled(resolved.heart_dir, slug, enabled=False)
        except PluginLifecycleError as exc:
            print(f"plugin: {exc}", file=err)
            return 1
        return _run_compose_slug(resolved, slug, ["stop", slug], stderr=err, env=src_env)

    if head == "--start":
        return _run_compose_slug(resolved, slug, ["up", "-d", slug], stderr=err, env=src_env)

    if head == "--stop":
        return _run_compose_slug(resolved, slug, ["stop", slug], stderr=err, env=src_env)

    if head == "--reset":
        data_dir = resolved.heart_dir / "var" / "plugins" / slug
        if not _confirm_or_abort(
            f"reset mutable data under {data_dir}?",
            argv_rest=rest,
            stdin=sin,
            stderr=err,
        ):
            return 2
        if data_dir.is_dir():
            shutil.rmtree(data_dir)
        print(f"plugin: reset complete ({data_dir})", file=out)
        return 0

    if head == "--exit":
        previous = src_env.get(_ENTER_ENV, "").strip()
        if not previous:
            print(
                f"plugin: {_ENTER_ENV} is not set (use hearth --plugin enter when available).",
                file=err,
            )
            return 1
        path = Path(previous)
        if not path.is_dir():
            print(f"plugin: {_ENTER_ENV} is not a directory: {previous}", file=err)
            return 1
        print(f"cd {shlex.quote(str(path.resolve()))}")
        return 0

    return _run_admin(plugin_root, argv, err)


def _run_admin(plugin_root: Path, admin_argv: list[str], err: TextIO) -> int:
    """``python -m <pkg>.admin`` for this template."""

    pkg_dir = plugin_root.name.replace("-", "_")
    admin_module = f"{pkg_dir}.admin"
    old_argv = sys.argv[:]
    sys.argv = [admin_module, *admin_argv]
    try:
        runpy.run_module(admin_module, run_name="__main__")
    except ImportError as exc:
        print(f"plugin: admin module {admin_module} not importable ({exc})", file=err)
        return 1
    except SystemExit as exc:
        code = exc.code
        if isinstance(code, int):
            return code
        if code is None:
            return 0
        if isinstance(code, str):
            print(code, file=err)
            return 1
        return 1
    finally:
        sys.argv = old_argv
    return 0
