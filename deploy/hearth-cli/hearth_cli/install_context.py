"""@HRT-OPS-002 Resolve Docker-profile install paths for ``hearth``."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ResolvedInstall:
    """Resolved install paths for a Docker-profile Hearth checkout."""

    install_root: Path
    heart_dir: Path
    version_path: Path
    compose_file: Path


def _looks_like_heart_dir(path: Path) -> bool:
    return (path / "VERSION.json").is_file()


def resolve_install(
    install_root: str | os.PathLike[str] | None = None,
    *,
    env: dict[str, str] | None = None,
) -> ResolvedInstall:
    """Resolve ``<install-root>/heart`` from CLI args, env, or cwd.

    ``HEARTH_INSTALL_ROOT`` and ``--install-root`` may point either at the parent
    install directory or directly at the ``heart/`` directory.
    """
    source_env = env if env is not None else os.environ
    raw_root = install_root or source_env.get("HEARTH_INSTALL_ROOT") or Path.cwd()
    candidate = Path(raw_root).expanduser().resolve()
    if _looks_like_heart_dir(candidate):
        heart_dir = candidate
        root = candidate.parent
    else:
        root = candidate
        heart_dir = root / "heart"
    return ResolvedInstall(
        install_root=root,
        heart_dir=heart_dir,
        version_path=heart_dir / "VERSION.json",
        compose_file=heart_dir / "compose" / "docker-compose.yml",
    )
