# Current branch state

**Branch:** `feat/FR-0001-hearth-platform-T-FR-0001-01-repo-scaffold`
**Ticket:** T-FR-0001-01 — Repo scaffold and Compose dev loop
**Status:** VAL complete — PR open for merge into `feat/FR-0001-hearth-platform`

## What was done

- TEST: `tests/smoke/dev-loop.sh` written and passing
- DEV: `.dockerignore` for api and web, root `package.json` + `pnpm-workspace.yaml`, `deploy/static/index.html` updated to "Hearth — placeholder"
- VAL: Smoke test passed on host (HTTP 200, body contains "Hearth"); host-only exception documented in `tasks/feature-history/FR-0001-hearth-platform/serial-diary.md`

## Next step

Merge this PR into `feat/FR-0001-hearth-platform`, then start T-FR-0001-02 (Hub API skeleton and SQLite registry).
