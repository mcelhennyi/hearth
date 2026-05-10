# Branch state — T-FR-0003-08 (`hearth --plugin enter`)

**Branch:** `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-08-plugin-enter`  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-08-plugin-enter/`

## Done (TEST → DEV → VAL)

- `hearth_install.plugin_session` + `hearth --plugin enter [--slug]` + Kindling `./plugin --exit`.
- Tests: `docker compose -f deploy/compose/docker-compose.yml --profile test run --rm hearth-test` → **59 passed**.
- Tracker: `tasks/ticket-progress.md` row **T-FR-0003-08**; DAG triad in `docs/design/tickets-initial.md`; diary `tasks/feature-history/FR-0003-hearth-pi-docker-cli/serial-diary.md`.

## Next

- Open **PR base `feat/FR-0003-hearth-pi-docker-cli`** (human merge into feature branch).
