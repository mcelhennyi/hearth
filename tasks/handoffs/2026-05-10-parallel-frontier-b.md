# Next-step handoff — parallel frontier (2026-05-10)

**Audience:** Next agent or maintainer picking up work from `feat/FR-0003-hearth-pi-docker-cli`.  
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md` (DAG), `docs/ai-context.md`.  
**Context:** FR-0003 wave 5 ticket PRs were merged into the feature branch: `T-FR-0003-03`, `T-FR-0003-06`, `T-FR-0003-07`, and `T-FR-0003-09`. Integrated validation passed with `docker compose -f deploy/compose/docker-compose.yml --profile test run --rm hearth-test` (`49 passed`).

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | `/identify-frontier 0003` after wave 5 integration: `T-FR-0003-08` and `T-FR-0003-11` are dependency-eligible from `feat/FR-0003-hearth-pi-docker-cli`; FR-0002 `T-FR-0002-01` VAL and `T-FR-0002-02` remain eligible in parallel. |
| **Active phase** | `handoff` — wave 5 merged, feature tests pass. |
| **Branch / worktree** | Feature: `.worktrees/FR-0003-hearth-pi-docker-cli/feature/` → `feat/FR-0003-hearth-pi-docker-cli`. |
| **Session status** | `handoff` |
| **Next agent should** | Start one stream each for `T-FR-0003-08` and `T-FR-0003-11`, or continue FR-0002 if that feature is priority. |

**Triad-complete (summary):** `T-FR-0000-01`; FR-0003 `T-FR-0003-01`, `-02`, `-03`, `-04`, `-05`, `-06`, `-07`, `-09`, `-10`, `-13`.

**Still incomplete (summary):** FR-0003 `T-FR-0003-08`, `-11`, `-12`; FR-0002 `T-FR-0002-01` VAL, `T-FR-0002-02`, `-03`, `-04`; FR-0001 remains parked.

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in `Deps:` has `VAL` = `done` in `tasks/ticket-progress.md`.

With FR-0003 `T-FR-0003-07` and `T-FR-0003-10` VAL-done, these tickets are eligible and mutually non-blocking:

| Ticket | Title | Deps |
|--------|-------|------|
| `T-FR-0003-08` | `hearth --plugin enter` | `T-FR-0003-07` |
| `T-FR-0003-11` | Per-plugin `plugin` executable: lifecycle + passthrough | `T-FR-0003-07`, `T-FR-0003-10` |

So **two FR-0003 streams** are dependency-valid now: `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-08-plugin-enter` and `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-11-plugin-executable`, each under `.worktrees/FR-0003-hearth-pi-docker-cli/`.

**Examples of what stays blocked until more VAL-done rows exist:**

- `T-FR-0003-12` — needs `T-FR-0003-03`, `T-FR-0003-06`, `T-FR-0003-08`, `T-FR-0003-09`, and `T-FR-0003-11`; only `-08` and `-11` remain.
- `T-FR-0002-03` — needs `T-FR-0002-01` and `T-FR-0002-02` VAL-done.
- FR-0001 tickets remain parked by policy even where graph deps would otherwise allow work.

Full `Deps:` edges: scan all `tasks/feature-history/**/tickets.md`; global mermaid in `docs/design/tickets-initial.md`.

---

## Process note (queue vs graph)

This handoff is based on the FR-0003 feature branch, not `main`. `main` may still lag until the feature PR is refreshed and reviewed. For FR-0003 ticket streams, branch from `feat/FR-0003-hearth-pi-docker-cli` and merge ticket PRs back into that feature branch first.

The global graph also permits FR-0002 work in parallel: `T-FR-0002-01` remains incomplete because server-first VAL is still open, and `T-FR-0002-02` is eligible with no deps. Keep those streams under the FR-0002 feature worktree.

---

## Cross-cutting work (parallel to tickets)

- Keep `CURRENT.md` on `feat/FR-0003-hearth-pi-docker-cli` aligned as ticket branches land.
- When `T-FR-0003-08` or `T-FR-0003-11` reaches VAL, update only that ticket's progress row and union the corresponding `triadDone` line in `docs/design/tickets-initial.md`.
- The repo-root `./develop test` wrapper is not available on this branch; use the explicit Compose test service command until the wrapper regains a test subcommand.

---

## First concrete steps

1. Create child worktrees from `feat/FR-0003-hearth-pi-docker-cli` for `T-FR-0003-08` and `T-FR-0003-11`.
2. Run TEST → DEV → VAL per each ticket in `tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`.
3. Validate in Docker with `docker compose -f deploy/compose/docker-compose.yml --profile test run --rm hearth-test`.
4. Merge both ticket PRs into the FR-0003 feature branch, then identify `T-FR-0003-12` as the final FR-0003 capstone ticket.

---

## Related files

- `tasks/ticket-progress.md`
- `tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`
- `tasks/feature-history/FR-0002-iphone-pwa-prototype/tickets.md`
- `tasks/feature-history/TICKET-SOURCES.md`
- `docs/design/tickets-initial.md`
