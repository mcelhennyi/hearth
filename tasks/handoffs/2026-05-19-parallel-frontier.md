# Next-step handoff — parallel frontier (2026-05-19)

**Audience:** Next agent or maintainer picking up work from `main`.
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md` (DAG), `docs/ai-context.md`.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | — (no ticket in-flight) |
| **Active phase** | — |
| **Branch / worktree** | `main` |
| **Session status** | `handoff` |
| **Next agent should** | Start **T-FR-0001-01** (repo scaffold & dev loop); run `/develop-frontier` |

**Triad-complete (summary):**
T-FR-0000-01 · T-FR-0002-01..04 · T-FR-0003-01..13 · T-FR-0004-01 — all done on `main`.

**Still incomplete (summary):**
T-FR-0001-01..10 (all `—`) · T-FR-0004-02..10 (parked, waiting on T-FR-0001-04 VAL).

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in **Deps:** has **VAL** = `done` in `tasks/ticket-progress.md`.

With all FR-0002 and FR-0003 tickets VAL-done, **one** ticket is currently eligible:

| Ticket | Title | Deps |
|--------|-------|------|
| **T-FR-0001-01** | Repo scaffold and Compose dev loop | `none` |

**One stream** is dependency-valid right now. T-FR-0001-01 is the critical-path gating ticket — until it reaches VAL done, no other FR-0001 ticket can start.

**Next batch (unlocks when T-FR-0001-01 is VAL done):**

| Ticket | Title | Deps |
|--------|-------|------|
| T-FR-0001-02 | Hub API skeleton and SQLite registry | T-FR-0001-01 |
| T-FR-0001-04 | Mantle PWA shell and iframe embed | T-FR-0001-01 |

These two can run **in parallel** once T01 is done.

**Examples of what stays blocked until more VAL-done rows exist:**

- T-FR-0001-05 (Caddy generation) — needs T01 + T03 + T04 all done.
- T-FR-0001-03 (Tinder loader) — needs T02 done.
- T-FR-0001-06 (Spark v1 broker) — needs T02 done.
- T-FR-0001-07 (Kindling repo & CLI) — needs T03 + T04 + T06 done.
- T-FR-0001-08 (groceries plugin) — needs T07 done.
- T-FR-0001-09 (Auth, VAPID, Web Push) — needs T02 + T04 done.
- T-FR-0001-10 (install.sh + backup) — needs T05 + T08 + T09 done.
- T-FR-0004-02..10 — parked until T-FR-0001-04 VAL done.

Full **Deps:** edges: `tasks/feature-history/FR-0001-hearth-platform/20-tickets-dag.md`; global mermaid in `docs/design/tickets-initial.md`.

---

## Process note

- **Feature branch:** `feat/FR-0001-hearth-platform` (create on first commit of T01).
- **Worktree:** `.worktrees/FR-0001-hearth-platform/T-FR-0001-01-repo-scaffold/` on branch `feat/FR-0001-hearth-platform/T-FR-0001-01-repo-scaffold`.
- **FR-0002 reuse:** T-FR-0001-04 should reuse `apps/hub/web/` from `main` (T-FR-0002-02); T-FR-0001-05 reuses Caddy TLS stack (T-FR-0002-01); T-FR-0001-09 reuses VAPID/Web Push (T-FR-0002-03).
- **Integration checkout:** `main` (or the feature branch after T01 lands) coordinates merges; individual ticket branches merge into `feat/FR-0001-hearth-platform` per §2d.

---

## Cross-cutting items

- REWORK-REQUIRED **RW-D1** still open: `10-design/deployment.md` links nginx wording; retire when Caddy-first wording is consistent (addressable in T-FR-0001-05 or T-FR-0001-10).
- FR-0004 unblocks after **T-FR-0001-04 VAL** — set REGISTRY.md row to `in-progress` and queue T-FR-0004-02 at that point.
- Stack pin: Python 3.12, Node 20 LTS, Caddy 2.8, pnpm workspace (per T-FR-0001-01 notes).

---

## Concrete next steps

1. **Run `/develop-frontier`** — T-FR-0001-01 is the sole eligible ticket; one subagent, one child worktree.
2. After T01 VAL done: re-run `/identify-frontier` to confirm T02 ‖ T04 are the next wave.
3. Run `/develop-frontier` on T02 ‖ T04 in parallel.
4. Continue down the DAG per `20-tickets-dag.md` frontier batches.

---

## Related files

- [`tasks/feature-history/FR-0001-hearth-platform/tickets.md`](../feature-history/FR-0001-hearth-platform/tickets.md)
- [`tasks/feature-history/FR-0001-hearth-platform/20-tickets-dag.md`](../feature-history/FR-0001-hearth-platform/20-tickets-dag.md)
- [`tasks/ticket-progress.md`](../ticket-progress.md)
- [`docs/design/tickets-initial.md`](../../docs/design/tickets-initial.md)
- [`tasks/feature-history/REGISTRY.md`](../feature-history/REGISTRY.md)
