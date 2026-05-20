"""Kindling CLI — developer-facing tooling for Hearth plugins.

Provides:
  kindling new <slug>      — scaffold a new plugin from the python template
  kindling validate [path] — validate a plugin's tinder.toml
  kindling install <path>  — POST the plugin to a running Hearth hub

Authority: tasks/feature-history/FR-0001-hearth-platform/tickets.md T-FR-0001-07
"""

from kindling_cli.cli import KindlingError, run_install, run_new, run_validate

__all__ = ["KindlingError", "run_install", "run_new", "run_validate"]
