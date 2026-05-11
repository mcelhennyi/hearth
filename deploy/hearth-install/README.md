# `deploy/hearth-install/` — Docker profile `heart/` layout

**Tickets:** [`T-FR-0003-02`](../../tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-02--install-layout-heart-versionjson-readme), [`T-FR-0003-05`](../../tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-05--plugin-registry-file--compose-fragment-generation), [`T-FR-0003-03`](../../tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-03--install-bootstrap-docker--layout--first-compose-up), [`T-FR-0003-08`](../../tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-08--hearth--plugin-enter)

## Repo-root `./install` (bootstrap)

From the deploy checkout root:

```bash
./install --dry-run ~/hearth-deploy          # print planned steps only
./install ~/hearth-deploy                    # layout + shim + compose + docker compose up -d
HEARTH_INSTALL_ROOT=~/hearth-deploy ./install --skip-compose-up
```

Heavy logic lives in `hearth_install.bootstrap`; the `./install` file is a thin `PYTHONPATH` wrapper. Docker Engine installation is **not** automated (unsafe to mutate the host from this script); missing Docker yields a clear message pointing at [Docker Engine install](https://docs.docker.com/engine/install/) and the Pi `get.docker.com` flow.

The generated **`heart/compose/docker-compose.yml`** is an MVP **hub-smoke** placeholder (`alpine` sleep) plus `include` of plugin overrides until FR-0001 hub images exist. Requires a Compose implementation that supports the top-level **`include`** field (Docker Compose **v2.20+**).

## Contents

| Path | Role |
|------|------|
| [`schemas/version-1.schema.json`](schemas/version-1.schema.json) | JSON Schema for **`heart/VERSION.json`** (manifest v1) |
| [`hearth_install/`](hearth_install/) | Python package: idempotent layout generator, plugin registry reader, Compose fragment generator, **`bootstrap`** (`python -m hearth_install.bootstrap`) |
| [`hearth_install/templates/docker-compose.install.yml`](hearth_install/templates/docker-compose.install.yml) | Copied to **`heart/compose/docker-compose.yml`** on `./install` (placeholder hub + `include` of plugin overrides) |
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

## `hearth --plugin enter` / `./plugin --exit` (T-FR-0003-08)

From an interactive **bash** or **zsh** session, `hearth --plugin enter` (optional `--slug`; otherwise a numbered picker) **`exec`s your login shell** (`$SHELL -i`) with `cwd` under **`heart/plugins/<slug>/`** and records the previous directory in **`HEARTH_PLUGIN_ENTER_FROM`** plus a JSON stack in **`HEARTH_PLUGIN_ENTER_STACK`** so **`./plugin --exit`** (Kindling template / per-plugin shim) can **`chdir`** back.

If **stdin/stdout is not a TTY** (scripts/CI), pass **`--slug`** and **`hearth`** prints **`cd`** + **`export`** lines instead of replacing the process.

Full **enter → `./plugin status` → `--exit`** still requires a TTY (or a manual subshell); automated coverage is via **`tests/test_plugin_enter_session.py`** and CLI **`execve`** checks in **`tests/test_hearth_plugin_commands.py`**.
