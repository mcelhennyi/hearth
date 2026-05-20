"""Tinder manifest loader — reads and validates tinder.toml per plugin-contract.md.

Usage::

    manifest, errors = load_tinder(Path("/apps/groceries"))
    if errors:
        # install with state='disabled', surface errors
    else:
        # proceed with manifest.plugin.slug etc.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from pydantic import ValidationError

from tinder.schema import TinderManifest


def load_tinder(plugin_dir: Path) -> tuple[TinderManifest | None, list[str]]:
    """Load and validate the tinder.toml from *plugin_dir*.

    Returns ``(manifest, [])`` on success, ``(None, errors)`` on failure.
    Never raises; all exceptions are captured into the error list.
    """
    toml_path = plugin_dir / "tinder.toml"

    if not toml_path.exists():
        return None, [f"tinder.toml not found at {toml_path}"]

    try:
        raw = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return None, [f"TOML parse error: {exc}"]
    except OSError as exc:
        return None, [f"Could not read tinder.toml: {exc}"]

    # Flatten capabilities.* sub-tables into the 'capabilities' dict Pydantic expects.
    # TOML represents [capabilities.list] as raw["capabilities"]["list"] already.

    try:
        manifest = TinderManifest.model_validate(raw)
    except ValidationError as exc:
        errors = [f"{'.'.join(str(p) for p in e['loc'])}: {e['msg']}" for e in exc.errors()]
        return None, errors

    return manifest, []
