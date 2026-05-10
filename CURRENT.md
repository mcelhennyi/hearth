# Branch state — `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-11-plugin-executable`

**Ticket:** **T-FR-0003-11** — Per-plugin `plugin` executable: lifecycle + passthrough  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-11-plugin-executable/`

## Status

- **TEST / DEV / VAL:** complete for this ticket.
- **Validation:** `docker compose -f deploy/compose/docker-compose.yml --profile test run --rm hearth-test` — 66 passed.

## Next (for integrator)

- Open / merge **PR** with base **`feat/FR-0003-hearth-pi-docker-cli`** (do not merge to `main` from this ticket branch).
- Follow-up unblockers: **T-FR-0003-12** (smoke / ARM CI) after **T-FR-0003-08** and related tickets per DAG.
