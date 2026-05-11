"""Allow ``python -m hearth_plugin_cli`` when debugging."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    try:
        from hearth_plugin_cli.cli import PluginCliError, run_plugin_cli
    except ImportError:
        print("hearth_plugin_cli: missing dependencies (use hearth-ops editable install).", file=sys.stderr)
        return 1

    root = Path.cwd()
    try:
        return run_plugin_cli(plugin_root=root, argv=sys.argv[1:])
    except PluginCliError as exc:
        print(f"plugin: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
