# Next-step handoff - parallel frontier (2026-05-27, FR-0007 scoped)

**Audience:** Next agent or maintainer picking up FR-0007 from `main`.
**Authority:** `tasks/feature-history/FR-0007-kindling-mantle-migration/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md` (DAG), `docs/ai-context.md`.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | grocery-list `T-FR-0001-01` -> `T-FR-0001-04` (serialized) |
| **Active phase** | TEST -> DEV -> VAL |
| **Branch / worktree** | `main` @ `25e3381`; grocery `feat/FR-0001-mvp-reference-plugin` @ `plugins/third-party/grocery-list/` |
| **Session status** | `developing` |
| **Next agent should** | For FR-0007, start **Contract and transition docs** (`T-FR-0007-01`) before moving package files. |

**Triad-complete (FR-0007 summary):** none.

**Still incomplete (FR-0007 summary):** all six FR-0007 tickets are incomplete.

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in **Deps:** has **VAL** = `done` in `tasks/ticket-progress.md`.

With no FR-0007 dependencies VAL-done yet, this ticket is eligible:

| Ticket | Title | Deps |
|--------|-------|------|
| `T-FR-0007-01` | Contract and transition docs | none |

So **up to 1 FR-0007 stream** is dependency-valid now: `feat/FR-0007-kindling-mantle-migration/T-FR-0007-01-contract-transition-docs`.

**Examples of what stays blocked until more VAL-done rows exist:**

- **Move Mantle package source to Kindling** (`T-FR-0007-02`) waits for `T-FR-0007-01` VAL.
- **Rewire Hearth to consume Kindling Mantle** (`T-FR-0007-03`) waits for `T-FR-0007-02` VAL.
- **Standalone Kindling app template support** (`T-FR-0007-04`) waits for `T-FR-0007-02` VAL.
- **Mantle version compliance validation** (`T-FR-0007-05`) waits for `T-FR-0007-01` and `T-FR-0007-04` VAL.
- **Downstream app proof and migration note** (`T-FR-0007-06`) waits for `T-FR-0007-03`, `T-FR-0007-04`, and `T-FR-0007-05` VAL.

Full **Deps:** edges live in `tasks/feature-history/FR-0007-kindling-mantle-migration/tickets.md`; global mermaid is in `docs/design/tickets-initial.md`.

---

## Process note (queue vs graph)

This handoff is intentionally scoped to `FR-0007` because the command request named `0007`. The global graph still has other incomplete work, but FR-0007 should begin with its contract/docs ticket so the package move has an explicit authority trail before touching Kindling, Hearth workspace wiring, or downstream app templates.

Implementation should follow the feature-branch workflow from `docs/ai-context.md` §2d. The previous FR registration used a clean planning worktree at `.worktrees/FR-0007-kindling-mantle-migration`; before implementation, create or normalize the feature integration checkout for branch `feat/FR-0007-kindling-mantle-migration` and add repo-root `CURRENT.md` there.

---

## Cross-cutting work (parallel to tickets)

- Initialize or verify the `kindling/` submodule before package-move work.
- Coordinate with any standalone app repo used as the proof target, especially Planwright or the current reference plugin.
- Keep Kindling changelog entries dense enough for downstream migration agents: who must update, required edits, verification, and fallback.

---

## First concrete steps (primary next ticket)

1. Create or refresh the feature integration branch `feat/FR-0007-kindling-mantle-migration`.
2. Create a child branch/worktree for **Contract and transition docs** (`T-FR-0007-01`) from that feature branch.
3. In TEST, add a doc/checklist failure that proves the Kindling ownership/compatibility contract is not fully captured yet.
4. In DEV, amend `docs/design/satellite-repos/kindling.md` and FR-0007 docs so the source move, compatibility model, and transitional `packages/mantle/` status are explicit.
5. In VAL, run Docker MkDocs build; record strict-mode warnings if they are still pre-existing repo-wide warnings.
6. Refresh repo-root `CURRENT.md` on `feat/FR-0007-kindling-mantle-migration` so the next frontier after `T-FR-0007-01` points to `T-FR-0007-02`.

---

## Related files

- `tasks/ticket-progress.md`
- `tasks/feature-history/FR-0007-kindling-mantle-migration/tickets.md`
- `tasks/feature-history/FR-0007-kindling-mantle-migration/20-tickets-dag.md`
- `tasks/feature-history/TICKET-SOURCES.md`
- `docs/design/tickets-initial.md`
- `docs/design/satellite-repos/kindling.md`
