"""Contract tests for the ``hearth`` operator CLI (T-FR-0003-04, T-FR-0003-09)."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from hearth_cli import cli


def _write_version(root: Path, *, ref: str = "test-ref") -> Path:
    hearth = root / "hearth"
    (hearth / "compose").mkdir(parents=True)
    (hearth / "VERSION.json").write_text(
        json.dumps({"schema": 1, "hearth_ref": ref}) + "\n",
        encoding="utf-8",
    )
    return hearth


def test_version_reads_manifest_from_install_root(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_version(tmp_path, ref="abc123")

    code = cli.run(["--install-root", str(tmp_path), "version"])

    assert code == 0
    assert "abc123" in capsys.readouterr().out


def test_resolve_hearth_dir_accepts_direct_hearth_path(tmp_path: Path) -> None:
    hearth = _write_version(tmp_path)

    resolved = cli.resolve_install(install_root=hearth)

    assert resolved.install_root == tmp_path.resolve()
    assert resolved.hearth_dir == hearth.resolve()


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


def _expected_compose_prefix(compose_file: Path, *, env_file: Path | None = None, project: str = "hearth") -> list[str]:
    cmd = [
        "docker",
        "compose",
        "-f",
        str(compose_file),
        "--project-name",
        project,
    ]
    if env_file is not None:
        cmd.extend(["--env-file", str(env_file)])
    return cmd


def test_compose_passthrough_runs_docker_compose_with_fixture_project(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    hearth = _write_version(tmp_path)
    compose_file = hearth / "compose" / "docker-compose.yml"
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
            [*_expected_compose_prefix(compose_file), "ps"],
            hearth / "compose",
        )
    ]


def test_compose_passthrough_includes_env_file_when_compose_dotenv_exists(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    hearth = _write_version(tmp_path)
    compose_file = hearth / "compose" / "docker-compose.yml"
    compose_file.write_text("services: {}\n", encoding="utf-8")
    env_path = hearth / "compose" / ".env"
    env_path.write_text("HUB_HTTP_PORT=8080\n", encoding="utf-8")
    calls: list[list[str]] = []

    def fake_run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    code = cli.run(["--install-root", str(tmp_path), "compose", "--", "config"])

    assert code == 0
    assert calls == [[*_expected_compose_prefix(compose_file, env_file=env_path), "config"]]


def test_compose_uses_project_name_from_env(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    hearth = _write_version(tmp_path)
    compose_file = hearth / "compose" / "docker-compose.yml"
    compose_file.write_text("services: {}\n", encoding="utf-8")
    calls: list[list[str]] = []

    def fake_run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    env = {**os.environ, "HEARTH_COMPOSE_PROJECT_NAME": "pi-home"}
    code = cli.run(["--install-root", str(tmp_path), "compose", "--", "ps"], env=env)

    assert code == 0
    assert calls == [[*_expected_compose_prefix(compose_file, project="pi-home"), "ps"]]


@pytest.mark.parametrize(
    ("extra_argv", "expected_tail"),
    [
        (["start"], ["up", "-d"]),
        (["start", "hub", "db"], ["up", "-d", "hub", "db"]),
        (["stop"], ["stop"]),
        (["stop", "hub"], ["stop", "hub"]),
        (["restart"], ["restart"]),
        (["restart", "hub"], ["restart", "hub"]),
        (["status", "--skip-health"], ["ps", "-a"]),
        (["logs"], ["logs"]),
        (["logs", "hub"], ["logs", "hub"]),
        (["logs", "-f", "hub"], ["logs", "-f", "hub"]),
    ],
)
def test_stack_commands_map_to_compose_invocation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    extra_argv: list[str],
    expected_tail: list[str],
) -> None:
    hearth = _write_version(tmp_path)
    compose_file = hearth / "compose" / "docker-compose.yml"
    compose_file.write_text("services: {}\n", encoding="utf-8")
    calls: list[list[str]] = []

    def fake_run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    code = cli.run(["--install-root", str(tmp_path), *extra_argv])

    assert code == 0
    assert calls == [[*_expected_compose_prefix(compose_file), *expected_tail]]


def test_status_without_skip_health_invokes_ps_then_health_probe(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    hearth = _write_version(tmp_path)
    compose_file = hearth / "compose" / "docker-compose.yml"
    compose_file.write_text("services: {}\n", encoding="utf-8")
    calls: list[list[str]] = []

    def fake_run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        prefix = _expected_compose_prefix(compose_file)
        if command[: len(prefix)] == prefix and command[len(prefix) : len(prefix) + 2] == ["ps", "-a"]:
            return subprocess.CompletedProcess(command, 0)
        return subprocess.CompletedProcess(command, 1)

    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    class _Ok:
        status = 200

        def __enter__(self) -> _Ok:
            return self

        def __exit__(self, *exc: object) -> None:
            return None

    monkeypatch.setattr(cli.urllib.request, "urlopen", lambda _req, timeout=3.0: _Ok())

    env = {**os.environ, "HEARTH_HUB_HEALTH_URL": "http://127.0.0.1:9999/api/health"}
    code = cli.run(["--install-root", str(tmp_path), "status"], env=env)

    assert code == 0
    assert calls[0] == [*_expected_compose_prefix(compose_file), "ps", "-a"]
    out = capsys.readouterr().out
    assert "hub /api/health: HTTP 200" in out
    assert "9999" in out


def test_global_help_is_available(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        cli.run(["--help"])

    assert exc.value.code == 0
    assert "hearth" in capsys.readouterr().out
