"""API contract tests for GET/PUT /api/settings — T-FR-0001-02."""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_get_settings_returns_defaults(client: TestClient) -> None:
    resp = client.get("/api/settings")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("theme") == "dark"
    assert data.get("hostname") == "hearth.home.arpa"
    assert data.get("notification_channel") == "web-push"


def test_put_settings_updates_value(client: TestClient) -> None:
    resp = client.put("/api/settings", json={"theme": "light"})
    assert resp.status_code == 200
    assert resp.json().get("theme") == "light"


def test_put_settings_persists_update(client: TestClient) -> None:
    client.put("/api/settings", json={"hostname": "box.local"})
    resp = client.get("/api/settings")
    assert resp.json().get("hostname") == "box.local"


def test_put_settings_partial_update_leaves_others_unchanged(client: TestClient) -> None:
    client.put("/api/settings", json={"theme": "light"})
    resp = client.get("/api/settings")
    data = resp.json()
    assert data.get("theme") == "light"
    assert data.get("hostname") == "hearth.home.arpa"
