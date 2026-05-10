"""Contract tests for the ``hearth`` operator CLI (T-FR-0003-04)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from hearth_cli import cli


def _write_version(root: Path, *, ref: str = "test-ref") -> Path:
    heart = root / "heart"
    (heart / "compose").mkdir(parents=True)
    (heart / "VERSION.json").write_text(
        json.dumps({"schema": 1, "hearth_ref": ref}) + "\n",
        encoding="utf-8",
    )
    return heart


def test_version_reads_manifest_from_install_root(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_version(tmp_path, ref="abc123")

    code = cli.run(["--install-root", str(tmp_path), "version"])

    assert code == 0
    assert "abc123" in capsys.readouterr().out


def test_resolve_heart_dir_accepts_direct_heart_path(tmp_path: Path) -> None:
    heart = _write_version(tmp_path)

    resolved = cli.resolve_install(install_root=heart)

    assert resolved.install_root == tmp_path.resolve()
    assert resolved.heart_dir == heart.resolve()


def test_doctor_fails_gracefully_without_docker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_version(tmp_path)
    monkeypatch.setattr(cli.shutil, "which", lambda _: None)

    code = cli.run(["--install-root", str(tmp_path), "doctor"])

    captured = capsys.readouterr()
    assert code == 1
    assert "docker: not found" in captured.out
    assert captured.err == ""


def test_compose_passthrough_runs_docker_compose_with_fixture_project(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    heart = _write_version(tmp_path)
    compose_file = heart / "compose" / "docker-compose.yml"
    compose_file.write_text("services: {}\n", encoding="utf-8")
    calls: list[tuple[list[str], Path]] = []

    def fake_run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
        calls.append((command, cwd))
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    code = cli.run(["--install-root", str(tmp_path), "compose", "--", "ps"])

    assert code == 0
    assert calls == [
        (
            ["docker", "compose", "-f", str(compose_file), "ps"],
            heart / "compose",
        )
    ]


def test_global_help_is_available(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        cli.run(["--help"])

    assert exc.value.code == 0
    assert "hearth" in capsys.readouterr().out
