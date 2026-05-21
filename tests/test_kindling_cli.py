"""Round-trip tests for the kindling CLI — T-FR-0001-07.

Phase TEST: verify kindling new + kindling validate work as a round-trip,
and kindling install produces the expected HTTP call to the hub.

Design-gap note: kindling install hits a live hub endpoint; we mock the HTTP
call here rather than spinning up the full FastAPI stack.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from kindling_cli.cli import (
    KindlingError,
    run_install,
    run_new,
    run_validate,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _kindling(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Run ``kindling`` as a subprocess so we exercise the entry-point path."""
    return subprocess.run(
        [sys.executable, "-m", "kindling_cli", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


# ---------------------------------------------------------------------------
# kindling new
# ---------------------------------------------------------------------------

class TestKindlingNew:
    def test_new_creates_plugin_directory(self, tmp_path: Path) -> None:
        run_new("groceries-test", parent=tmp_path)
        plugin_root = tmp_path / "groceries-test"
        assert plugin_root.is_dir()

    def test_new_creates_tinder_toml(self, tmp_path: Path) -> None:
        run_new("groceries-test", parent=tmp_path)
        tinder = tmp_path / "groceries-test" / "tinder.toml"
        assert tinder.is_file()
        content = tinder.read_text()
        assert 'slug = "groceries-test"' in content

    def test_new_creates_python_package(self, tmp_path: Path) -> None:
        run_new("groceries-test", parent=tmp_path)
        pkg_dir = tmp_path / "groceries-test" / "groceries_test"
        assert pkg_dir.is_dir()
        assert (pkg_dir / "__init__.py").is_file()

    def test_new_creates_executable_plugin_script(self, tmp_path: Path) -> None:
        import stat

        run_new("groceries-test", parent=tmp_path)
        plugin_exe = tmp_path / "groceries-test" / "plugin"
        assert plugin_exe.is_file()
        assert bool(plugin_exe.stat().st_mode & stat.S_IXUSR)

    def test_new_rejects_invalid_slug(self, tmp_path: Path) -> None:
        with pytest.raises(KindlingError):
            run_new("Bad_Slug!", parent=tmp_path)

    def test_new_rejects_duplicate(self, tmp_path: Path) -> None:
        run_new("groceries-test", parent=tmp_path)
        with pytest.raises(KindlingError):
            run_new("groceries-test", parent=tmp_path)

    def test_new_subprocess_zero_exit(self, tmp_path: Path) -> None:
        proc = _kindling("new", "groceries-test", "--parent", str(tmp_path))
        assert proc.returncode == 0, proc.stderr

    def test_new_subprocess_nonzero_on_bad_slug(self, tmp_path: Path) -> None:
        proc = _kindling("new", "Bad_Slug!")
        assert proc.returncode != 0


# ---------------------------------------------------------------------------
# kindling validate
# ---------------------------------------------------------------------------

class TestKindlingValidate:
    def test_validate_passes_on_fresh_new_plugin(self, tmp_path: Path) -> None:
        run_new("groceries-test", parent=tmp_path)
        errors = run_validate(tmp_path / "groceries-test")
        assert errors == []

    def test_validate_fails_on_empty_dir(self, tmp_path: Path) -> None:
        plugin_dir = tmp_path / "empty"
        plugin_dir.mkdir()
        errors = run_validate(plugin_dir)
        assert errors  # non-empty list of error strings

    def test_validate_fails_on_bad_tinder_toml(self, tmp_path: Path) -> None:
        plugin_dir = tmp_path / "bad-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "tinder.toml").write_text("[plugin]\nslug = \"bad-plugin\"\n# missing required fields\n")
        errors = run_validate(plugin_dir)
        assert errors

    def test_round_trip_new_then_validate(self, tmp_path: Path) -> None:
        """Core round-trip: kindling new → kindling validate."""
        run_new("groceries-test", parent=tmp_path)
        errors = run_validate(tmp_path / "groceries-test")
        assert errors == [], f"Unexpected validation errors: {errors}"

    def test_validate_subprocess_zero_exit(self, tmp_path: Path) -> None:
        run_new("groceries-test", parent=tmp_path)
        proc = _kindling("validate", str(tmp_path / "groceries-test"))
        assert proc.returncode == 0, proc.stderr

    def test_validate_subprocess_nonzero_on_missing(self, tmp_path: Path) -> None:
        proc = _kindling("validate", str(tmp_path / "does-not-exist"))
        assert proc.returncode != 0


# ---------------------------------------------------------------------------
# kindling install
# ---------------------------------------------------------------------------

class TestKindlingInstall:
    def test_install_posts_to_hub(self, tmp_path: Path) -> None:
        """install calls POST /api/plugins/install with the plugin slug."""
        run_new("groceries-test", parent=tmp_path)
        plugin_dir = tmp_path / "groceries-test"

        posted: list[dict[str, Any]] = []

        def fake_post(url: str, **kwargs: Any) -> MagicMock:
            posted.append({"url": url, "kwargs": kwargs})
            resp = MagicMock()
            resp.status_code = 200
            resp.json.return_value = {"status": "installed"}
            return resp

        import kindling_cli.cli as _cli_mod
        import types

        fake_requests = types.SimpleNamespace(post=fake_post, RequestException=Exception)
        with patch.object(_cli_mod, "requests", fake_requests):
            result = run_install(plugin_dir, hub_url="http://localhost:8200")

        assert result["status"] == "installed"
        assert len(posted) == 1
        assert "/api/plugins/install" in posted[0]["url"]

    def test_install_raises_on_hub_error(self, tmp_path: Path) -> None:
        run_new("groceries-test", parent=tmp_path)
        plugin_dir = tmp_path / "groceries-test"

        def bad_post(url: str, **kwargs: Any) -> MagicMock:
            resp = MagicMock()
            resp.status_code = 500
            resp.text = "internal server error"
            return resp

        import kindling_cli.cli as _cli_mod2
        import types

        fake_requests2 = types.SimpleNamespace(post=bad_post, RequestException=Exception)
        with patch.object(_cli_mod2, "requests", fake_requests2):
            with pytest.raises(KindlingError):
                run_install(plugin_dir, hub_url="http://localhost:8200")

    def test_install_subprocess_help(self) -> None:
        proc = _kindling("install", "--help")
        # help text should print and exit 0
        assert proc.returncode == 0
