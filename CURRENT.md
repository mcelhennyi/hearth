# CURRENT - FR-0007 Kindling Mantle migration

| Field | Value |
|-------|-------|
| **FR** | `FR-0007` |
| **Slug** | `FR-0007-kindling-mantle-migration` |
| **Branch** | `feat/FR-0007-kindling-mantle-migration-T-FR-0007-04-standalone-kindling-template` |
| **Role** | Ticket branch for `T-FR-0007-04` |

## State

`T-FR-0007-04` is TEST/DEV/VAL complete in this ticket worktree. Kindling's React template now renders a standalone `@kindling/mantle` dependency from local Kindling `mantle/`, builds local Mantle during generated-app install, imports Mantle token/component CSS, and keeps Mantle hooks under `MantleProvider`.

## Next Action

Commit and push this ticket branch, then let the frontier orchestrator merge it into `feat/FR-0007-kindling-mantle-migration` alongside the parallel T03 branch.

## Links

- `tasks/feature-history/FR-0007-kindling-mantle-migration/tickets.md`
- `tasks/handoffs/2026-05-27-parallel-frontier-fr-0007-after-t02.md`
- `tasks/ticket-progress.md`
