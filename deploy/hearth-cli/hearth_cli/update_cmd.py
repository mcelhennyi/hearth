"""@HRT-OPS-002 Implement ``hearth --update`` (T-FR-0003-06)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TextIO

from hearth_cli.install_context import ResolvedInstall
from hearth_install.plugin_compose import PluginRegistryError, generate_plugin_compose, load_plugin_registry
from hearth_install.version_manifest import VersionManifestError, parse_version_manifest, read_version_manifest

RunProc = Callable[[list[str], Path | None], subprocess.CompletedProcess[str]]


def _default_run_proc(argv: list[str], cwd: Path | None) -> subprocess.CompletedProcess[str]:
    # Stream docker compose to the terminal; keep git/migrate output captured for parsing.
    if argv and argv[0] == "docker":
        return subprocess.run(argv, cwd=cwd, check=False, text=True)
    return subprocess.run(argv, cwd=cwd, check=False, text=True, capture_output=True)


def _find_git_toplevel(search: Sequence[Path], run_proc: RunProc) -> Path | None:
    for base in search:
        if not base.is_dir():
            continue
        proc = run_proc(["git", "rev-parse", "--show-toplevel"], cwd=base)
        if proc.returncode == 0 and proc.stdout:
            return Path(proc.stdout.strip()).resolve()
    return None


def _git_head(repo: Path, run_proc: RunProc) -> str | None:
    proc = run_proc(["git", "rev-parse", "HEAD"], cwd=repo)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def _rewrite_version_hearth_ref(version_path: Path, new_ref: str) -> None:
    raw = json.loads(version_path.read_text(encoding="utf-8"))
    parse_version_manifest(raw)
    raw["hearth_ref"] = new_ref
    version_path.write_text(
        json.dumps(raw, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _maybe_run_migrate_hook(
    hearth_dir: Path,
    *,
    dry_run: bool,
    stdout: TextIO,
    run_proc: RunProc,
) -> int:
    """Run ``hearth/bin/hearth-migrate`` when the hub/install supplies an executable hook."""
    script = hearth_dir / "bin" / "hearth-migrate"
    if not script.is_file():
        return 0
    if not os.access(script, os.X_OK):
        print(f"hearth --update: skip non-executable migration hook {script}", file=stdout)
        return 0
    if dry_run:
        print(f"hearth --update: dry-run: would run {script}", file=stdout)
        return 0
    proc = run_proc([str(script)], cwd=hearth_dir)
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip()
        print(f"hearth --update: migrate hook failed ({proc.returncode}): {tail}", file=stdout)
        return proc.returncode
    return 0


def _docker_compose(
    compose_file: Path,
    compose_args: list[str],
    *,
    run_proc: RunProc,
) -> int:
    command = ["docker", "compose", "-f", str(compose_file), *compose_args]
    proc = run_proc(command, cwd=compose_file.parent)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    return proc.returncode


def _refresh_plugins(
    hearth_dir: Path,
    *,
    dry_run: bool,
    stdout: TextIO,
    run_proc: RunProc,
) -> int:
    registry_path = hearth_dir / "state" / "plugins.yaml"
    if dry_run and not registry_path.is_file():
        return 0
    try:
        records = load_plugin_registry(hearth_dir)
    except PluginRegistryError as exc:
        print(f"hearth --update: plugin registry: {exc}", file=stdout)
        return 1

    exit_code = 0
    for record in records:
        if not record.enabled:
            continue
        plugin_root = hearth_dir / "plugins" / record.slug
        if not (plugin_root / ".git").exists():
            continue
        before = _git_head(plugin_root, run_proc)
        if before is None:
            print(f"hearth --update: plugin {record.slug}: could not read HEAD", file=stdout)
            exit_code = 1
            continue
        if dry_run:
            print(f"hearth --update: dry-run: would refresh plugin {record.slug} ({before[:7]})", file=stdout)
            continue
        if record.pinned_ref:
            fetch = run_proc(["git", "fetch", "origin"], cwd=plugin_root)
            if fetch.returncode != 0:
                print(
                    f"hearth --update: plugin {record.slug}: git fetch failed: "
                    f"{(fetch.stderr or fetch.stdout or '').strip()}",
                    file=stdout,
                )
                exit_code = 1
                continue
            co = run_proc(["git", "checkout", record.pinned_ref], cwd=plugin_root)
            if co.returncode != 0:
                print(
                    f"hearth --update: plugin {record.slug}: checkout {record.pinned_ref!r} failed: "
                    f"{(co.stderr or co.stdout or '').strip()}",
                    file=stdout,
                )
                exit_code = 1
                continue
        else:
            pull = run_proc(["git", "pull", "--ff-only"], cwd=plugin_root)
            if pull.returncode != 0:
                print(
                    f"hearth --update: plugin {record.slug}: git pull failed: "
                    f"{(pull.stderr or pull.stdout or '').strip()}",
                    file=stdout,
                )
                exit_code = 1
                continue
        after = _git_head(plugin_root, run_proc)
        if after and after != before:
            print(f"hearth --update: plugin {record.slug}: {before} -> {after}", file=stdout)
        else:
            print(f"hearth --update: plugin {record.slug}: unchanged ({before})", file=stdout)

    return exit_code


def run_update(
    resolved: ResolvedInstall,
    *,
    dry_run: bool,
    stdout: TextIO,
    stderr: TextIO,
    run_proc: RunProc | None = None,
) -> int:
    """Fetch latest deploy sources, regenerate compose, and restart the stack."""
    runner = run_proc or _default_run_proc
    hearth = resolved.hearth_dir
    if not hearth.is_dir():
        print(f"hearth --update: missing hearth directory {hearth}", file=stderr)
        return 1
    if not resolved.compose_file.is_file():
        print(f"hearth --update: missing compose file {resolved.compose_file}", file=stderr)
        return 1

    try:
        read_version_manifest(resolved.version_path)
    except (OSError, VersionManifestError) as exc:
        print(f"hearth --update: VERSION.json: {exc}", file=stderr)
        return 1

    git_root = _find_git_toplevel((resolved.install_root, hearth.parent, hearth), runner)
    if git_root is None:
        print(
            "hearth --update: deploy checkout is not a git repository "
            "(expected git at install root or parent of hearth/)",
            file=stderr,
        )
        return 1

    before = _git_head(git_root, runner)
    if before is None:
        print(f"hearth --update: could not read HEAD under {git_root}", file=stderr)
        return 1

    if dry_run:
        print(f"hearth --update: dry-run: deploy at {git_root}", file=stdout)
        print(f"hearth --update: dry-run: current deploy ref {before}", file=stdout)
        print("hearth --update: dry-run: would git pull --ff-only", file=stdout)
    else:
        pull = runner(["git", "pull", "--ff-only"], cwd=git_root)
        if pull.returncode != 0:
            msg = (pull.stderr or pull.stdout or "git pull failed").strip()
            print(f"hearth --update: {msg}", file=stderr)
            return pull.returncode
        after_pull = _git_head(git_root, runner)
        if after_pull is None:
            print("hearth --update: could not read HEAD after pull", file=stderr)
            return 1
        if after_pull != before:
            print(f"hearth --update: deploy ref {before} -> {after_pull}", file=stdout)
            try:
                _rewrite_version_hearth_ref(resolved.version_path, after_pull)
            except (OSError, VersionManifestError, json.JSONDecodeError) as exc:
                print(f"hearth --update: could not update VERSION.json: {exc}", file=stderr)
                return 1
        else:
            print(f"hearth --update: deploy ref unchanged ({before})", file=stdout)

    plug_code = _refresh_plugins(hearth, dry_run=dry_run, stdout=stdout, run_proc=runner)
    if plug_code != 0:
        return plug_code

    if dry_run:
        print("hearth --update: dry-run: would regenerate plugin compose override", file=stdout)
    else:
        try:
            out = generate_plugin_compose(hearth)
            print(f"hearth --update: wrote {out}", file=stdout)
        except PluginRegistryError as exc:
            print(f"hearth --update: compose generation failed: {exc}", file=stderr)
            return 1

    mig = _maybe_run_migrate_hook(hearth, dry_run=dry_run, stdout=stdout, run_proc=runner)
    if mig != 0:
        return mig

    if dry_run:
        print(
            "hearth --update: dry-run: would run "
            f"docker compose -f {resolved.compose_file} up -d --pull always",
            file=stdout,
        )
        return 0

    code = _docker_compose(
        resolved.compose_file,
        ["up", "-d", "--pull", "always"],
        run_proc=runner,
    )
    if code != 0:
        print(f"hearth --update: docker compose up failed ({code})", file=stderr)
    return code
