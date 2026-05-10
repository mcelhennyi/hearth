"""@HRT-OPS-001 Parse and validate ``heart/VERSION.json`` (schema v1)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


class VersionManifestError(ValueError):
    """Raised when ``VERSION.json`` is missing required fields or wrong schema."""


@dataclass(frozen=True)
class VersionManifestV1:
    """In-memory representation of a v1 install manifest."""

    schema: int
    hearth_ref: str
    installed_at: str | None


def parse_version_manifest(data: Mapping[str, Any]) -> VersionManifestV1:
    """Validate a decoded JSON object against VERSION.json schema v1."""
    if not isinstance(data, Mapping):
        msg = "VERSION.json root must be a JSON object"
        raise VersionManifestError(msg)
    schema = data.get("schema")
    if schema != 1:
        msg = f'expected "schema": 1, got {schema!r}'
        raise VersionManifestError(msg)
    ref = data.get("hearth_ref")
    if not isinstance(ref, str) or not ref.strip():
        msg = 'expected non-empty string "hearth_ref"'
        raise VersionManifestError(msg)
    installed = data.get("installed_at")
    if installed is not None and not isinstance(installed, str):
        msg = '"installed_at", if present, must be a string'
        raise VersionManifestError(msg)
    return VersionManifestV1(schema=1, hearth_ref=ref.strip(), installed_at=installed)


def read_version_manifest(path: Path) -> VersionManifestV1:
    """Load and parse ``VERSION.json`` from disk."""
    raw = path.read_text(encoding="utf-8")
    try:
        decoded = json.loads(raw)
    except json.JSONDecodeError as exc:
        msg = f"invalid JSON in {path}: {exc}"
        raise VersionManifestError(msg) from exc
    return parse_version_manifest(decoded)
