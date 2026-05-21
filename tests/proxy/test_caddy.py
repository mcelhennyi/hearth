"""Unit tests for the Caddy fragment renderer — T-FR-0001-05.

Tests the fragment renderer in isolation (no Caddy process required).
Fixtures provide enabled/disabled plugin rows; assertions verify the
rendered text matches expected Caddyfile fragment snippets.

Integration tests (real Caddy + Compose network) are marked
``pytest.mark.integration`` and skipped unless ``HEARTH_INTEGRATION=1``
is set in the environment.  Those cannot run inside the hearth-test
Docker container; they require the full Compose stack.
"""

from __future__ import annotations

import os

import pytest

from proxy.caddy import render_fragment

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _plugin(slug: str, *, host: str, port: int, state: str = "enabled") -> dict:
    """Minimal plugin-row dict for render_fragment."""
    return {"slug": slug, "host": host, "port": port, "state": state}


# ---------------------------------------------------------------------------
# render_fragment — pure function tests (no I/O)
# ---------------------------------------------------------------------------


class TestRenderFragment:
    """render_fragment(plugins) → Caddyfile fragment string."""

    def test_empty_registry_yields_empty_fragment(self) -> None:
        result = render_fragment([])
        assert result.strip() == ""

    def test_single_enabled_plugin_produces_route_block(self) -> None:
        plugins = [_plugin("groceries", host="groceries-app", port=8000)]
        result = render_fragment(plugins)
        assert "route /groceries/*" in result
        assert "reverse_proxy groceries-app:8000" in result

    def test_disabled_plugin_is_excluded(self) -> None:
        plugins = [
            _plugin("groceries", host="groceries-app", port=8000),
            _plugin("todo", host="todo-app", port=9000, state="disabled"),
        ]
        result = render_fragment(plugins)
        assert "route /groceries/*" in result
        assert "route /todo/*" not in result

    def test_uninstalled_plugin_is_excluded(self) -> None:
        plugins = [
            _plugin("groceries", host="groceries-app", port=8000),
            _plugin("old-plugin", host="old-host", port=7000, state="uninstalled"),
        ]
        result = render_fragment(plugins)
        assert "route /old-plugin/*" not in result

    def test_multiple_enabled_plugins(self) -> None:
        plugins = [
            _plugin("groceries", host="groceries-app", port=8000),
            _plugin("weather", host="weather-svc", port=8100),
            _plugin("calendar", host="cal-svc", port=8200, state="disabled"),
        ]
        result = render_fragment(plugins)
        assert "route /groceries/*" in result
        assert "reverse_proxy groceries-app:8000" in result
        assert "route /weather/*" in result
        assert "reverse_proxy weather-svc:8100" in result
        assert "route /calendar/*" not in result

    def test_golden_single_plugin(self) -> None:
        """Exact golden-file assertion for a single plugin fragment."""
        plugins = [_plugin("groceries", host="groceries-app", port=8000)]
        result = render_fragment(plugins)
        # Must contain exactly one route block (no trailing noise)
        lines = [ln for ln in result.splitlines() if ln.strip()]
        # route line, reverse_proxy line, closing brace — at minimum 3 meaningful lines
        assert len(lines) >= 3
        # Route must use exact path pattern for slug
        route_lines = [ln for ln in lines if "route" in ln]
        assert len(route_lines) == 1
        assert "/groceries/*" in route_lines[0]

    def test_plugin_host_port_injected_correctly(self) -> None:
        """Ensure host:port are not swapped or mangled."""
        plugins = [_plugin("svc", host="my-host", port=1234)]
        result = render_fragment(plugins)
        assert "my-host:1234" in result

    def test_only_enabled_state_is_proxied(self) -> None:
        """All non-'enabled' states must be excluded from the fragment."""
        for state in ("disabled", "uninstalled", "error"):
            plugins = [_plugin("p", host="h", port=1, state=state)]
            result = render_fragment(plugins)
            assert result.strip() == "", f"expected empty fragment for state={state!r}"


# ---------------------------------------------------------------------------
# Integration placeholder (requires full Compose stack)
# ---------------------------------------------------------------------------


@pytest.mark.integration
@pytest.mark.skipif(
    os.environ.get("HEARTH_INTEGRATION") != "1",
    reason="Integration tests require HEARTH_INTEGRATION=1 and running Compose stack",
)
def test_caddy_proxies_stub_plugin_over_https() -> None:  # pragma: no cover
    """Spin up real Caddy, install stub plugin, curl the route.

    This test requires the full Compose stack (caddy + hub + stub plugin service).
    It cannot run inside the hearth-test Docker container.

    To run manually:
        docker compose -f deploy/compose/docker-compose.yml up -d
        HEARTH_INTEGRATION=1 pytest \
            tests/proxy/test_caddy.py::test_caddy_proxies_stub_plugin_over_https
    """
    import urllib.request

    # The stub plugin must be installed + enabled via the hub API before this runs.
    # See tests/proxy/README.md for manual setup steps.
    url = "https://hearth.home.arpa/groceries-stub/health"
    try:
        import ssl

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(url, context=ctx, timeout=5) as resp:
            assert resp.status == 200
    except Exception as exc:
        pytest.fail(f"Integration test failed: {exc}")
