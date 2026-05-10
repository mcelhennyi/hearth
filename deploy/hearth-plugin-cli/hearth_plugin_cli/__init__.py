"""@HRT-OPS-002 Per-plugin ``plugin`` CLI shared by Kindling templates (T-FR-0003-11)."""

from hearth_plugin_cli.cli import PluginCliError, run_plugin_cli

__all__ = ["PluginCliError", "run_plugin_cli"]
