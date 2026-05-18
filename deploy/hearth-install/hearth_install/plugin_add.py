"""@HRT-OPS-002 Add Hearth plugins from a git URL or local tree (T-FR-0003-07)."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Protocol, Sequence

from hearth_install.plugin_compose import PluginRecord, generate_plugin_compose, load_plugin_registry, save_plugin_registry
from hearth_install.tinder_manifest import load_tinder_manifest, validate_slug_available


class PluginAddError(RuntimeError):
    """User-facing failure installing a plugin."""

    def __init__(self, message: str, *, exit_code: int = 1) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class _RunnerFn(Protocol):
    def __call__(self, argv: Sequence[str], *, cwd: Path | None) -> subprocess.CompletedProcess[str]:
        ...


def _default_runner(argv: Sequence[str], *, cwd: Path | None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(argv),
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )


def classify_plugin_source(spec: str) -> str:
    """Normalize operator input; reject placeholder registry names."""

    raw = spec.strip()
    if not raw:
        raise PluginAddError("missing plugin source (git URL or directory path)")

    lowered = raw.lower()
    if lowered.startswith(("oci:", "docker:", "docker://")):
        raise PluginAddError(
            "OCI / image-registry plugin installs are not implemented yet. "
            "Pass a git clone URL (https://… or git@…) or a path to a local plugin directory.",
        )

    if "/" not in raw and "~" not in raw and not Path(raw).expanduser().exists():
        raise PluginAddError(
            f"{raw!r} does not look like a git URL or filesystem path. "
            "Registry shorthand / relay resolution is not implemented yet — use an explicit git URL.",
        )

    path_candidate = Path(raw).expanduser()
    if raw.startswith((".", "/", "~")) or path_candidate.exists():
        resolved = path_candidate.resolve()
        if not resolved.is_dir():
            raise PluginAddError(f"local plugin path is not a directory: {resolved}")
        return str(resolved)

    if any(
        raw.startswith(prefix)
        for prefix in ("https://", "http://", "git://", "ssh://", "git@", "file://")
    ):
        return raw

    resolved = path_candidate.resolve()
    if resolved.is_dir():
        return str(resolved)

    raise PluginAddError(
        f"{raw!r} is not an accepted plugin source. "
        "Use https://, http://, ssh://, git://, git@…, file://, or an existing directory path.",
    )


def _git_head(ref: Path, runner: _RunnerFn) -> str | None:
    if not (ref / ".git").exists():
        return None
    proc = runner(["git", "-C", str(ref), "rev-parse", "HEAD"], cwd=None)
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return proc.stdout.strip()


def _materialize_source(source: str, work: Path, runner: _RunnerFn) -> Path:
    clone_dir = work / "plugin-src"
    src_path = Path(source)
    if src_path.is_dir() and (src_path / ".git").exists():
        proc = runner(["git", "clone", "--depth", "1", str(src_path), str(clone_dir)], cwd=None)
        if proc.returncode != 0:
            err = proc.stderr.strip() or proc.stdout.strip() or f"exit {proc.returncode}"
            raise PluginAddError(f"git clone failed for {source}: {err}")
        return clone_dir

    if src_path.is_dir():
        shutil.copytree(src_path, clone_dir, symlinks=True, dirs_exist_ok=False)
        return clone_dir

    proc = runner(["git", "clone", "--depth", "1", source, str(clone_dir)], cwd=None)
    if proc.returncode != 0:
        err = proc.stderr.strip() or proc.stdout.strip() or f"exit {proc.returncode}"
        raise PluginAddError(f"git clone failed for {source}: {err}")
    return clone_dir


def _run_install_hook(plugin_dir: Path, runner: _RunnerFn) -> None:
    script = plugin_dir / "scripts" / "install"
    if not script.is_file():
        return

    if os.name == "posix" and not os.access(script, os.X_OK):
        argv: Sequence[str] = ["/bin/sh", str(script)]
    else:
        argv = [str(script)]

    proc = runner(list(argv), cwd=plugin_dir)
    if proc.returncode != 0:
        combined = (proc.stderr or proc.stdout or "").strip() or f"exit {proc.returncode}"
        raise PluginAddError(f"scripts/install failed: {combined}", exit_code=1)


def format_plugin_list_lines(hearth: Path) -> list[str]:
    records = load_plugin_registry(hearth.resolve())
    slug_w = 22
    src_w = 48
    lines = [
        f"{'SLUG':<{slug_w}} {'SOURCE':<{src_w}} {'EN':>4} VERSION/REF",
        f"{'-' * slug_w} {'-' * src_w} ---- ------------",
    ]
    for record in records:
        ref = record.pinned_ref or "(unpinned)"
        source = record.source_git
        if len(source) > src_w:
            source = source[: src_w - 1] + "…"
        enabled = "yes" if record.enabled else "no"
        lines.append(f"{record.slug:<{slug_w}} {source:<{src_w}} {enabled:>4} {ref}")
    return lines


def add_plugin_from_source(
    *,
    hearth: Path,
    source_spec: str,
    runner: _RunnerFn | None = None,
    start_if_enabled: bool = True,
    compose_runner: _RunnerFn | None = None,
) -> PluginRecord:
    """Clone or copy a plugin, validate Tinder, hook install, update registry, regenerate compose."""

    run = runner or _default_runner
    hearth = hearth.resolve()

    canonical = classify_plugin_source(source_spec)
    work = Path(tempfile.mkdtemp(prefix=".hearth-add-"))
    dest: Path | None = None
    try:
        materialized = _materialize_source(canonical, work, run)
        manifest = load_tinder_manifest(materialized)
        validate_slug_available(manifest.slug, hearth)

        dest = hearth / "plugins" / manifest.slug
        shutil.move(str(materialized), str(dest))
    except PluginAddError:
        shutil.rmtree(work, ignore_errors=True)
        raise
    except Exception:
        shutil.rmtree(work, ignore_errors=True)
        raise
    shutil.rmtree(work, ignore_errors=True)

    try:
        assert dest is not None
        pinned = _git_head(dest, run)
        _run_install_hook(dest, run)

        entries = load_plugin_registry(hearth)
        if any(existing.slug == manifest.slug for existing in entries):
            raise PluginAddError(f"plugin {manifest.slug!r} already listed in plugins.yaml")

        new_rec = PluginRecord(
            slug=manifest.slug,
            source_git=canonical,
            enabled=True,
            pinned_ref=pinned,
        )
        entries.append(new_rec)
        save_plugin_registry(hearth, entries)
        generate_plugin_compose(hearth)

        if start_if_enabled and new_rec.enabled:
            _maybe_start_plugin_services(hearth, [new_rec.slug], run=compose_runner or run)
        return new_rec
    except Exception:
        if dest is not None:
            shutil.rmtree(dest, ignore_errors=True)
        raise


def _maybe_start_plugin_services(hearth: Path, slugs: Sequence[str], *, run: _RunnerFn) -> None:
    compose_file = hearth / "compose" / "docker-compose.yml"
    if not compose_file.is_file():
        return

    overrides = hearth / "compose" / "overrides" / "generated.plugins.yml"
    command = ["docker", "compose", "-f", str(compose_file)]
    if overrides.is_file():
        command.extend(["-f", str(overrides)])
    command.extend(["up", "-d", *slugs])

    proc = run(command, cwd=compose_file.parent)
    if proc.returncode != 0:
        hint = (proc.stderr or proc.stdout or "").strip()
        msg = f"docker compose up reported an error for {', '.join(slugs)}"
        if hint:
            msg = f"{msg}: {hint}"
        raise PluginAddError(msg, exit_code=1)
