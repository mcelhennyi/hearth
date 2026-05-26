"""API contract tests for /api/system/{tiles,strips} — T-FR-0006-01.

Authority: docs/design/dashboard.md §"system block — content and configuration
(DF-U1)" and §"strip block — content and configuration (DF-U2)".

v0 tile catalogue: ca-trust, hub-healthy, pi-online.
v0 strip catalogue: pwa-install, mac-shell.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

V0_TILE_IDS = {"ca-trust", "hub-healthy", "pi-online"}
V0_STRIP_IDS = {"pwa-install", "mac-shell"}


# ---------------------------------------------------------------------------
# GET /api/system/tiles
# ---------------------------------------------------------------------------


def test_get_system_tiles_returns_v0_catalogue(client: TestClient) -> None:
    resp = client.get("/api/system/tiles")
    assert resp.status_code == 200
    data = resp.json()
    assert "tiles" in data
    ids = {t["id"] for t in data["tiles"]}
    assert ids == V0_TILE_IDS


def test_system_tile_shape(client: TestClient) -> None:
    resp = client.get("/api/system/tiles")
    tiles = resp.json()["tiles"]
    for tile in tiles:
        assert set(tile.keys()) >= {
            "id",
            "title",
            "body",
            "hidden_by_user",
            "suppressed",
        }
        assert isinstance(tile["hidden_by_user"], bool)
        assert isinstance(tile["suppressed"], bool)
        # action is optional but, when present, must have nav: str.
        if tile.get("action") is not None:
            assert isinstance(tile["action"], dict)
            assert isinstance(tile["action"]["nav"], str)


def test_default_tile_state_is_visible(client: TestClient) -> None:
    resp = client.get("/api/system/tiles")
    for tile in resp.json()["tiles"]:
        assert tile["hidden_by_user"] is False


# ---------------------------------------------------------------------------
# POST /api/system/tiles/<id>/hide and /restore
# ---------------------------------------------------------------------------


def test_hide_tile_persists(client: TestClient) -> None:
    resp = client.post("/api/system/tiles/ca-trust/hide")
    assert resp.status_code == 204

    listing = client.get("/api/system/tiles").json()["tiles"]
    by_id = {t["id"]: t for t in listing}
    assert by_id["ca-trust"]["hidden_by_user"] is True
    assert by_id["hub-healthy"]["hidden_by_user"] is False


def test_restore_tile_clears_hidden(client: TestClient) -> None:
    client.post("/api/system/tiles/ca-trust/hide")
    resp = client.post("/api/system/tiles/ca-trust/restore")
    assert resp.status_code == 204

    by_id = {t["id"]: t for t in client.get("/api/system/tiles").json()["tiles"]}
    assert by_id["ca-trust"]["hidden_by_user"] is False


def test_hide_unknown_tile_returns_404(client: TestClient) -> None:
    resp = client.post("/api/system/tiles/does-not-exist/hide")
    assert resp.status_code == 404


def test_hide_tile_is_idempotent(client: TestClient) -> None:
    assert client.post("/api/system/tiles/ca-trust/hide").status_code == 204
    assert client.post("/api/system/tiles/ca-trust/hide").status_code == 204
    by_id = {t["id"]: t for t in client.get("/api/system/tiles").json()["tiles"]}
    assert by_id["ca-trust"]["hidden_by_user"] is True


def test_restore_unhidden_tile_is_noop(client: TestClient) -> None:
    # Restore when not hidden should still succeed (idempotent).
    resp = client.post("/api/system/tiles/ca-trust/restore")
    assert resp.status_code == 204


# ---------------------------------------------------------------------------
# GET /api/system/strips
# ---------------------------------------------------------------------------


def test_get_system_strips_default_returns_no_active(client: TestClient) -> None:
    # Without a platform hint, no strip applies.
    resp = client.get("/api/system/strips")
    assert resp.status_code == 200
    assert resp.json() == {"strip": None}


def test_get_system_strips_ios_returns_pwa_install(client: TestClient) -> None:
    resp = client.get("/api/system/strips", params={"platform": "ios"})
    assert resp.status_code == 200
    strip = resp.json()["strip"]
    assert strip is not None
    assert strip["id"] == "pwa-install"


def test_get_system_strips_desktop_returns_mac_shell(client: TestClient) -> None:
    resp = client.get("/api/system/strips", params={"platform": "desktop"})
    strip = resp.json()["strip"]
    assert strip is not None
    assert strip["id"] == "mac-shell"


def test_strip_shape(client: TestClient) -> None:
    strip = client.get("/api/system/strips", params={"platform": "ios"}).json()["strip"]
    assert set(strip.keys()) >= {"id", "title", "body", "dismissed"}
    assert isinstance(strip["dismissed"], bool)


# ---------------------------------------------------------------------------
# POST /api/system/strips/<id>/dismiss
# ---------------------------------------------------------------------------


def test_dismiss_strip_persists(client: TestClient) -> None:
    resp = client.post("/api/system/strips/pwa-install/dismiss")
    assert resp.status_code == 204

    # Once dismissed, that strip is no longer returned as active.
    payload = client.get("/api/system/strips", params={"platform": "ios"}).json()
    assert payload["strip"] is None


def test_dismiss_one_strip_does_not_dismiss_others(client: TestClient) -> None:
    client.post("/api/system/strips/pwa-install/dismiss")
    payload = client.get("/api/system/strips", params={"platform": "desktop"}).json()
    assert payload["strip"] is not None
    assert payload["strip"]["id"] == "mac-shell"


def test_dismiss_unknown_strip_returns_404(client: TestClient) -> None:
    resp = client.post("/api/system/strips/does-not-exist/dismiss")
    assert resp.status_code == 404


def test_dismiss_is_idempotent(client: TestClient) -> None:
    assert client.post("/api/system/strips/pwa-install/dismiss").status_code == 204
    assert client.post("/api/system/strips/pwa-install/dismiss").status_code == 204
