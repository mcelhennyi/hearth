# CURRENT — `feat/FR-0003-hearth-pi-docker-cli`

**FR:** `FR-0003` — Hearth Pi Docker CLI and install bootstrap  
**Feature folder:** `tasks/feature-history/FR-0003-hearth-pi-docker-cli/`  
**Branch role:** Feature integration branch  
**Last meaningful update:** 2026-05-11

## Landed on this feature branch

- **`T-FR-0003-01` done:** `docs/design/deployment.md` documents the Docker-on-Pi profile and bare-metal systemd alternative.
- **`T-FR-0003-02` done:** `deploy/hearth-install/` scaffolds the `heart/` layout, `VERSION.json` v1 parser/schema, templates, README, and `./develop test` path.
- **`T-FR-0003-13` done:** Hearth CLI parity rules are mirrored across Cursor and Claude guidance.
- **`T-FR-0003-04` done:** `bin/hearth` and `deploy/hearth-cli/` provide install-root resolution, `version`, `doctor`, and `compose --` passthrough with tests.
- **`T-FR-0003-05` done:** `deploy/hearth-install/` now manages `heart/state/plugins.yaml` and generates Compose plugin overrides.
- **`T-FR-0003-10` done:** `deploy/kindling-contract/` mirrors the plugin `scripts/install` + `plugin` template contract until Kindling exists upstream.
- **`T-FR-0003-03` done:** `./install` bootstraps Docker layout, shim, compose template, plugin overrides, and initial `docker compose up -d`.
- **`T-FR-0003-06` done:** `hearth --update` supports dry-run, deploy git pull, plugin refresh, compose regeneration, optional migration hook, and compose restart.
- **`T-FR-0003-07` done:** `hearth --plugin --add` and `hearth --plugin list` install local/git plugins, validate MVP `tinder.toml`, update the registry, and regenerate Compose overrides.
- **`T-FR-0003-09` done:** `hearth start|stop|restart|status|logs` map to Docker Compose with stable project/env-file handling and optional hub health probing.
- **`T-FR-0003-08` done:** `hearth --plugin enter` supports plugin cwd selection, enter session environment, non-interactive fallback, and Kindling `plugin --exit`.
- **`T-FR-0003-11` done:** Per-plugin `plugin` executable supports lifecycle flags and admin passthrough via `hearth_plugin_cli`.
- **`T-FR-0003-12` done:** `scripts/ci/hearth-install-smoke.sh` plus `.github/workflows/hearth-install-smoke.yml` (amd64 + `ubuntu-24.04-arm`); see `serial-diary.md` for Pi hardware follow-up.

## Validation

- Ticket branches individually passed their scoped Docker/Compose validation before merge.
- Feature-branch validation passed before PR #13: `./develop test` (19 tests).
- Integrated feature validation after merging `T-FR-0003-03`, `-06`, `-07`, and `-09`: `docker compose -f deploy/compose/docker-compose.yml --profile test run --rm hearth-test` — PASS (`49 passed`).
- Integrated feature validation after merging `T-FR-0003-08` and `T-FR-0003-11`: `docker compose -f deploy/compose/docker-compose.yml --profile test run --rm hearth-test` — PASS (`76 passed`).
- `T-FR-0003-08`: `docker compose -f deploy/compose/docker-compose.yml --profile test run --rm hearth-test` — PASS (`59 passed`).
- `T-FR-0003-11`: `docker compose -f deploy/compose/docker-compose.yml --profile test run --rm hearth-test` — PASS (`66 passed`).
- After merge of **`T-FR-0003-12`**: `./develop test` — PASS (`76 passed`); `./scripts/ci/hearth-install-smoke.sh` — PASS on integration host.

## Next

1. Push **`feat/FR-0003-hearth-pi-docker-cli`** and ticket branch **`feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-12-smoke-arm-ci`** to `origin`.
2. Run **`/finish-feature`** (or open/update PR to **`main`**); remove repo-root **`CURRENT.md`** when the feature PR merges to **`main`** per process docs.
3. Optional: run **`scripts/ci/hearth-install-smoke.sh`** on a Pi-class host and append timing to `tasks/feature-history/FR-0003-hearth-pi-docker-cli/serial-diary.md`.
