# Next-step handoff - parallel frontier (2026-05-27, FR-0007 after T-FR-0007-01)

**Audience:** Next agent or maintainer picking up FR-0007 from `feat/FR-0007-kindling-mantle-migration`.
**Authority:** `tasks/feature-history/FR-0007-kindling-mantle-migration/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md` (DAG), `docs/ai-context.md`.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | `T-FR-0007-02` |
| **Active phase** | TEST -> DEV -> VAL |
| **Branch / worktree** | `feat/FR-0007-kindling-mantle-migration` @ `.worktrees/FR-0007-kindling-mantle-migration/feature/`; next ticket worktree `.worktrees/FR-0007-kindling-mantle-migration/T-FR-0007-02-move-mantle-package-source/` |
| **Session status** | `developing` |
| **Next agent should** | Start **Move Mantle package source to Kindling** (`T-FR-0007-02`) from the FR-0007 feature branch, update only its progress row, then merge to `feat/FR-0007-kindling-mantle-migration` and rerun `/identify-frontier`. |

**Triad-complete (FR-0007 summary):** **Contract and transition docs** (`T-FR-0007-01`).

**Still incomplete (FR-0007 summary):** `T-FR-0007-02` through `T-FR-0007-06`.

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in **Deps:** has **VAL** = `done` in `tasks/ticket-progress.md`.

With `T-FR-0007-01` VAL-done, this ticket is eligible:

| Ticket | Title | Deps |
|--------|-------|------|
| `T-FR-0007-02` | Move Mantle package source to Kindling | `T-FR-0007-01` |

So **up to 1 FR-0007 stream** is dependency-valid now: `feat/FR-0007-kindling-mantle-migration-T-FR-0007-02-move-mantle-package-source`.

**Examples of what stays blocked until more VAL-done rows exist:**

- **Rewire Hearth to consume Kindling Mantle** (`T-FR-0007-03`) waits for `T-FR-0007-02` VAL.
- **Standalone Kindling app template support** (`T-FR-0007-04`) waits for `T-FR-0007-02` VAL.
- **Mantle version compliance validation** (`T-FR-0007-05`) waits for `T-FR-0007-04` VAL.
- **Downstream app proof and migration note** (`T-FR-0007-06`) waits for `T-FR-0007-03`, `T-FR-0007-04`, and `T-FR-0007-05` VAL.

---

## Process note (queue vs graph)

T-FR-0007-02 is intentionally serial: it moves the package ownership boundary that unblocks both Hearth consumption and standalone template support. Do not start `T-FR-0007-03` or `T-FR-0007-04` until the package source move is VAL-done.

---

## Cross-cutting work (parallel to tickets)

- Initialize or verify the `kindling/` submodule before moving package files.
- Confirm whether the target Kindling package path is `mantle/` or a package workspace under Kindling before editing package metadata.
- Keep `packages/mantle/` transitional status explicit until it is removed, converted to fixtures, or documented as non-authoritative.

---

## First concrete steps (primary next ticket)

1. Create child worktree `.worktrees/FR-0007-kindling-mantle-migration/T-FR-0007-02-move-mantle-package-source/` from `feat/FR-0007-kindling-mantle-migration`.
2. Create branch `feat/FR-0007-kindling-mantle-migration-T-FR-0007-02-move-mantle-package-source`.
3. Read `packages/mantle/package.json`, `packages/mantle/README.md`, `packages/mantle/CHANGELOG.md`, and Kindling repo layout before moving files.
4. Follow TEST -> DEV -> VAL in `tasks/feature-history/FR-0007-kindling-mantle-migration/tickets.md`.

---

## Related files

- `tasks/ticket-progress.md`
- `tasks/feature-history/FR-0007-kindling-mantle-migration/tickets.md`
- `tasks/feature-history/FR-0007-kindling-mantle-migration/20-tickets-dag.md`
- `docs/design/tickets-initial.md`
- `docs/design/satellite-repos/kindling.md`
- `packages/mantle/`
- `kindling/`
