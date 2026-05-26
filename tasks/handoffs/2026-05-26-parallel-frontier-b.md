# Next-step handoff — parallel frontier (2026-05-26-b)

**Audience:** Next agent or maintainer picking up after the T13/T14 integration on `feat/FR-0004-centralized-users-auth`.
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md` (DAG), `docs/ai-context.md`.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | `T-FR-0004-15` — Admin user management API and settings UI |
| **Active phase** | TEST → DEV → VAL |
| **Branch / worktree** | `feat/FR-0004-centralized-users-auth` @ `.worktrees/FR-0004-centralized-users-auth/feature/`; next child worktree `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-15-admin-user-management/` |
| **Session status** | `developing` |
| **Next agent should** | Run `T-FR-0004-15`, update only its progress row, push the ticket branch, and merge back to `feat/FR-0004-centralized-users-auth`. |

**Triad-complete (summary):** `T-FR-0004-01` through `T-FR-0004-14` are TEST/DEV/VAL `done` in the feature branch tracker. All FR-0006 tickets are also done from the merged main baseline.

**Still incomplete (summary):** `T-FR-0004-15`, `T-FR-0004-16`, and the FR-0005 design tickets remain incomplete.

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in **Deps:** has **VAL** = `done` in `tasks/ticket-progress.md`.

With `T-FR-0004-12` and `T-FR-0004-14` VAL-done, these tickets are eligible and mutually non-blocking:

| Ticket | Title | Deps |
|--------|-------|------|
| `T-FR-0004-15` | Admin user management API and settings UI | `T-FR-0004-12`, `T-FR-0004-14` |
| `T-FR-0005-01` | Remote-build profile in deployment.md | `none` |

So **up to 2 parallel streams** are dependency-valid. This table mixes `FR-0004` and `FR-0005` because `docs/ai-context.md` §2c defines one global dependency graph.

**Recommended scope:** continue FR-0004 first unless FR-0005 is explicitly prioritized. `T-FR-0005-01` is eligible but still belongs to the FR-0005 design line.

**Examples of what stays blocked until more VAL-done rows exist:**

- `T-FR-0004-16` stays blocked until `T-FR-0004-13`, `T-FR-0004-14`, and `T-FR-0004-15` are all VAL `done`; only T15 is missing now.
- `T-FR-0005-02` and `T-FR-0005-03` stay blocked until `T-FR-0005-01` is VAL `done`.

Full **Deps:** edges: scan all `tasks/feature-history/**/tickets.md`; global mermaid and `triadDone` lines live in `docs/design/tickets-initial.md`.

---

## Process note (queue vs graph)

Do not run `finish-feature` for FR-0004 yet. PR #56 remains a feature preview until `T-FR-0004-11` through `T-FR-0004-16` are all TEST/DEV/VAL `done`.

T13 and T14 were merged into `feat/FR-0004-centralized-users-auth` and the feature branch was pushed at `df16df1`.

---

## Cross-cutting work (parallel to tickets)

- Keep the dense child-repo compliance changelog current if T15 changes Kindling, Mantle, auth, or generated template contracts.
- After T15 completes, update only its progress row plus the `TFR0004_15` `triadDone` line.
- Preserve the feature-branch workflow: ticket PRs target `feat/FR-0004-centralized-users-auth`; no default-branch PR for FR-0004 until the §2d feature-complete gate passes.

---

## First concrete steps (primary next ticket)

1. Create `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-15-admin-user-management/` from `origin/feat/FR-0004-centralized-users-auth`.
2. Run T15 TEST → DEV → VAL for the admin user management API and settings UI.
3. Merge T15 back into `feat/FR-0004-centralized-users-auth`, revalidate, and push.
4. Rerun `/identify-frontier`; the expected final FR-0004 ticket after T15 is `T-FR-0004-16`.

---

## Related files

- `tasks/ticket-progress.md`
- `tasks/feature-history/FR-0004-centralized-users-auth/tickets.md`
- `tasks/feature-history/TICKET-SOURCES.md`
- `docs/design/tickets-initial.md` (global DAG + triadDone)
