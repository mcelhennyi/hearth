"""Tests for ``hearth backup`` and ``hearth restore`` CLI subcommands — T-FR-0001-10.

Covers:
- backup creates a tarball containing hearth.db
- backup honors tinder.toml [backup] include/exclude
- restore unpacks tarball to the correct layout
- restore is idempotent (running twice is safe)
"""

from __future__ import annotations

import io
import tarfile
from pathlib import Path

import pytest

from hearth_cli import backup_cmd


def _make_var_dir(tmp_path: Path) -> Path:
    """Set up a minimal /var/hearth-like directory tree."""
    var = tmp_path / "var" / "hearth"
    (var / "plugins").mkdir(parents=True)
    (var / "secrets").mkdir(parents=True)
    (var / "log").mkdir(parents=True)
    (var / "run").mkdir(parents=True)
    (var / "hearth.db").write_bytes(b"SQLite fake db content")
    return var


def _write_plugin(var: Path, slug: str, *, include_cache: bool = True) -> None:
    """Write a fake plugin data directory."""
    plugin_dir = var / "plugins" / slug
    (plugin_dir / "data").mkdir(parents=True)
    (plugin_dir / "data" / "store.json").write_text('{"key": "value"}', encoding="utf-8")
    if include_cache:
        (plugin_dir / "data" / "cache").mkdir(parents=True)
        (plugin_dir / "data" / "cache" / "cached.dat").write_bytes(b"cache data")


def _write_tinder_toml(plugin_root: Path, *, include: list[str], exclude: list[str]) -> None:
    """Write a minimal tinder.toml with [backup] section."""
    include_list = ", ".join(f'"{p}"' for p in include)
    exclude_list = ", ".join(f'"{p}"' for p in exclude)
    content = f"""\
[plugin]
slug = "{plugin_root.name}"
name = "Test Plugin"
version = "0.1.0"
hearth_min = "0.1.0"
description = "Test plugin for backup tests."

[entrypoint]
backend = {{kind = "none"}}
ui = {{kind = "static", path = "web/dist"}}

[backup]
include = [{include_list}]
exclude = [{exclude_list}]
"""
    (plugin_root / "tinder.toml").write_text(content, encoding="utf-8")


class TestBackupCreatesTarball:
    def test_backup_creates_tarball_with_db(self, tmp_path: Path) -> None:
        """backup creates a .tar.gz containing hearth.db."""
        var = _make_var_dir(tmp_path)
        output_path = tmp_path / "hearth-backup.tar.gz"
        stdout = io.StringIO()
        stderr = io.StringIO()

        code = backup_cmd.cmd_backup(var, output_path, stdout=stdout, stderr=stderr)

        assert code == 0, f"Expected 0, got {code}; stderr={stderr.getvalue()!r}"
        assert output_path.is_file(), "backup file was not created"
        with tarfile.open(output_path, "r:gz") as tf:
            names = tf.getnames()
        assert any("hearth.db" in n for n in names), f"hearth.db not in archive: {names}"

    def test_backup_includes_secrets_dir(self, tmp_path: Path) -> None:
        """backup includes files under secrets/."""
        var = _make_var_dir(tmp_path)
        (var / "secrets" / "vapid.priv").write_bytes(b"secret-key")
        output_path = tmp_path / "hearth-backup.tar.gz"
        stdout = io.StringIO()
        stderr = io.StringIO()

        code = backup_cmd.cmd_backup(var, output_path, stdout=stdout, stderr=stderr)

        assert code == 0
        with tarfile.open(output_path, "r:gz") as tf:
            names = tf.getnames()
        assert any("vapid.priv" in n for n in names), f"vapid.priv not in archive: {names}"

    def test_backup_does_not_include_run_dir(self, tmp_path: Path) -> None:
        """backup must NOT include run/ (sockets)."""
        var = _make_var_dir(tmp_path)
        (var / "run" / "hub.sock").write_bytes(b"")
        output_path = tmp_path / "hearth-backup.tar.gz"
        stdout = io.StringIO()
        stderr = io.StringIO()

        backup_cmd.cmd_backup(var, output_path, stdout=stdout, stderr=stderr)

        with tarfile.open(output_path, "r:gz") as tf:
            names = tf.getnames()
        assert not any("hub.sock" in n for n in names), f"run/hub.sock should not be archived: {names}"

    def test_backup_output_path_reported_to_stdout(self, tmp_path: Path) -> None:
        var = _make_var_dir(tmp_path)
        output_path = tmp_path / "hearth-backup.tar.gz"
        stdout = io.StringIO()
        stderr = io.StringIO()

        backup_cmd.cmd_backup(var, output_path, stdout=stdout, stderr=stderr)

        assert str(output_path) in stdout.getvalue()


class TestBackupPluginIncludeExclude:
    def test_backup_honors_plugin_include(self, tmp_path: Path) -> None:
        """Plugin files under include paths are in the archive."""
        var = _make_var_dir(tmp_path)
        slug = "my-plugin"
        _write_plugin(var, slug, include_cache=False)
        plugin_root = tmp_path / "plugins" / slug
        plugin_root.mkdir(parents=True)
        _write_tinder_toml(
            plugin_root,
            include=[f"plugins/{slug}/"],
            exclude=[],
        )
        output_path = tmp_path / "backup.tar.gz"
        stdout = io.StringIO()
        stderr = io.StringIO()

        code = backup_cmd.cmd_backup(
            var,
            output_path,
            plugin_roots=[plugin_root],
            stdout=stdout,
            stderr=stderr,
        )

        assert code == 0
        with tarfile.open(output_path, "r:gz") as tf:
            names = tf.getnames()
        assert any(f"plugins/{slug}/data/store.json" in n for n in names), (
            f"Plugin data not in archive: {names}"
        )

    def test_backup_honors_plugin_exclude(self, tmp_path: Path) -> None:
        """Plugin cache is excluded when listed in [backup].exclude."""
        var = _make_var_dir(tmp_path)
        slug = "my-plugin"
        _write_plugin(var, slug, include_cache=True)
        plugin_root = tmp_path / "plugins" / slug
        plugin_root.mkdir(parents=True)
        _write_tinder_toml(
            plugin_root,
            include=[f"plugins/{slug}/"],
            exclude=[f"plugins/{slug}/data/cache/"],
        )
        output_path = tmp_path / "backup.tar.gz"
        stdout = io.StringIO()
        stderr = io.StringIO()

        code = backup_cmd.cmd_backup(
            var,
            output_path,
            plugin_roots=[plugin_root],
            stdout=stdout,
            stderr=stderr,
        )

        assert code == 0
        with tarfile.open(output_path, "r:gz") as tf:
            names = tf.getnames()
        assert any(f"plugins/{slug}/data/store.json" in n for n in names), (
            "store.json should be in archive"
        )
        assert not any("cached.dat" in n for n in names), (
            f"cache should not be in archive: {names}"
        )

    def test_backup_with_no_plugin_roots_still_includes_db(self, tmp_path: Path) -> None:
        """When no plugin_roots given, backup still works for hearth.db + secrets."""
        var = _make_var_dir(tmp_path)
        output_path = tmp_path / "backup.tar.gz"
        stdout = io.StringIO()
        stderr = io.StringIO()

        code = backup_cmd.cmd_backup(var, output_path, stdout=stdout, stderr=stderr)

        assert code == 0
        with tarfile.open(output_path, "r:gz") as tf:
            names = tf.getnames()
        assert any("hearth.db" in n for n in names)


class TestRestore:
    def test_restore_unpacks_to_var_dir(self, tmp_path: Path) -> None:
        """restore unpacks hearth.db to the var directory."""
        var_src = _make_var_dir(tmp_path / "source")
        output_path = tmp_path / "backup.tar.gz"
        stdout = io.StringIO()
        stderr = io.StringIO()
        backup_cmd.cmd_backup(var_src, output_path, stdout=stdout, stderr=stderr)

        var_dst = tmp_path / "dest" / "var" / "hearth"
        var_dst.mkdir(parents=True)
        restore_stdout = io.StringIO()
        restore_stderr = io.StringIO()

        code = backup_cmd.cmd_restore(
            var_dst,
            output_path,
            stdout=restore_stdout,
            stderr=restore_stderr,
        )

        assert code == 0, f"Expected 0, got {code}; stderr={restore_stderr.getvalue()!r}"
        assert (var_dst / "hearth.db").is_file(), "hearth.db not restored"
        assert (var_dst / "hearth.db").read_bytes() == b"SQLite fake db content"

    def test_restore_is_idempotent(self, tmp_path: Path) -> None:
        """Running restore twice produces the same result as once."""
        var_src = _make_var_dir(tmp_path / "source")
        output_path = tmp_path / "backup.tar.gz"
        stdout = io.StringIO()
        stderr = io.StringIO()
        backup_cmd.cmd_backup(var_src, output_path, stdout=stdout, stderr=stderr)

        var_dst = tmp_path / "dest" / "var" / "hearth"
        var_dst.mkdir(parents=True)

        for _ in range(2):
            code = backup_cmd.cmd_restore(
                var_dst,
                output_path,
                stdout=io.StringIO(),
                stderr=io.StringIO(),
            )
            assert code == 0

        assert (var_dst / "hearth.db").read_bytes() == b"SQLite fake db content"

    def test_restore_secrets_preserved(self, tmp_path: Path) -> None:
        """Secrets are restored from the archive."""
        var_src = _make_var_dir(tmp_path / "source")
        (var_src / "secrets" / "vapid.priv").write_bytes(b"my-secret")
        output_path = tmp_path / "backup.tar.gz"
        backup_cmd.cmd_backup(
            var_src, output_path, stdout=io.StringIO(), stderr=io.StringIO()
        )

        var_dst = tmp_path / "dest" / "var" / "hearth"
        var_dst.mkdir(parents=True)
        backup_cmd.cmd_restore(
            var_dst, output_path, stdout=io.StringIO(), stderr=io.StringIO()
        )

        assert (var_dst / "secrets" / "vapid.priv").read_bytes() == b"my-secret"

    def test_restore_missing_archive_returns_nonzero(self, tmp_path: Path) -> None:
        """restore returns a non-zero exit code if archive not found."""
        var_dst = tmp_path / "var" / "hearth"
        var_dst.mkdir(parents=True)
        missing = tmp_path / "does-not-exist.tar.gz"

        code = backup_cmd.cmd_restore(
            var_dst, missing, stdout=io.StringIO(), stderr=io.StringIO()
        )

        assert code != 0


class TestBackupCLIIntegration:
    """Test the CLI parser routes backup/restore to the right handlers."""

    def test_backup_subcommand_parsed(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """``hearth backup`` reaches cmd_backup."""
        from hearth_cli import cli

        var = _make_var_dir(tmp_path)
        output_path = tmp_path / "out.tar.gz"
        calls: list[tuple] = []

        def fake_backup(var_dir: Path, out: Path, *, plugin_roots=None, stdout=None, stderr=None) -> int:
            calls.append((var_dir, out))
            return 0

        monkeypatch.setattr(backup_cmd, "cmd_backup", fake_backup)

        env = {
            "HEARTH_VAR_DIR": str(var),
        }
        code = cli.run(
            ["backup", "--output", str(output_path)],
            env=env,
        )

        assert code == 0
        assert len(calls) == 1

    def test_restore_subcommand_parsed(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """``hearth restore`` reaches cmd_restore."""
        from hearth_cli import cli

        var = _make_var_dir(tmp_path)
        archive_path = tmp_path / "backup.tar.gz"
        archive_path.write_bytes(b"fake")
        calls: list[tuple] = []

        def fake_restore(var_dir: Path, archive: Path, *, stdout=None, stderr=None) -> int:
            calls.append((var_dir, archive))
            return 0

        monkeypatch.setattr(backup_cmd, "cmd_restore", fake_restore)

        env = {
            "HEARTH_VAR_DIR": str(var),
        }
        code = cli.run(
            ["restore", str(archive_path)],
            env=env,
        )

        assert code == 0
        assert len(calls) == 1
