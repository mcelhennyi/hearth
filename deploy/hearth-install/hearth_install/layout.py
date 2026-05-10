"""@HRT-OPS-001 Create ``<install-dir>/heart/`` layout idempotently."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from hearth_install.plugin_compose import write_default_plugin_registry
from hearth_install.version_manifest import read_version_manifest

_HEART_SUBDIRS = ("compose", "plugins", "state", "var", "bin")


def _package_templates() -> Path:
    """Directory containing ``templates`` (packaged via setuptools ``package-data``)."""
    return Path(__file__).resolve().parent / "templates"


def ensure_heart_layout(
    install_dir: Path,
    *,
    hearth_ref: str,
    extra_version_fields: dict[str, Any] | None = None,
) -> Path:
    """Ensure ``install_dir/heart`` exists with required dirs and operator files.

    * Creates ``heart/{compose,plugins,state,var,bin}`` if missing.
    * Writes ``heart/README.md`` from the bundled template (overwrites each run so
      template updates propagate; content is non-destructive to operator data).
    * Writes ``heart/VERSION.json`` only if absent; if present, validates schema v1
      and leaves contents unchanged.

    Returns the absolute ``heart`` path.
    """
    install_dir = install_dir.resolve()
    heart = install_dir / "heart"
    heart.mkdir(parents=True, exist_ok=True)
    for name in _HEART_SUBDIRS:
        (heart / name).mkdir(parents=True, exist_ok=True)
    write_default_plugin_registry(heart)

    tpl = _package_templates()
    readme_src = tpl / "README.heart.md"
    shutil.copyfile(readme_src, heart / "README.md")

    version_path = heart / "VERSION.json"
    if version_path.is_file():
        read_version_manifest(version_path)
    else:
        body: dict[str, Any] = {"schema": 1, "hearth_ref": hearth_ref}
        if extra_version_fields:
            overlap = set(body) & set(extra_version_fields)
            if overlap:
                msg = f"extra_version_fields must not override fixed keys: {sorted(overlap)}"
                raise ValueError(msg)
            body.update(extra_version_fields)
        version_path.write_text(
            json.dumps(body, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    return heart
