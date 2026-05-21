# Next-step handoff — parallel frontier (2026-05-19, wave 3)

**Audience:** Next agent or maintainer picking up work on `feat/FR-0001-hearth-platform`.
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md` (DAG), `docs/ai-context.md`.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | — (T02 + T04 done; next wave ready) |
| **Active phase** | — |
| **Branch / worktree** | `feat/FR-0001-hearth-platform` |
| **Session status** | `handoff` |
| **Next agent should** | Run `/develop-frontier` on T03 ‖ T06 ‖ T09 |

**Triad-complete (summary):**
T-FR-0000-01 · T-FR-0002-01..04 · T-FR-0003-01..13 · T-FR-0004-01 · **T-FR-0001-01..02 · T-FR-0001-04** — all done.

**Still incomplete in FR-0001:**
T-FR-0001-03, 05, 06, 07, 08, 09, 10 — all parked.

---

## Eligible ∩ incomplete (this wave)

| Ticket | Title | Deps | Branch | Worktree |
|--------|-------|------|--------|----------|
| **T-FR-0001-03** | Tinder loader and manifest schema | T02 ✓ | `feat/FR-0001-hearth-platform-T-FR-0001-03-tinder-loader` | `.worktrees/FR-0001-hearth-platform/T-FR-0001-03-tinder-loader/` |
| **T-FR-0001-06** | Spark v1 broker and client libs | T02 ✓ | `feat/FR-0001-hearth-platform-T-FR-0001-06-spark-broker` | `.worktrees/FR-0001-hearth-platform/T-FR-0001-06-spark-broker/` |
| **T-FR-0001-09** | Auth, VAPID, Web Push + ntfy | T02 ✓, T04 ✓ | `feat/FR-0001-hearth-platform-T-FR-0001-09-auth-vapid-push` | `.worktrees/FR-0001-hearth-platform/T-FR-0001-09-auth-vapid-push/` |

---

## Blocked (next waves)

| Ticket | Blocked on |
|--------|-----------|
| T-FR-0001-05 | T03 |
| T-FR-0001-07 | T03, T06 |
| T-FR-0001-08 | T07 |
| T-FR-0001-10 | T05, T08, T09 |
| T-FR-0004-02..10 | T-FR-0001-04 VAL ✓ — **FR-0004 unblocked!** (set REGISTRY.md to `in-progress` when staffing T-FR-0004-02) |

---

## Process notes (established in previous sessions)

- **Branch naming:** ticket branches use **dashes** throughout — `feat/FR-0001-hearth-platform-T-FR-0001-XX-short-name` (slash after `feat/` is fine; no additional slashes in the ticket segment, which would create ref-path conflicts).
- **ALL tests via Docker**, never on the host:
  - Python: `docker compose run --rm hearth-test` (profile `test`; entrypoint calls pytest)
  - Non-pytest shell in `hearth-test`: `docker compose run --rm --entrypoint sh hearth-test -c "..."`
  - JS: `docker compose run --rm --profile tooling web`; pnpm not pre-installed → run `npm install -g pnpm@9` first
- **Feature integration branch:** `feat/FR-0001-hearth-platform` at `.worktrees/FR-0001-hearth-platform/feature/`.
- Each ticket PR bases on `feat/FR-0001-hearth-platform`; the feature → `main` PR opens only after the §2d gate (all 10 tickets done).

---

## Cross-cutting notes

- **T-FR-0001-09** should reuse the existing `apps/hub/api/app/push_service.py` and `push_store.py` already on the feature branch (ported from FR-0002).
- **T-FR-0001-03** spec lives in `docs/design/plugin-contract.md` — read before writing Pydantic tinder.toml models; escalate `DESIGN-FLAW` if spec and needed code diverge.
- **T-FR-0001-06** introduces a Unix-socket broker at `var/hearth/run/spark.sock`; see `docs/design/spark-api.md`. No file-contention with T03 or T09.
- **FR-0004** is now unblocked (T-FR-0001-04 VAL is done) — when staffing T-FR-0004-02, update `REGISTRY.md` FR-0004 row from `parked` to `in-progress` and push immediately per §2b deconfliction rule.

---

## Concrete next steps

1. **Run `/develop-frontier`** — T03 ‖ T06 ‖ T09 in parallel, one subagent each.
2. After all three reach VAL done: re-run `/identify-frontier` to confirm T05, T07 become the next wave.
3. Optionally staff T-FR-0004-02 in parallel once FR-0004 `in-progress` is confirmed.

---

## Related files

- [`tasks/feature-history/FR-0001-hearth-platform/tickets.md`](../feature-history/FR-0001-hearth-platform/tickets.md)
- [`tasks/ticket-progress.md`](../ticket-progress.md)
- [`docs/design/tickets-initial.md`](../../docs/design/tickets-initial.md)
- [`tasks/feature-history/REGISTRY.md`](../feature-history/REGISTRY.md)
