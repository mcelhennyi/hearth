"""Kindling CLI implementation — T-FR-0001-07.

Commands:
  new <slug> [--parent <dir>]   Scaffold a new plugin directory.
  validate [<path>]              Validate a plugin's tinder.toml.
  install <path> [--hub <url>]   POST the plugin to a running Hearth hub.

The validate command delegates to hearth_kindling_contract (which itself wraps
the tinder.toml loader from apps/hub/api/tinder or the install-side mirror).
The new command delegates to hearth_kindling_contract.render_plugin_template.

DESIGN-GAP: kindling install requires a live hub with /api/plugins/install.
The MVP implementation POSTs the plugin slug + directory path; the hub API
must accept this form (see apps/hub/api/app/routes/plugins.py).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import requests  # type: ignore[import-untyped]
except ImportError:
    requests = None  # type: ignore[assignment]


class KindlingError(RuntimeError):
    """User-facing Kindling CLI error."""


# ---------------------------------------------------------------------------
# kindling new
# ---------------------------------------------------------------------------


def run_new(slug: str, *, parent: Path | None = None) -> Path:
    """Scaffold a new plugin under *parent* / *slug*.

    Returns the created plugin root directory.
    Raises KindlingError on invalid slug or if the directory already exists.
    """
    from hearth_kindling_contract import KindlingTemplateError, render_plugin_template

    dest = parent if parent is not None else Path.cwd()
    dest = dest.resolve()
    try:
        plugin_root = render_plugin_template(dest, slug=slug)
    except KindlingTemplateError as exc:
        raise KindlingError(str(exc)) from exc
    return plugin_root


# ---------------------------------------------------------------------------
# kindling validate
# ---------------------------------------------------------------------------


def run_validate(plugin_path: Path) -> list[str]:
    """Validate a plugin directory.

    Returns an empty list on success, or a list of human-readable error strings.
    Does NOT raise on validation failure — returns errors so callers can decide.
    Raises KindlingError only on unexpected internal errors.
    """
    # Prefer the full Pydantic-backed tinder loader when available (apps/hub/api
    # is on pythonpath in development). Fall back to the install-side mirror.
    try:
        from tinder.loader import load_tinder

        _, errors = load_tinder(plugin_path)
        return errors
    except ImportError:
        pass

    # Fallback: install-side manifest check (deploy/hearth-install)
    try:
        from hearth_install.tinder_manifest import TinderManifestError, load_tinder_manifest

        try:
            load_tinder_manifest(plugin_path)
            return []
        except TinderManifestError as exc:
            return [str(exc)]
    except ImportError:
        pass

    # Last resort: just check for tinder.toml existence
    toml_path = plugin_path / "tinder.toml"
    if not toml_path.is_file():
        return [f"tinder.toml not found at {toml_path}"]
    return []


# ---------------------------------------------------------------------------
# kindling install
# ---------------------------------------------------------------------------


def run_install(
    plugin_path: Path,
    *,
    hub_url: str = "http://localhost:8200",
) -> dict[str, Any]:
    """POST the plugin at *plugin_path* to the Hearth hub for installation.

    Returns the parsed JSON response on success.
    Raises KindlingError on HTTP errors or connection failures.

    DESIGN-GAP: The hub's /api/plugins/install endpoint must accept
    {"slug": "<slug>", "path": "<abs-path>"} or a multipart upload.
    The MVP uses a JSON body with the absolute plugin path (works when the
    CLI and hub share the same filesystem, i.e. developer workflow).
    """
    if requests is None:
        raise KindlingError(
            "kindling install requires the 'requests' package (pip install requests)"
        )

    plugin_path = plugin_path.resolve()

    # Read slug from tinder.toml if available
    slug = plugin_path.name
    toml_path = plugin_path / "tinder.toml"
    if toml_path.is_file():
        try:
            import tomllib

            data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
            slug = data.get("plugin", {}).get("slug", slug)
        except Exception:
            pass

    url = hub_url.rstrip("/") + "/api/plugins/install"
    payload = {"slug": slug, "path": str(plugin_path)}

    try:
        resp = requests.post(url, json=payload, timeout=10)
    except requests.RequestException as exc:
        raise KindlingError(f"could not reach hub at {hub_url}: {exc}") from exc

    if resp.status_code not in (200, 201):
        raise KindlingError(f"hub returned {resp.status_code} from {url}: {resp.text[:200]}")

    try:
        return dict(resp.json())
    except Exception:
        return {"status": "ok", "raw": resp.text}


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kindling",
        description="Hearth Kindling developer CLI",
    )
    sub = parser.add_subparsers(dest="command", metavar="command")

    # new
    p_new = sub.add_parser("new", help="Scaffold a new plugin")
    p_new.add_argument("slug", help="Plugin slug (kebab-case, e.g. groceries)")
    p_new.add_argument(
        "--parent",
        type=Path,
        default=None,
        help="Parent directory (default: cwd)",
    )

    # validate
    p_val = sub.add_parser("validate", help="Validate a plugin tinder.toml")
    p_val.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=None,
        help="Plugin directory (default: cwd)",
    )

    # install
    p_inst = sub.add_parser("install", help="Install a plugin into a running hub")
    p_inst.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=None,
        help="Plugin directory (default: cwd)",
    )
    p_inst.add_argument(
        "--hub",
        default="http://localhost:8200",
        help="Hub base URL (default: http://localhost:8200)",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "new":
        try:
            plugin_root = run_new(args.slug, parent=args.parent)
        except KindlingError as exc:
            print(f"kindling new: {exc}", file=sys.stderr)
            return 1
        print(f"Created plugin at {plugin_root}")
        return 0

    if args.command == "validate":
        path = (args.path or Path.cwd()).resolve()
        errors = run_validate(path)
        if errors:
            for err in errors:
                print(f"  error: {err}", file=sys.stderr)
            print(f"kindling validate: {path} FAILED ({len(errors)} error(s))", file=sys.stderr)
            return 1
        print(f"kindling validate: {path} OK")
        return 0

    if args.command == "install":
        path = (args.path or Path.cwd()).resolve()
        try:
            result = run_install(path, hub_url=args.hub)
        except KindlingError as exc:
            print(f"kindling install: {exc}", file=sys.stderr)
            return 1
        print(f"kindling install: {result}")
        return 0

    parser.print_help()
    return 1
