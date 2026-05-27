# CURRENT - FR-0007 Kindling Mantle migration

| Field | Value |
|-------|-------|
| **FR** | `FR-0007` |
| **Slug** | `FR-0007-kindling-mantle-migration` |
| **Branch** | `feat/FR-0007-kindling-mantle-migration-T-FR-0007-02-move-mantle-package-source` |
| **Role** | Ticket branch for `T-FR-0007-02` |

## State

`T-FR-0007-02` completed TEST, DEV, and VAL. `@kindling/mantle` source, tests, README, changelog, package metadata, and build config now live in the Kindling submodule at `kindling/mantle/`; the Hearth-local `packages/mantle/` source tree has been removed.

## Next Action

Merge this ticket branch back into `.worktrees/FR-0007-kindling-mantle-migration/feature/`, then rerun `/identify-frontier`. Expected next eligible tickets are **Rewire Hearth to consume Kindling Mantle** (`T-FR-0007-03`) and **Standalone Kindling app template support** (`T-FR-0007-04`).

## Links

- `tasks/feature-history/FR-0007-kindling-mantle-migration/tickets.md`
- `tasks/handoffs/2026-05-27-parallel-frontier-fr-0007.md`
- `tasks/ticket-progress.md`
