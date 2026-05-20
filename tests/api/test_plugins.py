"""API contract tests for the plugin registry — T-FR-0001-02.

Covers the install→enable→disable→uninstall CRUD cycle and asserts that
response schemas match the plugin contract in docs/design/plugin-contract.md.

Key schema assertions (from plugin-contract.md):
  - slug: kebab-case ASCII ≤ 32 chars
  - state: "disabled" | "enabled" | "uninstalled" | "error"
  - kind:  "app" | "widget" | "service"
"""
from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

VALID_PLUGIN: dict[str, Any] = {
    "slug": "test-plugin",
    "name": "Test Plugin",
    "version": "0.1.0",
    "kind": "app",
}


# ---------------------------------------------------------------------------
# GET /api/plugins — empty registry
# ---------------------------------------------------------------------------


def test_list_plugins_empty(client: TestClient) -> None:
    resp = client.get("/api/plugins")
    assert resp.status_code == 200
    assert resp.json() == []


# ---------------------------------------------------------------------------
# POST /api/plugins/install
# ---------------------------------------------------------------------------


def test_install_plugin_returns_disabled_state(client: TestClient) -> None:
    resp = client.post("/api/plugins/install", json=VALID_PLUGIN)
    assert resp.status_code == 200
    data = resp.json()
    assert data["slug"] == "test-plugin"
    assert data["state"] == "disabled"
    assert data["kind"] == "app"
    assert data["name"] == "Test Plugin"
    assert data["version"] == "0.1.0"
    assert "installed_at" in data


def test_install_plugin_appears_in_list(client: TestClient) -> None:
    client.post("/api/plugins/install", json=VALID_PLUGIN)
    resp = client.get("/api/plugins")
    assert resp.status_code == 200
    slugs = [p["slug"] for p in resp.json()]
    assert "test-plugin" in slugs


def test_install_duplicate_slug_returns_409(client: TestClient) -> None:
    client.post("/api/plugins/install", json=VALID_PLUGIN)
    resp = client.post("/api/plugins/install", json=VALID_PLUGIN)
    assert resp.status_code == 409


def test_install_slug_too_long_returns_422(client: TestClient) -> None:
    bad = {**VALID_PLUGIN, "slug": "a" * 33}
    resp = client.post("/api/plugins/install", json=bad)
    assert resp.status_code == 422


def test_install_invalid_slug_chars_returns_422(client: TestClient) -> None:
    bad = {**VALID_PLUGIN, "slug": "Bad_Slug"}
    resp = client.post("/api/plugins/install", json=bad)
    assert resp.status_code == 422


def test_install_invalid_kind_returns_422(client: TestClient) -> None:
    bad = {**VALID_PLUGIN, "slug": "other-plugin", "kind": "unknown"}
    resp = client.post("/api/plugins/install", json=bad)
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# POST /api/plugins/{slug}/enable
# ---------------------------------------------------------------------------


def test_enable_plugin_sets_enabled_state(client: TestClient) -> None:
    client.post("/api/plugins/install", json=VALID_PLUGIN)
    resp = client.post("/api/plugins/test-plugin/enable")
    assert resp.status_code == 200
    data = resp.json()
    assert data["state"] == "enabled"
    assert data["slug"] == "test-plugin"


def test_enable_unknown_plugin_returns_404(client: TestClient) -> None:
    resp = client.post("/api/plugins/no-such-plugin/enable")
    assert resp.status_code == 404


def test_enable_widget_plugin_returns_501(client: TestClient) -> None:
    """MVP policy: widget plugins cannot be enabled yet (plugin-contract.md)."""
    widget = {**VALID_PLUGIN, "slug": "my-widget", "kind": "widget"}
    client.post("/api/plugins/install", json=widget)
    resp = client.post("/api/plugins/my-widget/enable")
    assert resp.status_code == 501


# ---------------------------------------------------------------------------
# POST /api/plugins/{slug}/disable
# ---------------------------------------------------------------------------


def test_disable_enabled_plugin_sets_disabled_state(client: TestClient) -> None:
    client.post("/api/plugins/install", json=VALID_PLUGIN)
    client.post("/api/plugins/test-plugin/enable")
    resp = client.post("/api/plugins/test-plugin/disable")
    assert resp.status_code == 200
    assert resp.json()["state"] == "disabled"


def test_disable_unknown_plugin_returns_404(client: TestClient) -> None:
    resp = client.post("/api/plugins/no-such-plugin/disable")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/plugins/{slug}/uninstall
# ---------------------------------------------------------------------------


def test_uninstall_plugin_sets_uninstalled_state(client: TestClient) -> None:
    client.post("/api/plugins/install", json=VALID_PLUGIN)
    resp = client.post("/api/plugins/test-plugin/uninstall")
    assert resp.status_code == 200
    assert resp.json()["state"] == "uninstalled"


def test_uninstall_unknown_plugin_returns_404(client: TestClient) -> None:
    resp = client.post("/api/plugins/no-such-plugin/uninstall")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Full install → enable → disable → uninstall cycle
# ---------------------------------------------------------------------------


def test_full_lifecycle_cycle(client: TestClient) -> None:
    # install → disabled
    r = client.post("/api/plugins/install", json=VALID_PLUGIN)
    assert r.status_code == 200
    assert r.json()["state"] == "disabled"

    # enable → enabled
    r = client.post("/api/plugins/test-plugin/enable")
    assert r.status_code == 200
    assert r.json()["state"] == "enabled"

    # disable → disabled
    r = client.post("/api/plugins/test-plugin/disable")
    assert r.status_code == 200
    assert r.json()["state"] == "disabled"

    # uninstall → uninstalled
    r = client.post("/api/plugins/test-plugin/uninstall")
    assert r.status_code == 200
    assert r.json()["state"] == "uninstalled"

    # list still shows the row (uninstalled is a terminal state, not deleted)
    r = client.get("/api/plugins")
    assert r.status_code == 200
    states = {p["slug"]: p["state"] for p in r.json()}
    assert states.get("test-plugin") == "uninstalled"


# ---------------------------------------------------------------------------
# Schema completeness: required fields present on all list entries
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("field", ["slug", "name", "version", "kind", "state", "installed_at"])
def test_list_entry_has_required_field(client: TestClient, field: str) -> None:
    client.post("/api/plugins/install", json=VALID_PLUGIN)
    plugins = client.get("/api/plugins").json()
    assert len(plugins) == 1
    assert field in plugins[0], f"Missing field '{field}' in plugin list response"
