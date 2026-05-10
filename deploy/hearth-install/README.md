# `deploy/hearth-install/` — Docker profile `heart/` layout

**Tickets:** [`T-FR-0003-02`](../../tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-02--install-layout-heart-versionjson-readme), [`T-FR-0003-05`](../../tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-05--plugin-registry-file--compose-fragment-generation)

## Contents

| Path | Role |
|------|------|
| [`schemas/version-1.schema.json`](schemas/version-1.schema.json) | JSON Schema for **`heart/VERSION.json`** (manifest v1) |
| [`hearth_install/`](hearth_install/) | Python package: idempotent layout generator, plugin registry reader, Compose fragment generator |
| [`hearth_install/templates/README.heart.md`](hearth_install/templates/README.heart.md) | Copied to **`<install-dir>/heart/README.md`** |
| [`hearth_install/templates/VERSION.json.example`](hearth_install/templates/VERSION.json.example) | Non-secret example manifest (same shape as generated default) |

## Usage

From the repo root (after `pip install -e .` or inside **`./develop test`**):

```bash
python -m hearth_install /path/to/parent-of-heart --hearth-ref "$(git rev-parse HEAD)"
```

Generate the plugin override fragment from **`heart/state/plugins.yaml`**:

```bash
python -m hearth_install /path/to/parent-of-heart --generate-plugin-compose
```

The generator writes **`heart/compose/overrides/generated.plugins.yml`**. Registry rows are schema-v1 YAML:

```yaml
schema: 1
plugins:
  - slug: groceries
    source_git: https://example.test/groceries.git
    enabled: true
    image: ghcr.io/example/groceries:0.1.0
    port: 8201
    env:
      GROCERIES_MODE: prod
```

Design authority: **`docs/design/deployment.md`** (Docker profile, `heart/` mapping table).
