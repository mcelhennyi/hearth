# Next-step handoff — parallel frontier (2026-05-29)

**Audience:** Next agent or maintainer picking up FR-0007 from `feat/FR-0007-kindling-mantle-migration`.
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md` (DAG), `docs/ai-context.md`.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | `T-FR-0007-05` |
| **Active phase** | TEST |
| **Branch / worktree** | `feat/FR-0007-kindling-mantle-migration` @ `.worktrees/FR-0007-kindling-mantle-migration/feature/`; next ticket worktree `.worktrees/FR-0007-kindling-mantle-migration/T-FR-0007-05-mantle-version-compliance/` |
| **Session status** | `developing` |
| **Next agent should** | Run `/develop-frontier` for `T-FR-0007-05`; keep all installs/tests inside the development container. |

**Triad-complete (summary):** `T-FR-0007-01`, `T-FR-0007-02`, `T-FR-0007-03`, and `T-FR-0007-04` are TEST/DEV/VAL complete and merged into the FR-0007 feature branch.

**Still incomplete (summary):** `T-FR-0007-05` and `T-FR-0007-06` remain incomplete.

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in **Deps:** has **VAL** = `done` in `tasks/ticket-progress.md`.

With `T-FR-0007-01` and `T-FR-0007-04` VAL-done, this ticket is eligible:

| Ticket | Title | Deps |
|--------|-------|------|
| `T-FR-0007-05` | Mantle version compliance validation | `T-FR-0007-01`, `T-FR-0007-04` |

So **1 stream** is dependency-valid: `feat/FR-0007-kindling-mantle-migration-T-FR-0007-05-mantle-version-compliance` under `.worktrees/FR-0007-kindling-mantle-migration/...`.

**Examples of what stays blocked until more VAL-done rows exist:**

- `T-FR-0007-06` waits on `T-FR-0007-03`, `T-FR-0007-04`, and `T-FR-0007-05`, so it remains blocked until compliance validation lands.

Full **Deps:** edges: scan all `tasks/feature-history/**/tickets.md`; global mermaid in `docs/design/tickets-initial.md`.

---

## Process note (queue vs graph)

FR-0007 remains on the feature-branch workflow. Merge ticket branches back into `feat/FR-0007-kindling-mantle-migration`, revalidate there, and do not open a default-branch PR until every FR-0007 ticket is TEST/DEV/VAL done.

Development commands, package installs, builds, tests, and doc builds must run inside Docker / Docker Compose / the configured development container.

---

## Cross-cutting work (parallel to tickets)

- T03 wired Hearth hub web to consume `@kindling/mantle` from `kindling/mantle` through the pnpm workspace.
- T04 advanced the Kindling submodule to standalone React template support on Kindling commit `c2d9ddb`.
- T05 should add positive/negative compliance validation for supported `@kindling/mantle` ranges and Kindling compatibility metadata before install or release.

---

## First concrete steps (primary next ticket)

1. Create a child worktree from `feat/FR-0007-kindling-mantle-migration` for `T-FR-0007-05`.
2. Run TEST -> DEV -> VAL serially in that child worktree and update only the T05 progress row.
3. Run installs/tests/builds through the development container.
4. Refresh repo-root `CURRENT.md` on the feature branch after merge so the next action points at capstone `T-FR-0007-06`.

---

## Related files

- `tasks/ticket-progress.md`
- `tasks/feature-history/FR-0007-kindling-mantle-migration/tickets.md`
- `tasks/feature-history/TICKET-SOURCES.md`
- `docs/design/tickets-initial.md` (global DAG + triadDone)
