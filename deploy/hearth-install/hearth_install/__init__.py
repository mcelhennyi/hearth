"""@HRT-OPS-001 Install layout helpers for the Docker-on-Pi profile.

See ``docs/design/deployment.md`` (Docker profile, ``heart/`` mapping) and
``tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`` (**T-FR-0003-02**).
"""

from hearth_install.layout import ensure_heart_layout
from hearth_install.version_manifest import parse_version_manifest

__all__ = ["ensure_heart_layout", "parse_version_manifest"]
