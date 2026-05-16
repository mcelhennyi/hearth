"""Tests for ``hearth --update`` (T-FR-0003-06)."""

from __future__ import annotations

import io
import json
import subprocess
from pathlib import Path

import pytest

from hearth_cli import cli
from hearth_cli.update_cmd import run_update


def _make_version(hearth: Path, *, ref: str = "aaa") -> None:
    hearth.mkdir(parents=True, exist_ok=True)
    (hearth / "VERSION.json").write_text(
        json.dumps({"schema": 1, "hearth_ref": ref}) + "\n",
        encoding="utf-8",
    )
    (hearth / "compose").mkdir(parents=True, exist_ok=True)
    (hearth / "state").mkdir(parents=True, exist_ok=True)
    (hearth / "plugins").mkdir(parents=True, exist_ok=True)
    (hearth / "compose" / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")


def _fake_completed(code: int = 0, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess([], code, stdout, stderr)


def test_update_dry_run_skips_mutations(tmp_path: Path) -> None:
    root = tmp_path
    hearth = root / "hearth"
    _make_version(hearth)
    calls: list[tuple[list[str], Path | None]] = []

    def fake_run(argv: list[str], cwd: Path | None) -> subprocess.CompletedProcess[str]:
        calls.append((list(argv), cwd))
        if argv[:3] == ["git", "rev-parse", "--show-toplevel"]:
            return _fake_completed(0, f"{root.resolve()}\n")
        if argv[:3] == ["git", "rev-parse", "HEAD"]:
            return _fake_completed(0, "deadbeef\n")
        raise AssertionError(argv)

    out = io.StringIO()
    err = io.StringIO()
    resolved = cli.resolve_install(root)
    code = run_update(resolved, dry_run=True, stdout=out, stderr=err, run_proc=fake_run)

    assert code == 0
    combined = out.getvalue() + err.getvalue()
    assert "dry-run" in combined
    assert not any(c[0][:2] == ["git", "pull"] for c in calls)


def test_update_pull_unchanged_deploy_ref_writes_compose_and_composes_up(tmp_path: Path) -> None:
    root = tmp_path
    hearth = root / "hearth"
    _make_version(hearth)
    head_calls = 0

    def fake_run(argv: list[str], cwd: Path | None) -> subprocess.CompletedProcess[str]:
        nonlocal head_calls
        if argv[:3] == ["git", "rev-parse", "--show-toplevel"]:
            return _fake_completed(0, f"{root.resolve()}\n")
        if argv[:3] == ["git", "rev-parse", "HEAD"]:
            head_calls += 1
            return _fake_completed(0, "aaa1111\n")
        if argv[:3] == ["git", "pull", "--ff-only"]:
            return _fake_completed(0, "", "")
        if argv[:2] == ["docker", "compose"]:
            assert "--pull" in argv
            assert argv[-2:] == ["up", "-d"] or "up" in argv
            return _fake_completed(0, "", "")
        raise AssertionError(argv)

    out = io.StringIO()
    err = io.StringIO()
    resolved = cli.resolve_install(root)
    code = run_update(resolved, dry_run=False, stdout=out, stderr=err, run_proc=fake_run)

    assert code == 0
    assert "unchanged (aaa1111)" in out.getvalue()
    assert (hearth / "compose" / "overrides" / "generated.plugins.yml").is_file()
    assert head_calls == 2


def test_update_changed_deploy_ref_updates_version_json(tmp_path: Path) -> None:
    root = tmp_path
    hearth = root / "hearth"
    _make_version(hearth, ref="oldref")
    head_i = 0

    def fake_run(argv: list[str], cwd: Path | None) -> subprocess.CompletedProcess[str]:
        nonlocal head_i
        if argv[:3] == ["git", "rev-parse", "--show-toplevel"]:
            return _fake_completed(0, f"{root.resolve()}\n")
        if argv[:3] == ["git", "rev-parse", "HEAD"]:
            head_i += 1
            return _fake_completed(0, ("111\n" if head_i == 1 else "222\n"))
        if argv[:3] == ["git", "pull", "--ff-only"]:
            return _fake_completed(0, "", "")
        if argv[:2] == ["docker", "compose"]:
            return _fake_completed(0, "", "")
        raise AssertionError(argv)

    out = io.StringIO()
    err = io.StringIO()
    resolved = cli.resolve_install(root)
    code = run_update(resolved, dry_run=False, stdout=out, stderr=err, run_proc=fake_run)

    assert code == 0
    data = json.loads((hearth / "VERSION.json").read_text(encoding="utf-8"))
    assert data["hearth_ref"] == "222"
    assert "111 -> 222" in out.getvalue()


def test_update_fails_without_git(tmp_path: Path) -> None:
    root = tmp_path
    hearth = root / "hearth"
    _make_version(hearth)

    def fake_run(argv: list[str], cwd: Path | None) -> subprocess.CompletedProcess[str]:
        if argv[:3] == ["git", "rev-parse", "--show-toplevel"]:
            return _fake_completed(1, "", "not a git repository\n")
        raise AssertionError(argv)

    out = io.StringIO()
    err = io.StringIO()
    resolved = cli.resolve_install(root)
    code = run_update(resolved, dry_run=True, stdout=out, stderr=err, run_proc=fake_run)

    assert code == 1


def test_cli_update_runs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path
    hearth = root / "hearth"
    _make_version(hearth)
    head_i = 0

    def fake_run(argv: list[str], cwd: Path | None) -> subprocess.CompletedProcess[str]:
        nonlocal head_i
        if argv[:3] == ["git", "rev-parse", "--show-toplevel"]:
            return _fake_completed(0, f"{root.resolve()}\n")
        if argv[:3] == ["git", "rev-parse", "HEAD"]:
            head_i += 1
            return _fake_completed(0, "aaa1111\n")
        if argv[:3] == ["git", "pull", "--ff-only"]:
            return _fake_completed(0, "", "")
        if argv[:2] == ["docker", "compose"]:
            return _fake_completed(0, "", "")
        raise AssertionError(argv)

    monkeypatch.setattr("hearth_cli.update_cmd._default_run_proc", fake_run)

    code = cli.run(["--install-root", str(root), "--update"])

    assert code == 0


def test_cli_rejects_update_with_subcommand() -> None:
    with pytest.raises(SystemExit) as exc:
        cli.run(["--update", "version"])

    assert exc.value.code == 2


def test_cli_requires_command_without_update(capsys: pytest.CaptureFixture[str]) -> None:
    code = cli.run([])

    assert code == 2
