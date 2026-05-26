"""API contract tests for user preferences — T-FR-0006-04.

Covers:
  - GET returns default theme when none persisted.
  - PUT merges partial updates and returns 200.
  - PUT invalid theme returns 422.
  - GET after PUT round trip.

Authority: docs/design/mantle-ui.md § Settings modal, § Theme persistence.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_get_default_preferences(client: TestClient) -> None:
    resp = client.get("/api/user/preferences")
    assert resp.status_code == 200
    assert resp.json() == {"theme": "system"}


def test_put_then_get_round_trip(client: TestClient) -> None:
    put = client.put("/api/user/preferences", json={"theme": "dark"})
    assert put.status_code == 200
    assert put.json() == {"theme": "dark"}

    get = client.get("/api/user/preferences")
    assert get.status_code == 200
    assert get.json() == {"theme": "dark"}


def test_put_merge_preserves_unmentioned_fields(client: TestClient) -> None:
    client.put("/api/user/preferences", json={"theme": "light"})
    # Second PUT with same value still 200 (idempotent merge).
    resp = client.put("/api/user/preferences", json={"theme": "light"})
    assert resp.status_code == 200
    assert resp.json()["theme"] == "light"


def test_put_invalid_theme_returns_422(client: TestClient) -> None:
    resp = client.put("/api/user/preferences", json={"theme": "sepia"})
    assert resp.status_code == 422


def test_put_all_valid_themes(client: TestClient) -> None:
    for theme in ("light", "dark", "system"):
        resp = client.put("/api/user/preferences", json={"theme": theme})
        assert resp.status_code == 200, resp.text
        assert resp.json()["theme"] == theme
