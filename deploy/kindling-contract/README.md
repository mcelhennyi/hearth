# `deploy/kindling-contract/` — Kindling plugin template mirror

**Ticket:** [`T-FR-0003-10`](../../tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-10--kindling-contract-scriptsinstall--plugin-template)

Kindling is still a planned satellite repo, so this directory is the Hearth-side mirror of the contract that FR-0003 needs before `vendor/kindling/` exists.

## Contract

Rendering the mirrored Python plugin template produces:

| Path | Contract |
|------|----------|
| `tinder.toml` | Minimal Tinder manifest matching `docs/design/plugin-contract.md` |
| `plugin` | Executable per-plugin admin shim with common lifecycle flags and `--` passthrough |
| `scripts/install` | Executable install hook; non-zero exit aborts plugin add/update in later FR-0003 flows |
| `<plugin_package>/admin.py` | Stub target for `python -m <plugin>.admin` passthrough |

## Usage

From the repo root (after `pip install -e .` or inside `./develop test`):

```bash
python - <<'PY'
from pathlib import Path
from hearth_kindling_contract import render_plugin_template

print(render_plugin_template(Path("/tmp/kindling-demo"), slug="sample-plugin"))
PY
```

Design authority: `docs/design/satellite-repos/kindling.md`, `docs/design/plugin-contract.md`, and the FR-0003 skeleton contract.
