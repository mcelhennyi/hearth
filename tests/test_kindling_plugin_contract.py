"""Contract tests for the Hearth-side Kindling plugin template mirror (T-FR-0003-10)."""

from __future__ import annotations

import hashlib
import hmac
import importlib
import os
import stat
import subprocess
import sys
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from hearth_kindling_contract import KindlingTemplateError, render_plugin_template


def _is_executable(path: Path) -> bool:
    return bool(path.stat().st_mode & stat.S_IXUSR)


def _signed_headers(
    *,
    secret: str,
    method: str = "GET",
    path: str = "/api/me",
    user_id: str = "local",
    name: str = "Local User",
    roles: str | None = None,
    ts: int | None = None,
) -> dict[str, str]:
    ts_text = str(int(time.time()) if ts is None else ts)
    payload = "\n".join([user_id, ts_text, method.upper(), path]).encode("utf-8")
    sig = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    headers = {
        "X-Hearth-User-Id": user_id,
        "X-Hearth-User-Ts": ts_text,
        "X-Hearth-User-Sig": sig,
        "X-Hearth-User-Name": name,
    }
    if roles is not None:
        headers["X-Hearth-Roles"] = roles
    return headers


def _rendered_app_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")
    monkeypatch.setenv("HEARTH_USER_SIG_SECRET", "test-secret")
    monkeypatch.syspath_prepend(str(plugin_root))
    for module_name in ["sample_plugin.app", "sample_plugin.trust", "sample_plugin"]:
        sys.modules.pop(module_name, None)
    app_module = importlib.import_module("sample_plugin.app")
    return TestClient(app_module.create_app())


def test_render_plugin_template_creates_plugin_executable_and_install_hook(
    tmp_path: Path,
) -> None:
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")

    assert plugin_root == tmp_path / "sample-plugin"
    assert (plugin_root / "tinder.toml").read_text(encoding="utf-8").startswith(
        '[plugin]\nslug = "sample-plugin"'
    )
    assert _is_executable(plugin_root / "plugin")
    assert _is_executable(plugin_root / "scripts" / "install")
    assert (plugin_root / "sample_plugin" / "admin.py").is_file()
    assert (plugin_root / "sample_plugin" / "app.py").is_file()
    assert (plugin_root / "sample_plugin" / "trust.py").is_file()
    assert (plugin_root / "README.md").is_file()


def test_rendered_plugin_rejects_missing_trust_headers_on_protected_route(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = _rendered_app_client(tmp_path, monkeypatch)

    response = client.get("/api/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "missing Hearth user headers"


def test_rendered_plugin_rejects_invalid_trust_signature(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = _rendered_app_client(tmp_path, monkeypatch)
    headers = _signed_headers(secret="wrong-secret")

    response = client.get("/api/me", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid Hearth user signature"


def test_rendered_plugin_accepts_signed_hearth_user_headers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = _rendered_app_client(tmp_path, monkeypatch)
    headers = _signed_headers(secret="test-secret")

    response = client.get("/api/me", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "id": "local",
        "name": "Local User",
        "roles": [],
    }


def test_rendered_plugin_accepts_distinct_real_user_headers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = _rendered_app_client(tmp_path, monkeypatch)
    ada = _signed_headers(
        secret="test-secret",
        user_id="user_ada_123",
        name="Ada Lovelace",
        roles="admin,user",
    )
    grace = _signed_headers(
        secret="test-secret",
        user_id="user_grace_456",
        name="Grace Hopper",
        roles="user",
    )

    ada_response = client.get("/api/me", headers=ada)
    grace_response = client.get("/api/me", headers=grace)

    assert ada_response.status_code == 200
    assert grace_response.status_code == 200
    assert ada_response.json() == {
        "id": "user_ada_123",
        "name": "Ada Lovelace",
        "roles": ["admin", "user"],
    }
    assert grace_response.json() == {
        "id": "user_grace_456",
        "name": "Grace Hopper",
        "roles": ["user"],
    }


def test_rendered_plugin_rejects_stale_trust_headers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = _rendered_app_client(tmp_path, monkeypatch)
    headers = _signed_headers(secret="test-secret", ts=int(time.time()) - 120)

    response = client.get("/api/me", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "stale Hearth user headers"


def test_rendered_plugin_help_works_without_hearth_layout(tmp_path: Path) -> None:
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")

    proc = subprocess.run(
        [str(plugin_root / "plugin"), "--help"],
        cwd=plugin_root,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "sample-plugin" in proc.stdout


def test_rendered_plugin_ops_fail_without_registry(tmp_path: Path) -> None:
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")
    proc = subprocess.run(
        [str(plugin_root / "plugin"), "--disable"],
        cwd=plugin_root,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1
    assert "hearth/plugins" in proc.stderr or "registered" in proc.stderr


def test_rendered_plugin_passthrough_with_hearth_layout(tmp_path: Path) -> None:
    from test_plugin_executable import _layout_with_plugin

    _root, plugin_exe = _layout_with_plugin(tmp_path)
    proc = subprocess.run(
        [str(plugin_exe), "--", "doctor"],
        cwd=tmp_path / "hearth" / "plugins" / "sample-plugin",
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "admin passthrough: doctor" in proc.stdout


def test_rendered_plugin_exit_errors_without_enter_session(tmp_path: Path) -> None:
    import hearth_install

    pkg_parent = str(Path(hearth_install.__file__).resolve().parents[1])
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")
    env = os.environ.copy()
    env["PYTHONPATH"] = pkg_parent
    completed = subprocess.run(
        [str(plugin_root / "plugin"), "--exit"],
        cwd=plugin_root,
        env=env,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 1
    assert "not inside" in completed.stderr


def test_rendered_install_hook_delegates_to_admin_install(tmp_path: Path) -> None:
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")
    env = os.environ.copy()
    env["HEARTH_PLUGIN_DIR"] = str(plugin_root)

    installed = subprocess.run(
        [str(plugin_root / "scripts" / "install"), "--dry-run"],
        check=True,
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert "sample-plugin admin install hook: --dry-run" in installed.stdout


def test_render_plugin_template_rejects_invalid_slug(tmp_path: Path) -> None:
    with pytest.raises(KindlingTemplateError):
        render_plugin_template(tmp_path, slug="Bad_Plugin")


def test_rendered_readme_documents_auth_without_local_login(tmp_path: Path) -> None:
    plugin_root = render_plugin_template(tmp_path, slug="sample-plugin")

    readme = (plugin_root / "README.md").read_text(encoding="utf-8")

    assert "## Authentication" in readme
    assert "require_hearth_user()" in readme
    assert "@kindling/mantle" in readme
    assert "useUser()" in readme
    assert "Do not build a local login form" in readme
    assert "document.cookie" not in readme


def test_kindling_contract_compliance_changelog_documents_trust_migration() -> None:
    changelog = Path("deploy/kindling-contract/COMPLIANCE_CHANGELOG.md").read_text(
        encoding="utf-8"
    )

    assert "T-FR-0004-07" in changelog
    for field in [
        "Contract area",
        "Compatibility",
        "Who must update",
        "Required edits",
        "Verification",
        "Fallback",
    ]:
        assert f"**{field}:**" in changelog


def test_kindling_contract_compliance_changelog_documents_multi_user_migration() -> None:
    changelog = Path("deploy/kindling-contract/COMPLIANCE_CHANGELOG.md").read_text(
        encoding="utf-8"
    )

    assert "T-FR-0004-16" in changelog
    assert "multi-user" in changelog
    for required in [
        "first admin",
        "second user",
        "drift",
        "X-Hearth-Roles",
        "useUser()",
        "kindling validate",
        "protected route",
    ]:
        assert required in changelog
