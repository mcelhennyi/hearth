"""Contract tests for ``heart/`` layout and ``VERSION.json`` (T-FR-0003-02)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from hearth_install.layout import ensure_heart_layout
from hearth_install.version_manifest import VersionManifestError, parse_version_manifest, read_version_manifest


def _expected_subdirs(heart: Path) -> tuple[str, ...]:
    return ("compose", "plugins", "state", "var", "bin")


def test_ensure_heart_layout_creates_directories_and_readme(tmp_path: Path) -> None:
    root = tmp_path / "deploy"
    heart = ensure_heart_layout(root, hearth_ref="abc123")
    assert heart == (root / "heart").resolve()
    for name in _expected_subdirs(heart):
        assert (heart / name).is_dir()
    assert (heart / "README.md").is_file()
    text = (heart / "README.md").read_text(encoding="utf-8")
    assert "VERSION.json" in text
    assert (heart / "VERSION.json").is_file()


def test_version_json_parse_round_trip(tmp_path: Path) -> None:
    ensure_heart_layout(tmp_path, hearth_ref="ref-for-test")
    manifest = read_version_manifest(tmp_path / "heart" / "VERSION.json")
    assert manifest.schema == 1
    assert manifest.hearth_ref == "ref-for-test"


def test_ensure_heart_layout_idempotent_version_preserved(tmp_path: Path) -> None:
    ensure_heart_layout(tmp_path, hearth_ref="first")
    first = (tmp_path / "heart" / "VERSION.json").read_text(encoding="utf-8")
    ensure_heart_layout(tmp_path, hearth_ref="second")
    second = (tmp_path / "heart" / "VERSION.json").read_text(encoding="utf-8")
    assert first == second


def test_parse_version_manifest_rejects_bad_schema() -> None:
    with pytest.raises(VersionManifestError):
        parse_version_manifest({"schema": 2, "hearth_ref": "x"})


def test_parse_version_manifest_requires_hearth_ref() -> None:
    with pytest.raises(VersionManifestError):
        parse_version_manifest({"schema": 1})


def test_read_version_manifest_invalid_json(tmp_path: Path) -> None:
    vf = tmp_path / "VERSION.json"
    vf.write_text("{", encoding="utf-8")
    with pytest.raises(VersionManifestError):
        read_version_manifest(vf)


def test_schema_example_file_matches_parser(repo_root: Path) -> None:
    example = (
        repo_root
        / "deploy"
        / "hearth-install"
        / "hearth_install"
        / "templates"
        / "VERSION.json.example"
    )
    data = json.loads(example.read_text(encoding="utf-8"))
    manifest = parse_version_manifest(data)
    assert manifest.schema == 1
    assert manifest.hearth_ref == "main"


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]
