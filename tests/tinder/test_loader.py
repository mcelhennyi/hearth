"""Tests for the Tinder loader — T-FR-0001-03.

Covers every documented validation rule in docs/design/plugin-contract.md.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tinder.loader import load_tinder
from tinder.schema import TinderManifest

FIXTURES = Path(__file__).parent.parent / "fixtures" / "plugins"
REPO_ROOT = Path(__file__).resolve().parents[2]


class TestValidManifest:
    def test_groceries_stub_loads(self) -> None:
        manifest, errors = load_tinder(FIXTURES / "groceries-stub")
        assert errors == [], f"Unexpected errors: {errors}"
        assert isinstance(manifest, TinderManifest)

    def test_groceries_stub_fields(self) -> None:
        manifest, _ = load_tinder(FIXTURES / "groceries-stub")
        assert manifest is not None
        assert manifest.plugin.slug == "groceries-stub"
        assert manifest.plugin.kind == "app"
        assert manifest.plugin.version == "0.1.0"
        assert manifest.entrypoint.ui is not None
        assert manifest.entrypoint.ui.kind == "static"

    def test_capabilities_parsed(self) -> None:
        manifest, _ = load_tinder(FIXTURES / "groceries-stub")
        assert manifest is not None
        assert "list" in manifest.capabilities
        cap = manifest.capabilities["list"]
        assert "add" in cap.methods
        assert "added" in cap.events

    def test_permissions_parsed(self) -> None:
        manifest, _ = load_tinder(FIXTURES / "groceries-stub")
        assert manifest is not None
        assert "groceries-stub.*" in manifest.permissions.spark_publish
        assert "pantry.changed" in manifest.permissions.spark_subscribe

    def test_nav_parsed(self) -> None:
        manifest, _ = load_tinder(FIXTURES / "groceries-stub")
        assert manifest is not None
        assert manifest.ui.nav is not None
        assert manifest.ui.nav.label == "Groceries"
        assert manifest.ui.nav.order == 30

    def test_hearth_users_builtin_manifest_loads(self) -> None:
        manifest, errors = load_tinder(REPO_ROOT / "apps" / "builtin" / "hearth-users")
        assert errors == [], f"Unexpected errors: {errors}"
        assert manifest is not None
        assert manifest.plugin.slug == "hearth-users"
        assert manifest.plugin.builtin is True
        assert manifest.entrypoint.backend.module == "hearth_users.app:create_app"
        assert manifest.capabilities["session"].methods == ["current"]
        assert manifest.capabilities["session"].events == ["login", "logout"]
        assert "hearth-users.*" in manifest.permissions.spark_publish


class TestSlugValidation:
    def test_bad_slug_rejected(self) -> None:
        manifest, errors = load_tinder(FIXTURES / "bad-slug")
        assert manifest is None
        assert any("slug" in e for e in errors), f"Expected slug error, got: {errors}"

    @pytest.mark.parametrize("slug", [
        "Bad",           # uppercase
        "bad slug",      # space
        "bad_slug",      # underscore
        "-bad",          # leading dash
        "a" * 33,        # too long
        "",              # empty
    ])
    def test_invalid_slug_patterns(self, slug: str) -> None:
        from tinder.schema import PluginBlock
        with pytest.raises(Exception):
            PluginBlock(slug=slug, name="Test", version="0.1.0")


class TestKindValidation:
    def test_unknown_kind_rejected(self) -> None:
        manifest, errors = load_tinder(FIXTURES / "unknown-kind")
        assert manifest is None
        assert any("kind" in e.lower() or "plugin" in e.lower() for e in errors), (
            f"Expected kind error, got: {errors}"
        )

    def test_app_without_ui_rejected(self) -> None:
        manifest, errors = load_tinder(FIXTURES / "missing-ui")
        assert manifest is None
        assert any("ui" in e.lower() or "entrypoint" in e.lower() for e in errors), (
            f"Expected ui error, got: {errors}"
        )


class TestSemverValidation:
    def test_bad_semver_rejected(self) -> None:
        manifest, errors = load_tinder(FIXTURES / "bad-semver")
        assert manifest is None
        assert any("semver" in e.lower() or "version" in e.lower() for e in errors), (
            f"Expected semver error, got: {errors}"
        )


class TestMissingFile:
    def test_missing_toml_returns_error(self, tmp_path: Path) -> None:
        manifest, errors = load_tinder(tmp_path)
        assert manifest is None
        assert any("not found" in e for e in errors)

    def test_toml_parse_error_returns_error(self, tmp_path: Path) -> None:
        (tmp_path / "tinder.toml").write_text("this is { not valid toml", encoding="utf-8")
        manifest, errors = load_tinder(tmp_path)
        assert manifest is None
        assert any("TOML" in e or "parse" in e.lower() for e in errors)
