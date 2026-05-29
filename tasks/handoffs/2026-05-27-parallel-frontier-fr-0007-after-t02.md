# Next-step handoff — parallel frontier (2026-05-27)

**Audience:** Next agent or maintainer picking up FR-0007 from `feat/FR-0007-kindling-mantle-migration`.
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md` (DAG), `docs/ai-context.md`.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | `T-FR-0007-03`, `T-FR-0007-04` |
| **Active phase** | TEST |
| **Branch / worktree** | `feat/FR-0007-kindling-mantle-migration` @ `.worktrees/FR-0007-kindling-mantle-migration/feature/`; next ticket worktrees `.worktrees/FR-0007-kindling-mantle-migration/T-FR-0007-03-rewire-hearth-kindling-mantle/` and `.worktrees/FR-0007-kindling-mantle-migration/T-FR-0007-04-standalone-kindling-template/` |
| **Session status** | `developing` |
| **Next agent should** | Run `/develop-frontier` for `T-FR-0007-03` and `T-FR-0007-04` in separate child worktrees; keep all installs/tests inside the development container. |

**Triad-complete (summary):** `T-FR-0007-01` and `T-FR-0007-02` are TEST/DEV/VAL complete and merged into the FR-0007 feature branch.

**Still incomplete (summary):** `T-FR-0007-03`, `T-FR-0007-04`, `T-FR-0007-05`, and `T-FR-0007-06` remain incomplete.

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in **Deps:** has **VAL** = `done` in `tasks/ticket-progress.md`.

With `T-FR-0007-01` and `T-FR-0007-02` VAL-done, these tickets are eligible and mutually non-blocking:

| Ticket | Title | Deps |
|--------|-------|------|
| `T-FR-0007-03` | Rewire Hearth to consume Kindling Mantle | `T-FR-0007-02` |
| `T-FR-0007-04` | Standalone Kindling app template support | `T-FR-0007-02` |

So **up to 2 parallel streams** are dependency-valid: `feat/FR-0007-kindling-mantle-migration-T-FR-0007-03-rewire-hearth-kindling-mantle` and `feat/FR-0007-kindling-mantle-migration-T-FR-0007-04-standalone-kindling-template`, each under `.worktrees/FR-0007-kindling-mantle-migration/...`.

**Examples of what stays blocked until more VAL-done rows exist:**

- `T-FR-0007-05` waits on `T-FR-0007-01` and `T-FR-0007-04`, so it remains blocked until standalone template support is VAL-done.
- `T-FR-0007-06` waits on `T-FR-0007-03`, `T-FR-0007-04`, and `T-FR-0007-05`, so it remains the capstone proof/migration ticket.

Full **Deps:** edges: scan all `tasks/feature-history/**/tickets.md`; global mermaid in `docs/design/tickets-initial.md`.

---

## Process note (queue vs graph)

FR-0007 remains on the feature-branch workflow. Merge ticket branches back into `feat/FR-0007-kindling-mantle-migration`, revalidate there, and do not open a default-branch PR until every FR-0007 ticket is TEST/DEV/VAL done.

Development commands, package installs, builds, tests, and doc builds must run inside Docker / Docker Compose / the configured development container. The T02 diary records that host-local package validation was discarded after this rule was reasserted.

---

## Cross-cutting work (parallel to tickets)

- Keep `CURRENT.md`, `tasks/ticket-progress.md`, and per-ticket parallel diaries aligned when each child branch starts or completes.
- Do not treat Hearth `packages/mantle/` as authoritative; T02 removed it and advanced the Kindling submodule to the Mantle source commit.
- If T03 and T04 both need shared package/workspace metadata, coordinate through the feature branch before editing the same files in parallel.

---

## First concrete steps (primary next ticket)

1. Create child worktrees from `feat/FR-0007-kindling-mantle-migration` for `T-FR-0007-03` and `T-FR-0007-04`.
2. For each ticket, run TEST -> DEV -> VAL serially in that child worktree and update only the owned progress row.
3. Run installs/tests/builds through the development container. For Kindling package checks, activate the package manager inside the container with Corepack when needed.
4. Refresh repo-root `CURRENT.md` on the feature branch after each merge so the parallel set and next actions match this handoff.

---

## Related files

- `tasks/ticket-progress.md`
- `tasks/feature-history/FR-0007-kindling-mantle-migration/tickets.md`
- `tasks/feature-history/TICKET-SOURCES.md`
- `docs/design/tickets-initial.md` (global DAG + triadDone)
