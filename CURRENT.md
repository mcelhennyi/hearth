# Current branch state

| Field | Value |
|------|--------|
| **FR** | FR-0003 |
| **Feature folder** | `tasks/feature-history/FR-0003-hearth-pi-docker-cli/` |
| **This branch** | `feat/FR-0003-hearth-pi-docker-cli` (feature integration) |
| **Parent branch** | `main` |
| **Last meaningful update** | 2026-05-10 |

## What is on this branch

- Registry + tracker alignment: FR-0003 **`in-progress`**; scheduling-only park (**option A**) superseded for implementation.
- Code: none yet — policy/docs branch until **`T-FR-0003-01`** DEV starts.

## In flight / blockers

- None. FR-0002 does not gate FR-0003 in **`tickets.md`**. Use Compose fixtures and optional hub health checks per **`10-design-00-skeleton.md`** until hub + web surfaces land.

## Next

1. **[T-FR-0003-01 — Design contract: amend deployment for Docker-on-Pi](tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md)** — TEST → DEV → VAL, or run **`/identify-frontier`** if batching with other eligible globals.
2. Create ticket branch + worktree under **`.worktrees/FR-0003-hearth-pi-docker-cli/`** when starting DEV.
3. Refresh **`tasks/ticket-progress.md`** as phases complete.
