# Next-step handoff — parallel frontier (2026-05-26-c)

**Audience:** Next agent or maintainer picking up after the T15 integration on `feat/FR-0004-centralized-users-auth`.
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md` (DAG), `docs/ai-context.md`.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | `T-FR-0004-15` — Admin user management API and settings UI |
| **Active phase** | TEST → DEV → VAL |
| **Branch / worktree** | `feat/FR-0004-centralized-users-auth` @ `.worktrees/FR-0004-centralized-users-auth/feature/`; completed child worktree `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-15-admin-user-management/` |
| **Session status** | `developing` |
| **Next agent should** | Advance to `T-FR-0004-16`, the final multi-user E2E/compliance ticket, then run `finish-feature` only if the §2d feature-complete gate passes. |

**Triad-complete (summary):** `T-FR-0004-01` through `T-FR-0004-15` are TEST/DEV/VAL `done` in the feature branch tracker.

**Still incomplete (summary):** `T-FR-0004-16` remains incomplete. FR-0005 design tickets remain independently incomplete and eligible only if prioritized.

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in **Deps:** has **VAL** = `done` in `tasks/ticket-progress.md`.

With `T-FR-0004-13`, `T-FR-0004-14`, and `T-FR-0004-15` VAL-done, these tickets are eligible:

| Ticket | Title | Deps |
|--------|-------|------|
| `T-FR-0004-16` | Multi-user E2E and compliance changelog refresh | `T-FR-0004-13`, `T-FR-0004-14`, `T-FR-0004-15` |
| `T-FR-0005-01` | Remote-build profile in deployment.md | `none` |

So **up to 2 parallel streams** are dependency-valid globally. For FR-0004 closeout, staff `T-FR-0004-16` next and leave FR-0005 aside unless explicitly requested.

**Examples of what stays blocked until more VAL-done rows exist:**

- FR-0004 `finish-feature` stays blocked until `T-FR-0004-16` is TEST/DEV/VAL `done`.
- `T-FR-0005-02` and `T-FR-0005-03` stay blocked until `T-FR-0005-01` is VAL `done`.

---

## Process note (queue vs graph)

Do not run `finish-feature` for FR-0004 until `T-FR-0004-16` completes. PR #56 remains a feature preview until every `T-FR-0004-11` through `T-FR-0004-16` row is done.

T15 was merged into `feat/FR-0004-centralized-users-auth` and the feature branch was pushed at `b1f6feb`.

---

## Cross-cutting work (parallel to tickets)

- T16 must refresh the dense child-repo compliance changelog for any Kindling, Mantle, auth header, gateway, or generated-template contract changes across the multi-user wave.
- After T16 completes, update `TFR0004_16` `triadDone`, revalidate the full feature branch, then run `finish-feature` if the §2d gate passes.
- Preserve the feature-branch workflow: no default-branch PR for FR-0004 until feature closeout is complete.

---

## First concrete steps (primary next ticket)

1. Create `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-16-multi-user-e2e-compliance/` from `origin/feat/FR-0004-centralized-users-auth`.
2. Run T16 TEST → DEV → VAL for multi-user E2E and compliance changelog refresh.
3. Merge T16 back into `feat/FR-0004-centralized-users-auth`, run full validation, and push.
4. If every FR-0004 ticket row is done, run `finish-feature` for FR-0004.

---

## Related files

- `tasks/ticket-progress.md`
- `tasks/feature-history/FR-0004-centralized-users-auth/tickets.md`
- `tasks/feature-history/TICKET-SOURCES.md`
- `docs/design/tickets-initial.md` (global DAG + triadDone)
