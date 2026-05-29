# CURRENT - FR-0007 Kindling Mantle migration

| Field | Value |
|-------|-------|
| **FR** | `FR-0007` |
| **Slug** | `FR-0007-kindling-mantle-migration` |
| **Branch** | `feat/FR-0007-kindling-mantle-migration` |
| **Role** | Feature integration branch |

## State

`T-FR-0007-01` and `T-FR-0007-02` are complete and merged. `@kindling/mantle` source, tests, README, changelog, package metadata, and build config now live in the Kindling submodule at `kindling/mantle/`; the Hearth-local `packages/mantle/` source tree has been removed.

## Next Action

Run the next frontier: **Rewire Hearth to consume Kindling Mantle** (`T-FR-0007-03`) and **Standalone Kindling app template support** (`T-FR-0007-04`) are dependency-eligible and may proceed in parallel from this feature branch.

## Links

- `tasks/feature-history/FR-0007-kindling-mantle-migration/tickets.md`
- `tasks/handoffs/2026-05-27-parallel-frontier-fr-0007-after-t02.md`
- `tasks/ticket-progress.md`
