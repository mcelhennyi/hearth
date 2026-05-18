"""@HRT-KDLG-001 Hearth-side Kindling plugin template contract mirror.

Kindling is still a planned satellite repository; this package mirrors the
template contract that Hearth FR-0003 consumes. See
``docs/design/satellite-repos/kindling.md`` and
``tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`` (**T-FR-0003-10**).
"""

from hearth_kindling_contract.template import KindlingTemplateError, render_plugin_template

__all__ = ["KindlingTemplateError", "render_plugin_template"]
