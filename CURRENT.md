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
- **`T-FR-0003-03` done:** `./install` bootstraps Docker layout, shim, compose template, plugin overrides, and initial `docker compose up -d`.
- **`T-FR-0003-06` done:** `hearth --update` supports dry-run, deploy git pull, plugin refresh, compose regeneration, optional migration hook, and compose restart.
- **`T-FR-0003-07` done:** `hearth --plugin --add` and `hearth --plugin list` install local/git plugins, validate MVP `tinder.toml`, update the registry, and regenerate Compose overrides.
- **`T-FR-0003-09` done:** `hearth start|stop|restart|status|logs` map to Docker Compose with stable project/env-file handling and optional hub health probing.

## Validation

- Ticket branches individually passed their scoped Docker/Compose validation before merge.
- Feature-branch validation passed before PR #13: `./develop test` (19 tests).
- `T-FR-0003-03`: `./develop test` full suite PASS; host-local generated `docker compose config` PASS.
- `T-FR-0003-06`: `./develop test` PASS (26 tests); host-local `hearth --update --dry-run` no-op idempotence PASS.
- `T-FR-0003-07`: `./develop test` PASS (24 tests); Docker test image installs `git` for clone coverage.
- `T-FR-0003-09`: `./develop test tests/test_hearth_cli.py` and `./develop test` PASS in Docker.

## Next

1. Rerun `./develop test` on the integrated feature branch.
2. Identify the next frontier from the updated `feat/FR-0003-hearth-pi-docker-cli` state.
3. Update PR #13 or a successor feature PR to `main`, noting that `CURRENT.md` should be removed when merged to `main`.

## Notes

- Compose project: `HEARTH_COMPOSE_PROJECT_NAME` (default `hearth`).
- Env file: `heart/compose/.env` or `HEARTH_COMPOSE_ENV_FILE`.
- Hub health on `hearth status`: `HEARTH_HUB_HEALTH_URL` or `docker compose port hub …`; use `--skip-health` to skip.
