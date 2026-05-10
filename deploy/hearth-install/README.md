# `deploy/hearth-install/` — Docker profile `heart/` layout

**Ticket:** [`T-FR-0003-02`](../../tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-02--install-layout-heart-versionjson-readme)

## Contents

| Path | Role |
|------|------|
| [`schemas/version-1.schema.json`](schemas/version-1.schema.json) | JSON Schema for **`heart/VERSION.json`** (manifest v1) |
| [`hearth_install/`](hearth_install/) | Python package: idempotent layout generator + parser |
| [`hearth_install/templates/README.heart.md`](hearth_install/templates/README.heart.md) | Copied to **`<install-dir>/heart/README.md`** |
| [`hearth_install/templates/VERSION.json.example`](hearth_install/templates/VERSION.json.example) | Non-secret example manifest (same shape as generated default) |

## Usage

From the repo root (after `pip install -e .` or inside **`./develop test`**):

```bash
python -m hearth_install /path/to/parent-of-heart --hearth-ref "$(git rev-parse HEAD)"
```

Design authority: **`docs/design/deployment.md`** (Docker profile, `heart/` mapping table).
