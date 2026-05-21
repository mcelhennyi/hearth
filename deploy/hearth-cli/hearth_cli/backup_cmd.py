"""@HRT-OPS-010 ``hearth backup`` and ``hearth restore`` subcommands — T-FR-0001-10.

Backup layout (per docs/design/deployment.md):
    hearth-backup-YYYYMMDD-HHMM.tar.gz
    ├── hearth.db
    ├── plugins/<slug>/...   (paths in tinder.toml [backup].include, minus excludes)
    └── secrets/             (always included)

run/ is explicitly excluded (sockets, ephemeral).

Restore: unpacks the archive to <var_dir>, overwriting existing files.
Idempotent: running restore twice on the same archive produces the same result.
"""

from __future__ import annotations

import tarfile
from pathlib import Path
from typing import IO, TextIO


def _read_backup_config(tinder_toml: Path) -> tuple[list[str], list[str]]:
    """Parse [backup] include and exclude from tinder.toml.

    Returns (include, exclude) as lists of path strings.
    Falls back to empty lists if tinder.toml has no [backup] section.
    """
    import tomllib

    try:
        data = tomllib.loads(tinder_toml.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return [], []

    backup = data.get("backup")
    if not isinstance(backup, dict):
        return [], []

    include = backup.get("include", [])
    exclude = backup.get("exclude", [])

    if not isinstance(include, list):
        include = []
    if not isinstance(exclude, list):
        exclude = []

    return [str(p) for p in include], [str(p) for p in exclude]


def _is_excluded(rel_path: str, exclude_prefixes: list[str]) -> bool:
    """Return True if rel_path starts with any exclude prefix (normalised)."""
    for prefix in exclude_prefixes:
        norm_prefix = prefix.rstrip("/")
        norm_path = rel_path
        if norm_path == norm_prefix or norm_path.startswith(norm_prefix + "/"):
            return True
    return False


def _add_path_to_tar(
    tf: tarfile.TarFile,
    abs_path: Path,
    arcname: str,
    exclude_prefixes: list[str],
) -> None:
    """Recursively add abs_path to tf under arcname, honouring excludes."""
    if abs_path.is_dir():
        for child in sorted(abs_path.iterdir()):
            child_arcname = f"{arcname}/{child.name}"
            if _is_excluded(child_arcname, exclude_prefixes):
                continue
            _add_path_to_tar(tf, child, child_arcname, exclude_prefixes)
    elif abs_path.is_file():
        if not _is_excluded(arcname, exclude_prefixes):
            tf.add(abs_path, arcname=arcname, recursive=False)


def cmd_backup(
    var_dir: Path,
    output_path: Path,
    *,
    plugin_roots: list[Path] | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Create a backup archive from var_dir.

    Args:
        var_dir: /var/hearth or equivalent mutable data directory.
        output_path: destination .tar.gz file path.
        plugin_roots: optional list of plugin checkout roots containing
            tinder.toml with [backup] include/exclude.  Each root's
            tinder.toml is read for include/exclude; the matching paths
            under var_dir are then archived.
        stdout: stream for progress messages.
        stderr: stream for error messages.

    Returns exit code (0 = success).
    """
    import sys

    if stdout is None:
        stdout = sys.stdout
    if stderr is None:
        stderr = sys.stderr

    # Always-included paths relative to var_dir (run/ is always excluded).
    core_entries: list[tuple[Path, str]] = []

    db_path = var_dir / "hearth.db"
    if db_path.is_file():
        core_entries.append((db_path, "hearth.db"))

    secrets_dir = var_dir / "secrets"
    if secrets_dir.is_dir():
        core_entries.append((secrets_dir, "secrets"))

    # Plugin entries from tinder.toml [backup] include/exclude
    plugin_entries: list[tuple[Path, str, list[str]]] = []
    if plugin_roots:
        for plugin_root in plugin_roots:
            tinder_toml = plugin_root / "tinder.toml"
            if not tinder_toml.is_file():
                continue
            include, exclude = _read_backup_config(tinder_toml)
            for inc_path in include:
                norm = inc_path.rstrip("/")
                abs_inc = var_dir / norm
                if abs_inc.exists():
                    plugin_entries.append((abs_inc, norm, exclude))

    try:
        with tarfile.open(output_path, "w:gz") as tf:
            for abs_path, arcname in core_entries:
                if abs_path.is_dir():
                    _add_path_to_tar(tf, abs_path, arcname, [])
                elif abs_path.is_file():
                    tf.add(abs_path, arcname=arcname, recursive=False)

            for abs_path, arcname, excludes in plugin_entries:
                _add_path_to_tar(tf, abs_path, arcname, excludes)

    except OSError as exc:
        print(f"hearth backup: {exc}", file=stderr)
        return 1

    print(f"hearth backup: created {output_path}", file=stdout)
    return 0


def cmd_restore(
    var_dir: Path,
    archive_path: Path,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Restore a backup archive into var_dir.

    Idempotent: running restore twice on the same archive yields the same
    directory state (files are overwritten).

    Args:
        var_dir: destination /var/hearth or equivalent mutable data directory.
        archive_path: path to .tar.gz backup created by cmd_backup.
        stdout: stream for progress messages.
        stderr: stream for error messages.

    Returns exit code (0 = success).
    """
    import sys

    if stdout is None:
        stdout = sys.stdout
    if stderr is None:
        stderr = sys.stderr

    if not archive_path.is_file():
        print(f"hearth restore: archive not found: {archive_path}", file=stderr)
        return 1

    try:
        with tarfile.open(archive_path, "r:gz") as tf:
            # extractall with filter="data" (Python 3.12+) prevents path traversal.
            try:
                tf.extractall(var_dir, filter="data")
            except TypeError:
                # Python < 3.12 fallback (not expected in our 3.12 container).
                tf.extractall(var_dir)  # noqa: S202
    except (tarfile.TarError, OSError) as exc:
        print(f"hearth restore: {exc}", file=stderr)
        return 1

    print(f"hearth restore: restored to {var_dir}", file=stdout)
    return 0
