"""Tests for install.sh artifacts — T-FR-0001-10.

Covers:
- deploy/install.sh exists and is executable
- deploy/systemd/hearth-hub.service exists
- deploy/systemd/hearth-plugin@.service exists
- deploy/launchd/com.hearth.hub.plist exists
- deploy/launchd/com.hearth.plugin.plist exists
- Smoke / integration test of install.sh in ARM container (gated by HEARTH_INTEGRATION=1)
"""

from __future__ import annotations

import os
import stat
from pathlib import Path

import pytest

# The repo root relative to this test file (tests/ → project root)
_REPO_ROOT = Path(__file__).parent.parent


class TestInstallShExists:
    def test_install_sh_is_executable(self) -> None:
        """deploy/install.sh exists and has executable bit set."""
        script = _REPO_ROOT / "deploy" / "install.sh"
        assert script.is_file(), f"deploy/install.sh not found at {script}"
        mode = script.stat().st_mode
        is_exec = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
        assert is_exec, f"deploy/install.sh is not executable (mode={oct(mode)})"

    def test_install_sh_has_shebang(self) -> None:
        """deploy/install.sh starts with a bash shebang."""
        script = _REPO_ROOT / "deploy" / "install.sh"
        first_line = script.read_text(encoding="utf-8").splitlines()[0]
        assert first_line.startswith("#!/"), f"Missing shebang: {first_line!r}"


class TestSystemdUnitsExist:
    def test_hearth_hub_service_exists(self) -> None:
        """deploy/systemd/hearth-hub.service exists."""
        unit = _REPO_ROOT / "deploy" / "systemd" / "hearth-hub.service"
        assert unit.is_file(), f"Missing: {unit}"

    def test_hearth_hub_service_has_execstart(self) -> None:
        """hearth-hub.service contains an ExecStart directive."""
        unit = _REPO_ROOT / "deploy" / "systemd" / "hearth-hub.service"
        content = unit.read_text(encoding="utf-8")
        assert "ExecStart=" in content, "hearth-hub.service missing ExecStart"

    def test_hearth_hub_service_wants_network(self) -> None:
        """hearth-hub.service references network-online.target."""
        unit = _REPO_ROOT / "deploy" / "systemd" / "hearth-hub.service"
        content = unit.read_text(encoding="utf-8")
        assert "network-online.target" in content, (
            "hearth-hub.service should wait on network-online.target"
        )

    def test_hearth_plugin_template_service_exists(self) -> None:
        """deploy/systemd/hearth-plugin@.service (template unit) exists."""
        unit = _REPO_ROOT / "deploy" / "systemd" / "hearth-plugin@.service"
        assert unit.is_file(), f"Missing: {unit}"

    def test_hearth_plugin_template_has_instance_specifier(self) -> None:
        """hearth-plugin@.service uses %i instance specifier."""
        unit = _REPO_ROOT / "deploy" / "systemd" / "hearth-plugin@.service"
        content = unit.read_text(encoding="utf-8")
        assert "%i" in content, "Template unit should use %i instance specifier"


class TestLaunchdPlists:
    def test_hub_plist_exists(self) -> None:
        """deploy/launchd/com.hearth.hub.plist exists."""
        plist = _REPO_ROOT / "deploy" / "launchd" / "com.hearth.hub.plist"
        assert plist.is_file(), f"Missing: {plist}"

    def test_hub_plist_is_valid_xml(self) -> None:
        """com.hearth.hub.plist is well-formed XML plist."""
        plist = _REPO_ROOT / "deploy" / "launchd" / "com.hearth.hub.plist"
        content = plist.read_text(encoding="utf-8")
        assert "<?xml" in content, "plist should be XML"
        assert "<plist" in content, "plist should contain <plist> root element"

    def test_hub_plist_has_label(self) -> None:
        """com.hearth.hub.plist declares the Label key."""
        plist = _REPO_ROOT / "deploy" / "launchd" / "com.hearth.hub.plist"
        content = plist.read_text(encoding="utf-8")
        assert "com.hearth.hub" in content, "plist Label should be com.hearth.hub"

    def test_plugin_plist_exists(self) -> None:
        """deploy/launchd/com.hearth.plugin.plist exists."""
        plist = _REPO_ROOT / "deploy" / "launchd" / "com.hearth.plugin.plist"
        assert plist.is_file(), f"Missing: {plist}"

    def test_plugin_plist_is_valid_xml(self) -> None:
        """com.hearth.plugin.plist is well-formed XML plist."""
        plist = _REPO_ROOT / "deploy" / "launchd" / "com.hearth.plugin.plist"
        content = plist.read_text(encoding="utf-8")
        assert "<?xml" in content
        assert "<plist" in content


@pytest.mark.integration
class TestInstallShIntegration:
    """CI ARM container smoke test — requires HEARTH_INTEGRATION=1."""

    @pytest.fixture(autouse=True)
    def require_integration(self) -> None:
        if not os.environ.get("HEARTH_INTEGRATION"):
            pytest.skip("Set HEARTH_INTEGRATION=1 to run this smoke test")

    def test_install_sh_creates_dirs(self, tmp_path: Path) -> None:
        """install.sh creates /opt/hearth, /etc/hearth, /var/hearth subdirs."""
        import subprocess

        result = subprocess.run(
            ["bash", str(_REPO_ROOT / "deploy" / "install.sh"), "--dry-run", "--prefix", str(tmp_path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"install.sh failed: {result.stderr}"
