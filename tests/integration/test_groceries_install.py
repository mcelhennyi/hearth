"""Groceries reference plugin — Hearth-side install tests (T-FR-0001-08).

Unit tests use the groceries-stub fixture (runs inside hearth-test Docker image).
Integration tests require ``HEARTH_INTEGRATION=1`` and a running Compose stack.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Fixture path helpers
# ---------------------------------------------------------------------------

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "plugins"
GROCERIES_STUB = FIXTURES_DIR / "groceries-stub"


# ---------------------------------------------------------------------------
# Unit-level tests (run inside hearth-test Docker image without Compose stack)
# ---------------------------------------------------------------------------


def test_install_groceries_stub_from_source(client: TestClient) -> None:
    """Install from groceries-stub tinder.toml; verify slug and state."""
    resp = client.post(
        "/api/plugins/install",
        json={"source": str(GROCERIES_STUB)},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["slug"] == "groceries-stub"
    assert data["state"] == "disabled"
    assert data["kind"] == "app"
    assert data["version"] == "0.1.0"
    assert data.get("validation_errors", []) == []


def test_install_groceries_stub_appears_in_list(client: TestClient) -> None:
    resp = client.post(
        "/api/plugins/install",
        json={"source": str(GROCERIES_STUB)},
    )
    assert resp.status_code == 200

    resp = client.get("/api/plugins")
    assert resp.status_code == 200
    slugs = [p["slug"] for p in resp.json()]
    assert "groceries-stub" in slugs


def test_install_groceries_stub_duplicate_returns_409(client: TestClient) -> None:
    client.post("/api/plugins/install", json={"source": str(GROCERIES_STUB)})
    resp = client.post(
        "/api/plugins/install",
        json={"source": str(GROCERIES_STUB)},
    )
    assert resp.status_code == 409


def test_enable_groceries_stub_after_install(client: TestClient) -> None:
    client.post("/api/plugins/install", json={"source": str(GROCERIES_STUB)})
    resp = client.post("/api/plugins/groceries-stub/enable")
    assert resp.status_code == 200
    assert resp.json()["state"] == "enabled"


# ---------------------------------------------------------------------------
# Live-stack integration test (skipped without HEARTH_INTEGRATION=1)
# ---------------------------------------------------------------------------


@pytest.mark.integration
@pytest.mark.skipif(
    os.environ.get("HEARTH_INTEGRATION") != "1",
    reason="Requires HEARTH_INTEGRATION=1 and running Compose stack",
)
def test_groceries_install_via_live_hub() -> None:  # pragma: no cover
    """Install the groceries submodule path against the running hub container.

    apps/groceries/ must be checked out (git submodule) in the repo root.
    Requires the full Compose stack with HEARTH_INTEGRATION=1.
    """
    import requests  # noqa: PLC0415

    hub_url = os.environ.get("HEARTH_HUB_URL", "http://localhost:8200")
    groceries_path = str(Path(__file__).parent.parent.parent / "apps" / "groceries")

    resp = requests.post(
        f"{hub_url}/api/plugins/install",
        json={"source": groceries_path},
        timeout=10,
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["slug"] == "groceries"
    assert data["state"] == "disabled"
    assert data["kind"] == "app"

    list_resp = requests.get(f"{hub_url}/api/plugins", timeout=10)
    assert list_resp.status_code == 200
    slugs = [p["slug"] for p in list_resp.json()]
    assert "groceries" in slugs
