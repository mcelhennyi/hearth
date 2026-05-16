"""@HRT-OPS-001 Install layout helpers for the Docker-on-Pi profile.

See ``docs/design/deployment.md`` (Docker profile, ``hearth/`` mapping) and
``tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`` (**T-FR-0003-02**
and **T-FR-0003-05**).
"""

from hearth_install.layout import ensure_hearth_layout
from hearth_install.plugin_compose import generate_plugin_compose, load_plugin_registry
from hearth_install.version_manifest import parse_version_manifest

__all__ = [
    "ensure_hearth_layout",
    "generate_plugin_compose",
    "load_plugin_registry",
    "parse_version_manifest",
]
