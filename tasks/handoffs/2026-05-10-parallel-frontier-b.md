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

**Still incomplete (summary):** FR-0003 `T-FR-0003-08`, `-11`, `-12`; FR-0002 `T-FR-0002-01` VAL, `T-FR-0002-02`, `-03`, `-04`; FR-0001 remains parked by policy.

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in `Deps:` has `VAL` = `done` in `tasks/ticket-progress.md`.

With FR-0003 `T-FR-0003-07` and `T-FR-0003-10` VAL-done, and with FR-0002 `T-FR-0002-01` / `T-FR-0002-02` both having `Deps: none`, these tickets are eligible and mutually non-blocking:

| Ticket | FR | Title | Deps |
|--------|----|-------|------|
| `T-FR-0002-01` | FR-0002 | Caddy + `tls internal` + static placeholder | `none` |
| `T-FR-0002-02` | FR-0002 | Mantle PWA bones | `none` |
| `T-FR-0003-08` | FR-0003 | `hearth --plugin enter` | `T-FR-0003-07` |
| `T-FR-0003-11` | FR-0003 | Per-plugin `plugin` executable: lifecycle + passthrough | `T-FR-0003-07`, `T-FR-0003-10` |

So **four implementation streams** are dependency-valid now across the global graph:

- `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls` under `.worktrees/FR-0002-iphone-pwa-prototype/`
- `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones` under `.worktrees/FR-0002-iphone-pwa-prototype/`
- `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-08-plugin-enter` under `.worktrees/FR-0003-hearth-pi-docker-cli/`
- `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-11-plugin-executable` under `.worktrees/FR-0003-hearth-pi-docker-cli/`

**Policy-excluded despite graph eligibility:** `T-FR-0001-01` has `Deps: none`, but FR-0001 is parked until FR-0002 closes or the registry policy changes.

**Examples of what stays blocked until more VAL-done rows exist:**

- `T-FR-0003-12` — needs `T-FR-0003-03`, `T-FR-0003-06`, `T-FR-0003-08`, `T-FR-0003-09`, and `T-FR-0003-11`; only `-08` and `-11` remain.
- `T-FR-0002-03` — needs `T-FR-0002-01` and `T-FR-0002-02` VAL-done.
- FR-0001 tickets remain parked by policy even where graph deps would otherwise allow work.

Full `Deps:` edges: scan all `tasks/feature-history/**/tickets.md`; global mermaid in `docs/design/tickets-initial.md`.

---

## Process note (queue vs graph)

This handoff is based on the FR-0003 feature branch, not `main`. `main` may still lag until the feature PR is refreshed and reviewed. For FR-0003 ticket streams, branch from `feat/FR-0003-hearth-pi-docker-cli` and merge ticket PRs back into that feature branch first.

The global graph mixes FR-0002 and FR-0003 in this frontier, which is expected under `docs/ai-context.md` §2c. Keep FR-0002 streams under the FR-0002 feature worktree and FR-0003 streams under the FR-0003 feature worktree.

---

## Cross-cutting work (parallel to tickets)

- Keep `CURRENT.md` on `feat/FR-0003-hearth-pi-docker-cli` aligned as ticket branches land.
- When `T-FR-0003-08` or `T-FR-0003-11` reaches VAL, update only that ticket's progress row and union the corresponding `triadDone` line in `docs/design/tickets-initial.md`.
- The repo-root `./develop test` wrapper is not available on this branch; use the explicit Compose test service command until the wrapper regains a test subcommand.

---

## First concrete steps

1. For FR-0003, create child worktrees from `feat/FR-0003-hearth-pi-docker-cli` for `T-FR-0003-08` and `T-FR-0003-11`.
2. For FR-0002, either finish `T-FR-0002-01` server-first VAL or merge/validate `T-FR-0002-02` from its feature branch, depending on operator priority.
3. Run TEST → DEV → VAL per each ticket's owning `tickets.md`.
4. Validate FR-0003 in Docker with `docker compose -f deploy/compose/docker-compose.yml --profile test run --rm hearth-test`; use the FR-0002 feature's documented stack validation for FR-0002 streams.
5. After FR-0003 `T-FR-0003-08` and `T-FR-0003-11` are VAL-done, identify `T-FR-0003-12` as the final FR-0003 capstone ticket.

---

## Related files

- `tasks/ticket-progress.md`
- `tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`
- `tasks/feature-history/FR-0002-iphone-pwa-prototype/tickets.md`
- `tasks/feature-history/TICKET-SOURCES.md`
- `docs/design/tickets-initial.md`
