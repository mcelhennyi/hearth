"""Caddy fragment renderer and reload trigger — T-FR-0001-05.

Renders a Caddyfile fragment from the enabled plugin registry and
optionally reloads Caddy via its admin API.

Design authority: docs/design/plugin-contract.md (proxy section)

Public API
----------
render_fragment(plugins)          Pure function: list of plugin dicts → fragment text.
write_fragment(plugins, path)     Render and write fragment to *path*.
reload_caddy(admin_url)           POST to Caddy admin API; no-op / logs on error.
regenerate_and_reload(session)    Query DB, write fragment, reload.  Called by plugin routes.
"""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

# Default fragment output path (override with HEARTH_CADDY_FRAGMENT_PATH).
_DEFAULT_FRAGMENT_PATH = Path(
    os.getenv("HEARTH_CADDY_FRAGMENT_PATH", "/workspace/var/hearth/caddy-fragment.conf")
)

# Caddy admin API base URL (override with HEARTH_CADDY_ADMIN_URL).
# In the Compose stack the caddy container is reachable at http://caddy:2019.
_DEFAULT_CADDY_ADMIN_URL = os.getenv("HEARTH_CADDY_ADMIN_URL", "http://caddy:2019")

# Path to the Caddyfile config used for `caddy reload` (fallback if admin API is unavailable).
_DEFAULT_CADDYFILE = os.getenv("HEARTH_CADDYFILE_PATH", "/etc/caddy/Caddyfile")


# ---------------------------------------------------------------------------
# Fragment renderer — pure, no I/O
# ---------------------------------------------------------------------------


def render_fragment(plugins: list[dict[str, Any]]) -> str:
    """Render a Caddyfile reverse-proxy fragment for all enabled plugins.

    Each enabled plugin produces a block of the form::

        route /<slug>/* {
          reverse_proxy <host>:<port>
        }

    Args:
        plugins: sequence of dicts with keys ``slug``, ``host``, ``port``,
                 and ``state``.  Only entries with ``state == "enabled"``
                 are emitted.

    Returns:
        Caddyfile fragment string (may be empty if no plugins are enabled).
    """
    lines: list[str] = []
    for p in plugins:
        if p.get("state") != "enabled":
            continue
        slug = p["slug"]
        host = p["host"]
        port = p["port"]
        lines.append(f"route /{slug}/* {{")
        lines.append(f"  reverse_proxy {host}:{port}")
        lines.append("}")
        lines.append("")  # blank line between blocks
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Fragment writer
# ---------------------------------------------------------------------------


def write_fragment(plugins: list[dict[str, Any]], path: Path = _DEFAULT_FRAGMENT_PATH) -> None:
    """Render *plugins* to a Caddyfile fragment file at *path*.

    Creates parent directories as needed.  Writes atomically via a temp file
    so a concurrent Caddy reload does not read a partial fragment.
    """
    content = render_fragment(plugins)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)
    log.debug("caddy fragment written to %s (%d bytes)", path, len(content))


# ---------------------------------------------------------------------------
# Caddy reload
# ---------------------------------------------------------------------------


def reload_caddy(admin_url: str = _DEFAULT_CADDY_ADMIN_URL) -> None:
    """Signal Caddy to reload its config via the admin API.

    Uses ``POST <admin_url>/load`` with the current Caddyfile content so the
    reload is atomic.  Falls back to ``caddy reload`` subprocess on error.

    Never raises — errors are logged so the plugin operation still completes.
    """
    try:
        import urllib.error
        import urllib.request

        caddyfile_path = Path(_DEFAULT_CADDYFILE)
        if not caddyfile_path.exists():
            log.warning("caddy reload skipped: Caddyfile not found at %s", caddyfile_path)
            return

        config_bytes = caddyfile_path.read_bytes()
        req = urllib.request.Request(
            f"{admin_url}/load",
            data=config_bytes,
            headers={"Content-Type": "text/caddyfile"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                log.info("caddy reloaded via admin API")
            else:
                log.warning("caddy admin API returned status %s", resp.status)

    except Exception as exc:  # noqa: BLE001
        log.warning("caddy admin API reload failed (%s); trying subprocess reload", exc)
        _reload_via_subprocess()


def _reload_via_subprocess() -> None:
    """Fall back to 'caddy reload' subprocess (for privileged sidecar setups)."""
    try:
        result = subprocess.run(
            ["caddy", "reload", "--config", _DEFAULT_CADDYFILE],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            log.info("caddy reloaded via subprocess")
        else:
            log.error("caddy reload subprocess failed: %s", result.stderr)
    except Exception as exc:  # noqa: BLE001
        log.error("caddy reload subprocess error: %s", exc)


# ---------------------------------------------------------------------------
# High-level helper for route handlers
# ---------------------------------------------------------------------------


async def regenerate_and_reload(
    session: Any,
    *,
    fragment_path: Path = _DEFAULT_FRAGMENT_PATH,
    admin_url: str = _DEFAULT_CADDY_ADMIN_URL,
) -> None:
    """Query the DB for enabled plugins, write the fragment, and reload Caddy.

    Intended to be called from plugin install/enable/disable/uninstall routes
    after the DB transaction commits.

    Args:
        session:       Active SQLAlchemy AsyncSession.
        fragment_path: Where to write the fragment (default: HEARTH_CADDY_FRAGMENT_PATH).
        admin_url:     Caddy admin API URL (default: HEARTH_CADDY_ADMIN_URL).
    """
    from sqlalchemy import select

    from app.models import Plugin

    result = await session.execute(select(Plugin))
    db_plugins = list(result.scalars().all())

    # Build the host/port from env convention: HEARTH_PLUGIN_<SLUG_UPPER>_{HOST,PORT}
    # Falls back to slug-based defaults for the Compose network.
    proxy_plugins: list[dict[str, Any]] = []
    for plugin in db_plugins:
        slug_env = plugin.slug.upper().replace("-", "_")
        host = os.getenv(f"HEARTH_PLUGIN_{slug_env}_HOST", plugin.slug)
        port = int(os.getenv(f"HEARTH_PLUGIN_{slug_env}_PORT", "8000"))
        proxy_plugins.append(
            {
                "slug": plugin.slug,
                "host": host,
                "port": port,
                "state": plugin.state,
            }
        )

    write_fragment(proxy_plugins, path=fragment_path)
    reload_caddy(admin_url=admin_url)
