# Next-step handoff — parallel frontier (2026-05-10)

**Audience:** Next agent or maintainer picking up work from `feat/FR-0003-hearth-pi-docker-cli` and the active FR-0002 feature line.  
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md` (DAG), `docs/ai-context.md`.  
**Context:** FR-0003 wave 6 (`T-FR-0003-08`, `T-FR-0003-11`) is merged into `feat/FR-0003-hearth-pi-docker-cli`; integrated Compose validation passed with `76 passed`.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | FR-0003 wave 6 integrated; `T-FR-0003-12` is now dependency-eligible. |
| **Active phase** | `handoff` — wave 6 merged; integrated Compose test suite passed (`76 passed`). |
| **Branch / worktree** | FR-0003 feature: `.worktrees/FR-0003-hearth-pi-docker-cli/feature/` → `feat/FR-0003-hearth-pi-docker-cli`. |
| **Session status** | `handoff` |
| **Next agent should** | Start `T-FR-0003-12` from the FR-0003 feature branch, or continue FR-0002 `T-FR-0002-01` VAL / `T-FR-0002-02` if the prototype line is priority. |

**Triad-complete (summary):** `T-FR-0000-01`; FR-0003 `T-FR-0003-01`, `-02`, `-03`, `-04`, `-05`, `-06`, `-07`, `-08`, `-09`, `-10`, `-11`, `-13`.

**Still incomplete (summary):** FR-0003 `T-FR-0003-12`; FR-0002 `T-FR-0002-01` VAL, `T-FR-0002-02`, `-03`, `-04`; FR-0001 remains parked by policy.

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in `Deps:` has `VAL` = `done` in `tasks/ticket-progress.md`.

With FR-0003 `T-FR-0003-03`, `-06`, `-08`, `-09`, and `-11` VAL-done, and with FR-0002 `T-FR-0002-01` / `T-FR-0002-02` both having `Deps: none`, these tickets are eligible and incomplete:

| Ticket | FR | Title | Deps |
|--------|----|-------|------|
| `T-FR-0002-01` | FR-0002 | Caddy + `tls internal` + static placeholder | `none` |
| `T-FR-0002-02` | FR-0002 | Mantle PWA bones | `none` |
| `T-FR-0003-12` | FR-0003 | Smoke tests + ARM CI for install path | `T-FR-0003-03`, `T-FR-0003-06`, `T-FR-0003-08`, `T-FR-0003-09`, `T-FR-0003-11` |

So **three implementation streams** are dependency-valid now across the active graph:

- `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls` under `.worktrees/FR-0002-iphone-pwa-prototype/`
- `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones` under `.worktrees/FR-0002-iphone-pwa-prototype/`
- `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-12-install-smoke-arm-ci` under `.worktrees/FR-0003-hearth-pi-docker-cli/`

**Policy-excluded despite graph eligibility:** `T-FR-0001-01` has `Deps: none`, but FR-0001 is parked until FR-0002 closes or registry policy changes.

**Examples of what stays blocked until more VAL-done rows exist:**

- `T-FR-0002-03` — needs `T-FR-0002-01` and `T-FR-0002-02` VAL-done.
- `T-FR-0002-04` — needs `T-FR-0002-01`, `T-FR-0002-02`, and `T-FR-0002-03` VAL-done.
- FR-0001 tickets remain parked by policy even where graph deps would otherwise allow work.

Full `Deps:` edges: scan all `tasks/feature-history/**/tickets.md`; global mermaid in `docs/design/tickets-initial.md`.

---

## Process note (queue vs graph)

This handoff is based on the FR-0003 feature branch, not `main`. `main` may still lag until the feature PR is refreshed and reviewed. For FR-0003 ticket streams, branch from `feat/FR-0003-hearth-pi-docker-cli` and merge ticket PRs back into that feature branch first.

The global graph mixes FR-0002 and FR-0003 in this frontier, which is expected under `docs/ai-context.md` §2c. Keep FR-0002 streams under the FR-0002 feature worktree and FR-0003 streams under the FR-0003 feature worktree.

---

## Cross-cutting work (parallel to tickets)

- Keep `CURRENT.md` on `feat/FR-0003-hearth-pi-docker-cli` aligned as `T-FR-0003-12` lands.
- When `T-FR-0003-12` reaches VAL, update only that ticket's progress row and union the corresponding `triadDone` line in `docs/design/tickets-initial.md`.
- FR-0003 validation should use the explicit Compose test service command: `docker compose -f deploy/compose/docker-compose.yml --profile test run --rm hearth-test`.

---

## First concrete steps

1. For FR-0003, create child worktree `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-12-install-smoke-arm-ci/` from `feat/FR-0003-hearth-pi-docker-cli`.
2. Run TEST → DEV → VAL for `T-FR-0003-12` per `tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`.
3. Validate in Docker with `docker compose -f deploy/compose/docker-compose.yml --profile test run --rm hearth-test`; document any ARM/Pi manual validation gap in the diary.
4. For FR-0002, continue `T-FR-0002-01` server-first VAL or `T-FR-0002-02` integration depending on operator priority.
5. After `T-FR-0003-12` is VAL-done, FR-0003 ticket implementation is complete and should move toward feature closeout / PR refresh.

---

## Related files

- `tasks/ticket-progress.md`
- `tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`
- `tasks/feature-history/FR-0002-iphone-pwa-prototype/tickets.md`
- `tasks/feature-history/TICKET-SOURCES.md`
- `docs/design/tickets-initial.md`
