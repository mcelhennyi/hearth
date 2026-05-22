"""API contract tests for the dashboard layout endpoints — T-FR-0006-02.

Covers:
  - GET default layout with 0, 1, N enabled plugins.
  - PUT then GET round trip retains exactly what was saved.
  - PUT with overlapping blocks returns 409.
  - PUT with malformed body returns 422.

Authority: docs/design/dashboard.md § Layout persistence, § Default layout.
"""

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient


def _install_and_enable(client: TestClient, slug: str, name: str | None = None) -> None:
    body = {
        "slug": slug,
        "name": name or slug.replace("-", " ").title(),
        "version": "0.1.0",
        "kind": "app",
    }
    resp = client.post("/api/plugins/install", json=body)
    assert resp.status_code == 200, resp.text
    resp = client.post(f"/api/plugins/{slug}/enable")
    assert resp.status_code == 200, resp.text


# ---------------------------------------------------------------------------
# GET — default layout
# ---------------------------------------------------------------------------


def test_get_default_layout_no_plugins(client: TestClient) -> None:
    resp = client.get("/api/dashboard/layout")
    assert resp.status_code == 200
    data: dict[str, Any] = resp.json()
    assert data["version"] == 1
    assert data["columns"] == 4
    assert data["blocks"] == []
    assert data["updated_at"] is None


def test_get_default_layout_one_plugin(client: TestClient) -> None:
    _install_and_enable(client, "groceries", "Groceries")
    resp = client.get("/api/dashboard/layout")
    assert resp.status_code == 200
    blocks = resp.json()["blocks"]
    assert len(blocks) == 1
    assert blocks[0]["type"] == "app-shortcut"
    assert blocks[0]["plugin"] == "groceries"
    assert (blocks[0]["x"], blocks[0]["y"], blocks[0]["w"], blocks[0]["h"]) == (0, 0, 1, 1)


def test_get_default_layout_many_plugins_wraps_rows(client: TestClient) -> None:
    # 5 plugins on a 4-col grid wraps the 5th onto row 1.
    for slug in ["a-plugin", "b-plugin", "c-plugin", "d-plugin", "e-plugin"]:
        _install_and_enable(client, slug)
    blocks = client.get("/api/dashboard/layout").json()["blocks"]
    assert len(blocks) == 5
    # Ordered by name (deterministic stub for ui.nav.order).
    assert [b["plugin"] for b in blocks] == [
        "a-plugin",
        "b-plugin",
        "c-plugin",
        "d-plugin",
        "e-plugin",
    ]
    assert (blocks[0]["x"], blocks[0]["y"]) == (0, 0)
    assert (blocks[3]["x"], blocks[3]["y"]) == (3, 0)
    assert (blocks[4]["x"], blocks[4]["y"]) == (0, 1)


def test_get_default_skips_disabled_and_widgets(client: TestClient) -> None:
    _install_and_enable(client, "groceries")
    # Install but do not enable
    client.post(
        "/api/plugins/install",
        json={"slug": "pantry", "name": "Pantry", "version": "0.1.0", "kind": "app"},
    )
    # Widget kind shouldn't appear as a default app-shortcut.
    client.post(
        "/api/plugins/install",
        json={"slug": "weather", "name": "Weather", "version": "0.1.0", "kind": "widget"},
    )
    blocks = client.get("/api/dashboard/layout").json()["blocks"]
    assert [b["plugin"] for b in blocks] == ["groceries"]


# ---------------------------------------------------------------------------
# PUT — happy path round trip
# ---------------------------------------------------------------------------


def test_put_then_get_round_trip(client: TestClient) -> None:
    payload = {
        "version": 1,
        "columns": 4,
        "blocks": [
            {
                "id": "b-1",
                "type": "app-shortcut",
                "plugin": "groceries",
                "x": 0,
                "y": 0,
                "w": 1,
                "h": 1,
            },
            {
                "id": "b-2",
                "type": "widget",
                "plugin": "pantry",
                "surface": "item-count",
                "x": 2,
                "y": 0,
                "w": 2,
                "h": 1,
            },
        ],
    }
    put = client.put("/api/dashboard/layout", json=payload)
    assert put.status_code == 200, put.text
    body = put.json()
    assert body["blocks"] == payload["blocks"]
    assert body["updated_at"] is not None

    got = client.get("/api/dashboard/layout").json()
    assert got["blocks"] == payload["blocks"]
    assert got["columns"] == 4


# ---------------------------------------------------------------------------
# PUT — 409 on collision
# ---------------------------------------------------------------------------


def test_put_rejects_overlapping_blocks_with_409(client: TestClient) -> None:
    payload = {
        "version": 1,
        "columns": 4,
        "blocks": [
            {
                "id": "a",
                "type": "app-shortcut",
                "plugin": "groceries",
                "x": 0,
                "y": 0,
                "w": 2,
                "h": 2,
            },
            {
                "id": "b",
                "type": "app-shortcut",
                "plugin": "pantry",
                "x": 1,
                "y": 1,
                "w": 1,
                "h": 1,
            },
        ],
    }
    resp = client.put("/api/dashboard/layout", json=payload)
    assert resp.status_code == 409
    assert "collision" in resp.json()["detail"].lower()


def test_put_allows_adjacent_non_overlapping_blocks(client: TestClient) -> None:
    payload = {
        "version": 1,
        "columns": 4,
        "blocks": [
            {"id": "a", "type": "app-shortcut", "plugin": "g", "x": 0, "y": 0, "w": 1, "h": 1},
            {"id": "b", "type": "app-shortcut", "plugin": "p", "x": 1, "y": 0, "w": 1, "h": 1},
        ],
    }
    resp = client.put("/api/dashboard/layout", json=payload)
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# PUT — 422 on schema invalid
# ---------------------------------------------------------------------------


def test_put_rejects_negative_coordinates_with_422(client: TestClient) -> None:
    resp = client.put(
        "/api/dashboard/layout",
        json={
            "version": 1,
            "columns": 4,
            "blocks": [
                {
                    "id": "x",
                    "type": "app-shortcut",
                    "plugin": "g",
                    "x": -1,
                    "y": 0,
                    "w": 1,
                    "h": 1,
                }
            ],
        },
    )
    assert resp.status_code == 422


def test_put_rejects_widget_without_surface_with_422(client: TestClient) -> None:
    resp = client.put(
        "/api/dashboard/layout",
        json={
            "version": 1,
            "columns": 4,
            "blocks": [
                {
                    "id": "x",
                    "type": "widget",
                    "plugin": "pantry",
                    "x": 0,
                    "y": 0,
                    "w": 2,
                    "h": 1,
                }
            ],
        },
    )
    assert resp.status_code == 422


def test_put_rejects_unknown_block_type_with_422(client: TestClient) -> None:
    resp = client.put(
        "/api/dashboard/layout",
        json={
            "version": 1,
            "columns": 4,
            "blocks": [
                {"id": "x", "type": "strip", "x": 0, "y": 0, "w": 4, "h": 1},
            ],
        },
    )
    # strip blocks are NOT in blocks[] — they live on /api/system/strips.
    assert resp.status_code == 422
