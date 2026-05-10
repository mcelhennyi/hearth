# CURRENT — `feat/FR-0003-hearth-pi-docker-cli`

**FR:** `FR-0003` — Hearth Pi Docker CLI and install bootstrap  
**Feature folder:** `tasks/feature-history/FR-0003-hearth-pi-docker-cli/`  
**Branch role:** Feature integration branch  
**Last meaningful update:** 2026-05-10

## Landed on this feature branch

- **`T-FR-0003-01` done:** `docs/design/deployment.md` documents the Docker-on-Pi profile and bare-metal systemd alternative.
- **`T-FR-0003-02` done:** `deploy/hearth-install/` scaffolds the `heart/` layout, `VERSION.json` v1 parser/schema, templates, README, and `./develop test` path.
- **`T-FR-0003-13` done:** Hearth CLI parity rules are mirrored across Cursor and Claude guidance.
- **`T-FR-0003-04` done:** `bin/hearth` and `deploy/hearth-cli/` provide install-root resolution, `version`, `doctor`, and `compose --` passthrough with tests.
- **`T-FR-0003-05` done:** `deploy/hearth-install/` now manages `heart/state/plugins.yaml` and generates Compose plugin overrides.
- **`T-FR-0003-10` done:** `deploy/kindling-contract/` mirrors the plugin `scripts/install` + `plugin` template contract until Kindling exists upstream.
- Repo-root `./install` wrapper + `hearth_install.bootstrap` (dry-run, layout, shim, compose template, plugin overrides, `docker compose up -d`).
- **`T-FR-0003-03` done:** `./install` bootstraps Docker layout, shim, compose template, plugin overrides, and initial `docker compose up -d`.

## Validation

- Ticket branches individually passed their scoped Docker/Compose validation before merge.
- Feature-branch validation passed before PR #13: `./develop test` (19 tests).
- `T-FR-0003-03`: `./develop test` full suite PASS; host-local generated `docker compose config` PASS.

## Next

1. Merge remaining wave 5 ticket branches: `T-FR-0003-06`, `T-FR-0003-07`, and `T-FR-0003-09`.
2. Rerun `./develop test`.
3. Update PR #13 or a successor feature PR to `main`, noting that `CURRENT.md` should be removed when merged to `main`.
