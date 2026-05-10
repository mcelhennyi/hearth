# CURRENT — `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-09-stack-control`

**Ticket:** `T-FR-0003-09` — stack control (`start`, `stop`, `restart`, `status`, `logs`)  
**Feature:** `FR-0003` — Hearth Pi Docker CLI  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-09-stack-control/`  
**Last update:** 2026-05-10

## Phase

- **TEST:** done — stack/compose mapping and env-file tests in `tests/test_hearth_cli.py`.
- **DEV:** done — `deploy/hearth-cli/hearth_cli/cli.py` implements commands + shared compose prefix.
- **VAL:** done — `./develop test` (full suite) in Docker.

## Next

1. Push branch and open PR → `feat/FR-0003-hearth-pi-docker-cli`.
2. After merge, refresh feature `CURRENT.md` and rerun `./develop test` on the integration branch.

## Notes

- Compose project: `HEARTH_COMPOSE_PROJECT_NAME` (default `hearth`).
- Env file: `heart/compose/.env` or `HEARTH_COMPOSE_ENV_FILE`.
- Hub health on `hearth status`: `HEARTH_HUB_HEALTH_URL` or `docker compose port hub …`; use `--skip-health` to skip.
