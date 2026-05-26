"""@HRT-OPS-002 Sync ``hearth/plugins/<slug>`` from the deploy checkout when install trees are stubs."""

from __future__ import annotations

import shutil
from pathlib import Path

from hearth_install.plugin_compose import PluginRegistryError, load_plugin_registry
from hearth_install.tinder_manifest import TinderManifestError, load_tinder_manifest

# generated.plugins.yml lives under hearth/compose/overrides/
_OVERRIDE_TO_HEARTH = "../.."


def repo_plugin_candidates(repo_root: Path) -> list[Path]:
    candidates: list[Path] = []
    direct = repo_root / "plugins"
    if direct.is_dir():
        for child in sorted(direct.iterdir()):
            if child.is_dir():
                candidates.append(child)
    third_party = repo_root / "plugins" / "third-party"
    if third_party.is_dir():
        for child in sorted(third_party.iterdir()):
            if child.is_dir():
                candidates.append(child)
    return candidates


def find_repo_plugin_root(repo_root: Path, slug: str) -> Path | None:
    for candidate in repo_plugin_candidates(repo_root):
        manifest_path = candidate / "tinder.toml"
        if not manifest_path.is_file():
            continue
        try:
            manifest = load_tinder_manifest(candidate)
        except (OSError, TinderManifestError):
            continue
        if manifest.slug == slug.strip():
            return candidate.resolve()
    return None


def install_plugin_is_complete(install_root: Path) -> bool:
    return (install_root / "Dockerfile").is_file() and (install_root / "tinder.toml").is_file()


def sync_plugin_install_tree(hearth: Path, repo_root: Path, slug: str) -> Path:
    """Ensure ``hearth/plugins/<slug>`` exists; symlink from repo when the install copy is a stub."""
    normalized = slug.strip()
    dest = (hearth / "plugins" / normalized).resolve()
    if install_plugin_is_complete(dest):
        return dest

    src = find_repo_plugin_root(repo_root.resolve(), normalized)
    if src is None:
        return dest

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        if dest.is_symlink():
            dest.unlink()
        elif dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()

    dest.symlink_to(src, target_is_directory=True)
    return dest


def sync_enabled_plugins_from_repo(hearth: Path, repo_root: Path) -> list[Path]:
    """Symlink incomplete install plugin trees from ``HEARTH_REPO_ROOT`` for enabled registry rows."""
    hearth = hearth.resolve()
    repo_root = repo_root.resolve()
    try:
        records = [row for row in load_plugin_registry(hearth) if row.enabled]
    except PluginRegistryError:
        return []

    synced: list[Path] = []
    for record in records:
        synced.append(sync_plugin_install_tree(hearth, repo_root, record.slug))
    return synced
