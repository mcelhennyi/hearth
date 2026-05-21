"""Resolve plugin *source* paths for hub install (Docker vs host).

When Compose bind-mounts the deploy checkout at ``/workspace``, the hub process
cannot read host paths like ``/home/pi/hearth/apps/groceries`` unless they are
rewritten. ``HEARTH_REPO_ROOT`` (host path from ``compose/.env``) triggers that
mapping; otherwise ``/workspace/...`` and existing paths pass through unchanged.
"""

from __future__ import annotations

import os
from pathlib import Path

_WORKSPACE_ROOT = Path("/workspace")


def resolve_plugin_source_path(source: str) -> Path:
    """Return a path the hub container can use to read ``tinder.toml``."""
    raw = Path(source)
    host_root = os.getenv("HEARTH_REPO_ROOT", "").strip().rstrip("/")
    if host_root:
        src = os.path.normpath(str(raw))
        norm_host = os.path.normpath(host_root)
        if src == norm_host or src.startswith(norm_host + os.sep):
            rel = src[len(norm_host) :].lstrip(os.sep)
            return _WORKSPACE_ROOT / rel
    if raw.is_absolute() and raw.exists():
        return raw
    under_workspace = _WORKSPACE_ROOT / raw
    if under_workspace.exists():
        return under_workspace
    return raw
