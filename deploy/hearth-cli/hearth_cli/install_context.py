"""@HRT-OPS-002 Resolve Docker-profile install paths for ``hearth``."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ResolvedInstall:
    """Resolved install paths for a Docker-profile Hearth checkout."""

    install_root: Path
    hearth_dir: Path
    version_path: Path
    compose_file: Path
    compose_env_file: Path


def _looks_like_hearth_app_dir(path: Path) -> bool:
    return (path / "VERSION.json").is_file()


def resolve_install(
    install_root: str | os.PathLike[str] | None = None,
    *,
    env: dict[str, str] | None = None,
) -> ResolvedInstall:
    """Resolve ``<install-root>/hearth`` from CLI args, env, or cwd.

    ``HEARTH_INSTALL_ROOT`` and ``--install-root`` may point either at the parent
    install directory or directly at the ``hearth/`` directory.
    """
    source_env = env if env is not None else os.environ
    raw_root = install_root or source_env.get("HEARTH_INSTALL_ROOT") or Path.cwd()
    candidate = Path(raw_root).expanduser().resolve()
    if _looks_like_hearth_app_dir(candidate):
        hearth_dir = candidate
        root = candidate.parent
    else:
        root = candidate
        hearth_dir = root / "hearth"
    compose_env_file = hearth_dir / "compose" / ".env"
    return ResolvedInstall(
        install_root=root,
        hearth_dir=hearth_dir,
        version_path=hearth_dir / "VERSION.json",
        compose_file=hearth_dir / "compose" / "docker-compose.yml",
        compose_env_file=compose_env_file,
    )


def _repo_root_from_hearth_shim(hearth_dir: Path) -> Path | None:
    """Infer deploy checkout from ``hearth/bin/hearth`` → ``<repo>/bin/hearth`` symlink."""
    shim = hearth_dir / "bin" / "hearth"
    if not shim.is_symlink():
        return None
    try:
        target = shim.resolve()
    except OSError:
        return None
    if target.name != "hearth" or target.parent.name != "bin":
        return None
    repo_root = target.parent.parent
    if (repo_root / "develop").is_file() and (repo_root / "install").is_file():
        return repo_root
    return None


def read_compose_dotenv(path: Path) -> dict[str, str]:
    """Parse a simple KEY=VALUE compose ``.env`` file (no export syntax)."""
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def resolve_deploy_repo_root(
    resolved: ResolvedInstall,
    *,
    env: dict[str, str] | None = None,
) -> Path:
    """Deploy checkout used to build hub images and Mantle static assets.

    Preference: ``HEARTH_REPO_ROOT`` in ``compose/.env`` (written by ``./install``),
    then the process environment, then the ``hearth/bin/hearth`` shim target.
    """
    source_env = env if env is not None else os.environ
    dotenv = read_compose_dotenv(resolved.compose_env_file)
    raw = dotenv.get("HEARTH_REPO_ROOT") or source_env.get("HEARTH_REPO_ROOT")
    if not raw:
        inferred = _repo_root_from_hearth_shim(resolved.hearth_dir)
        if inferred is not None:
            return inferred
        msg = (
            "hearth: HEARTH_REPO_ROOT is not set.\n"
            f"  Expected in: {resolved.compose_env_file}\n"
            "  Fix: from your git checkout, re-run:\n"
            f"    ./install {resolved.install_root}\n"
            "  Or append one line (replace path if your checkout differs):\n"
            f"    echo 'HEARTH_REPO_ROOT=/path/to/hearth' >> {resolved.compose_env_file}\n"
            "  And export HEARTH_INSTALL_ROOT for this shell:\n"
            f"    export HEARTH_INSTALL_ROOT={resolved.install_root}"
        )
        raise ValueError(msg)
    root = Path(raw).expanduser().resolve()
    if not root.is_dir():
        msg = f"hearth: HEARTH_REPO_ROOT is not a directory: {root}"
        raise ValueError(msg)
    return root
