# Next-step handoff — parallel frontier (2026-05-26)

**Audience:** Next agent or maintainer picking up work from `feat/FR-0004-centralized-users-auth` or `main`.
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md` (DAG), `docs/ai-context.md`.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | `T-FR-0004-12` — Users plugin: multi-user schema, migration, and auth API |
| **Active phase** | TEST → DEV → VAL |
| **Branch / worktree** | `feat/FR-0004-centralized-users-auth-T-FR-0004-12-multi-user-auth-api` at `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-12-multi-user-auth-api/` |
| **Session status** | `developing` |
| **Next agent should** | Review/merge PR #60 for `T-FR-0004-12` into `feat/FR-0004-centralized-users-auth`, then rerun `/identify-frontier` or proceed to `T-FR-0004-13` and `T-FR-0004-14` if the tracker is updated to VAL-done for T12. |

**Triad-complete (summary):** `T-FR-0000-01`, all tracked `T-FR-0001-*`, all tracked `T-FR-0002-*`, all tracked `T-FR-0003-*`, `T-FR-0004-01` through `T-FR-0004-11`, and all `T-FR-0006-*` are TEST/DEV/VAL `done` in the current feature-branch tracker.

**Still incomplete (summary):** On the feature branch, `T-FR-0004-12` through `T-FR-0004-16` and `T-FR-0005-01` through `T-FR-0005-05` remain incomplete. A completed T12 ticket branch exists at PR #60 but is not yet merged into the feature branch tracker as of this handoff.

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in **Deps:** has **VAL** = `done` in `tasks/ticket-progress.md`.

With `T-FR-0004-11` and the prior FR-0004 foundation tickets VAL-done, and with `T-FR-0005-01` declaring `Deps: none`, these tickets are eligible and mutually non-blocking in the current feature-branch tracker:

| Ticket | Title | Deps |
|--------|-------|------|
| `T-FR-0004-12` | Users plugin: multi-user schema, migration, and auth API | `T-FR-0004-11` |
| `T-FR-0005-01` | Remote-build profile in deployment.md | `none` |

So **up to 2 parallel streams** are dependency-valid: `feat/FR-0004-centralized-users-auth/T-FR-0004-12-...` and `feat/FR-0005-remote-build-pi-deploy/T-FR-0005-01-...` per ticket, each under its owning `.worktrees/FR-NNNN-<slug>/...` folder.

This table intentionally mixes tickets from different product features (`FR-0004` and `FR-0005`) because `docs/ai-context.md` §2c defines one global dependency graph.

**Important timing note:** `T-FR-0004-12` has completed on its ticket branch and was pushed as PR #60. Once PR #60 is merged and `tasks/ticket-progress.md` marks T12 VAL `done` on `feat/FR-0004-centralized-users-auth`, the expected FR-0004 frontier becomes:

| Ticket | Title | Deps |
|--------|-------|------|
| `T-FR-0004-13` | Hearth Users UI: first admin setup and username login | `T-FR-0004-12` |
| `T-FR-0004-14` | Session, Spark, gateway, and Mantle claims use real users | `T-FR-0004-12` |
| `T-FR-0005-01` | Remote-build profile in deployment.md | `none` |

**Examples of what stays blocked until more VAL-done rows exist:**

- `T-FR-0004-13` and `T-FR-0004-14` stay blocked on the feature branch until `T-FR-0004-12` is merged and marked VAL `done`.
- `T-FR-0004-15` stays blocked until both `T-FR-0004-12` and `T-FR-0004-14` are VAL `done`.
- `T-FR-0004-16` stays blocked until `T-FR-0004-13`, `T-FR-0004-14`, and `T-FR-0004-15` are VAL `done`.
- `T-FR-0005-02` and `T-FR-0005-03` stay blocked until `T-FR-0005-01` is VAL `done`; `T-FR-0005-04` and `T-FR-0005-05` stay blocked until `T-FR-0005-02` is VAL `done`.

Full **Deps:** edges: scan all `tasks/feature-history/**/tickets.md`; global mermaid and `triadDone` lines live in `docs/design/tickets-initial.md`.

---

## Process note (queue vs graph)

`tasks/ticket-progress.md` is the queue beacon for what is active right now; the dependency graph can still show additional eligible work across other features. For this snapshot, `T-FR-0004-12` is the active FR-0004 ticket, while `T-FR-0005-01` is independently eligible but still in design status and should only be staffed if the maintainer explicitly wants FR-0005 work to begin in parallel.

Do not run `finish-feature` for FR-0004 yet. PR #56 remains a feature preview until `T-FR-0004-11` through `T-FR-0004-16` are all TEST/DEV/VAL `done`.

---

## Cross-cutting work (parallel to tickets)

- Keep the FR-0004 dense child-repo compliance changelog current for every Kindling/template/auth contract change so downstream repos can update without re-auditing the full upstream diff.
- After each completed ticket merge, update only the owned progress row in `tasks/ticket-progress.md`, then coordinate global `triadDone` updates in `docs/design/tickets-initial.md`.
- Preserve the feature-branch workflow: ticket PRs target `feat/FR-0004-centralized-users-auth`; no default-branch PR for FR-0004 until the §2d feature-complete gate passes.

---

## First concrete steps (primary next ticket)

1. Review PR #60 (`T-FR-0004-12`) and merge it into `feat/FR-0004-centralized-users-auth`.
2. Re-run validation on the feature branch after the merge, including the T12 focused tests and a broader project test pass.
3. Update `tasks/ticket-progress.md` and `docs/design/tickets-initial.md` so `T-FR-0004-12` is TEST/DEV/VAL `done` and has `triadDone`.
4. Rerun `/identify-frontier`; if the tracker reflects T12 done, staff `T-FR-0004-13` and `T-FR-0004-14` in parallel.
5. If `feat/*` implementation branches are in scope, refresh repo-root `CURRENT.md` on each affected `feat/FR-NNNN-<slug>` branch so the parallel set and next actions match this handoff.

---

## Related files

- `tasks/ticket-progress.md`
- `tasks/feature-history/**/tickets.md`
- `tasks/feature-history/TICKET-SOURCES.md`
- `docs/design/tickets-initial.md` (global DAG + triadDone)
