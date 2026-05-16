"""@HRT-HUB-003 Minimal ``tinder.toml`` parsing + validation for FR-0003 plugin installs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{0,31}$")
_SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")

_BACKEND_KINDS = frozenset({"python", "node", "binary", "none"})
_UI_KINDS = frozenset({"static", "iframe-spa", "module-federation"})


class TinderManifestError(ValueError):
    """Raised when ``tinder.toml`` is missing required fields or violates MVP rules."""


@dataclass(frozen=True)
class TinderManifest:
    """Fields required for install-time checks (FR-0003 MVP)."""

    slug: str
    name: str
    version: str
    hearth_min: str
    description: str


def load_tinder_manifest(plugin_root: Path, *, raw_text: str | None = None) -> TinderManifest:
    """Parse and validate ``tinder.toml`` under ``plugin_root``.

    This intentionally validates only the slice needed for **T-FR-0003-07**; hub
    loaders may enforce more of ``docs/design/plugin-contract.md``.
    """
    import tomllib

    path = plugin_root / "tinder.toml"
    blob = raw_text if raw_text is not None else path.read_text(encoding="utf-8")
    try:
        data = tomllib.loads(blob)
    except tomllib.TOMLDecodeError as exc:
        msg = f"{path}: invalid TOML ({exc})"
        raise TinderManifestError(msg) from exc

    plugin = data.get("plugin")
    if not isinstance(plugin, dict):
        raise TinderManifestError(f"{path}: missing [plugin] table")

    slug = _required(plugin, "slug")
    if not isinstance(slug, str) or not _SLUG_RE.fullmatch(slug):
        raise TinderManifestError(f"{path}: plugin.slug must match kebab-case rules (see plugin-contract.md)")
    name = _required_str(plugin, path, "name")
    version = _required_str(plugin, path, "version")
    if not _SEMVER_RE.fullmatch(version):
        raise TinderManifestError(f"{path}: plugin.version must be semver-ish (major.minor.patch)")
    hearth_min = _required_str(plugin, path, "hearth_min")
    if not _SEMVER_RE.fullmatch(hearth_min):
        raise TinderManifestError(f"{path}: plugin.hearth_min must use major.minor.patch semver syntax")
    description = _required_str(plugin, path, "description")

    entrypoint = data.get("entrypoint")
    if not isinstance(entrypoint, dict):
        raise TinderManifestError(f"{path}: missing [entrypoint]")

    _validate_backend(entrypoint.get("backend"), path)
    _validate_ui(entrypoint.get("ui"), path)

    return TinderManifest(slug=slug, name=name, version=version, hearth_min=hearth_min, description=description)


def validate_slug_available(slug: str, hearth: Path) -> None:
    """Reject invalid slugs with the same rules as ``plugins.yaml``."""

    if not isinstance(slug, str) or not slug or not _SLUG_RE.fullmatch(slug):
        raise TinderManifestError(f"invalid plugin slug {slug!r}")

    target = hearth / "plugins" / slug
    if target.exists():
        msg = f"plugin directory already exists: {target}"
        raise TinderManifestError(msg)


def _required(tbl: dict[str, Any], key: str) -> Any:
    val = tbl.get(key)
    if val is None:
        raise TinderManifestError(f"missing plugin.{key}")
    return val


def _required_str(tbl: dict[str, Any], path: Path, key: str) -> str:
    val = _required(tbl, key)
    if not isinstance(val, str) or not val.strip():
        raise TinderManifestError(f"{path}: plugin.{key} must be a non-empty string")
    return val


def _validate_backend(value: Any, path: Path) -> None:
    if not isinstance(value, dict):
        raise TinderManifestError(f"{path}: entrypoint.backend must be a table")
    kind = value.get("kind")
    if kind not in _BACKEND_KINDS:
        raise TinderManifestError(f"{path}: unsupported entrypoint.backend.kind {kind!r}")

    if kind == "python":
        module = value.get("module")
        port_env = value.get("port_env")
        if not isinstance(module, str) or ":" not in module:
            raise TinderManifestError(f"{path}: python backend needs module like package.mod:create_app")
        if not isinstance(port_env, str) or not port_env.strip():
            raise TinderManifestError(f"{path}: python backend needs port_env")
    elif kind == "node":
        command = value.get("command")
        port_env = value.get("port_env")
        if not isinstance(command, list) or not all(isinstance(x, str) for x in command):
            raise TinderManifestError(f"{path}: node backend needs command list")
        if not isinstance(port_env, str):
            raise TinderManifestError(f"{path}: node backend needs port_env")
    elif kind == "binary":
        command = value.get("command")
        port_env = value.get("port_env")
        if not isinstance(command, list) or not command:
            raise TinderManifestError(f"{path}: binary backend needs command list")
        if not isinstance(port_env, str):
            raise TinderManifestError(f"{path}: binary backend needs port_env")


def _validate_ui(value: Any, path: Path) -> None:
    if not isinstance(value, dict):
        raise TinderManifestError(f"{path}: entrypoint.ui must be a table")
    kind = value.get("kind")
    if kind not in _UI_KINDS:
        raise TinderManifestError(f"{path}: unsupported entrypoint.ui.kind {kind!r}")

    if kind == "static":
        ui_path = value.get("path")
        if not isinstance(ui_path, str) or not ui_path.strip():
            raise TinderManifestError(f"{path}: static ui requires path")
    elif kind == "iframe-spa":
        base = value.get("base")
        if not isinstance(base, str):
            raise TinderManifestError(f"{path}: iframe-spa ui requires base")
    elif kind == "module-federation":
        remote = value.get("remote")
        if not isinstance(remote, str):
            raise TinderManifestError(f"{path}: module-federation ui requires remote")
