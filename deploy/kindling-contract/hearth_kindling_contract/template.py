"""Render the mirrored Kindling plugin template for Hearth tests and fixtures."""

from __future__ import annotations

import re
import shutil
import stat
from pathlib import Path

_SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{0,31}$")


class KindlingTemplateError(ValueError):
    """Raised when a plugin template cannot be rendered safely."""


def render_plugin_template(parent_dir: Path, *, slug: str) -> Path:
    """Render a minimal Python plugin template under ``parent_dir/slug``.

    This mirrors the planned ``kindling new <slug>`` output until the external
    Kindling repo exists. The template deliberately focuses on the FR-0003
    contract: executable ``plugin``, executable ``scripts/install``, Tinder
    metadata, and admin passthrough to ``python -m <plugin>.admin``.
    """
    if not _SLUG_RE.fullmatch(slug):
        msg = "slug must match ^[a-z][a-z0-9-]{0,31}$"
        raise KindlingTemplateError(msg)

    parent_dir = parent_dir.resolve()
    plugin_root = parent_dir / slug
    if plugin_root.exists():
        msg = f"plugin template destination already exists: {plugin_root}"
        raise KindlingTemplateError(msg)

    package_name = slug.replace("-", "_")
    tokens = {
        "plugin_slug": slug,
        "python_package": package_name,
        "plugin_name": _title_from_slug(slug),
    }

    template_root = Path(__file__).resolve().parent / "templates" / "plugin-python"
    shutil.copytree(template_root, plugin_root)

    package_dir = plugin_root / "package"
    package_target = plugin_root / package_name
    package_dir.rename(package_target)

    for path in plugin_root.rglob("*"):
        if path.is_file():
            _replace_tokens(path, tokens)

    _make_executable(plugin_root / "plugin")
    _make_executable(plugin_root / "scripts" / "install")

    return plugin_root


def _replace_tokens(path: Path, tokens: dict[str, str]) -> None:
    body = path.read_text(encoding="utf-8")
    for key, value in tokens.items():
        body = body.replace("{{ " + key + " }}", value)
    path.write_text(body, encoding="utf-8")


def _make_executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))
