# Parallel frontier — 2026-05-20

## Queue snapshot

**Completed this session:**
- T-FR-0001-03 (Tinder loader + manifest schema) — [PR #23](https://github.com/mcelhennyi/hearth/pull/23)
- T-FR-0001-06 (Spark v1 broker + client libs) — [PR #24](https://github.com/mcelhennyi/hearth/pull/24)
- T-FR-0001-09 (Auth, VAPID, Web Push + ntfy) — [PR #25](https://github.com/mcelhennyi/hearth/pull/25)

All three merged into `feat/FR-0001-hearth-platform`; 181 tests green via Docker.

**Done tickets (dep-check inputs):** T-FR-0001-01, 02, 03, 04, 06, 09; T-FR-0004-01; all FR-0000/0002/0003 tickets.

---

## Parallel-capable tickets

| Ticket | Title | FR | Deps | Status | Worktree path | Branch |
|--------|-------|-----|------|--------|--------------|--------|
| **T-FR-0001-05** | Caddy generation and local TLS | FR-0001 | T01 ✓ T03 ✓ T04 ✓ | **eligible** | `.worktrees/FR-0001-hearth-platform/T-FR-0001-05-caddy-gen/` | `feat/FR-0001-hearth-platform-T-FR-0001-05-caddy-gen` |
| **T-FR-0001-07** | Kindling repo and CLI | FR-0001 | T03 ✓ T04 ✓ T06 ✓ | **eligible** | `.worktrees/FR-0001-hearth-platform/T-FR-0001-07-kindling-repo/` | `feat/FR-0001-hearth-platform-T-FR-0001-07-kindling-repo` |
| **T-FR-0004-02** | Built-in hearth-users plugin scaffold | FR-0004 | T-FR-0004-01 ✓ | **eligible-if-activated** — gate met (T-FR-0001-04 VAL done); requires setting FR-0004 to `in-progress` in `REGISTRY.md` first | `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-02-users-scaffold/` | `feat/FR-0004-centralized-users-auth-T-FR-0004-02-users-scaffold` |

---

## Blocked tickets (examples)

| Ticket | Blocked by |
|--------|------------|
| T-FR-0001-08 (groceries reference plugin) | T-FR-0001-07 |
| T-FR-0001-10 (Pi/Mac install + backup) | T-FR-0001-05, T-FR-0001-08 |
| T-FR-0004-03 … T-FR-0004-10 | T-FR-0004-02, then serial chain |

---

## Process note

- **T-FR-0001-05 and T-FR-0001-07** are safe to run in parallel — no shared files under edit.
- **T-FR-0001-07** creates a new external repo (`kindling`). Its worktree path above is for the Hearth-side ticket work; the Kindling repo itself should be scaffolded at `~/projects/kindling/` (or equivalent) using `.skeleton/` per the ticket notes. **Register the new repo in `registry/projects.md` in the projects root** after creation.
- **T-FR-0004-02**: Before staffing this ticket, update `REGISTRY.md` to set FR-0004 status to `in-progress` and push to `main`. Also create the feature integration worktree at `.worktrees/FR-0004-centralized-users-auth/feature/` on branch `feat/FR-0004-centralized-users-auth`. Note: T-FR-0004-01 design amendments are done in the feature tree but may not yet be promoted to `docs/design/` on `main` — verify before starting T04-02.

---

## Cross-cutting notes

- **T-FR-0001-05 (Caddy gen):** The renderer tests require Caddy in the Compose stack. The integration test path ("spin up real Caddy, install stub plugin, curl `/groceries-stub/health`") needs the `caddy` service in `docker-compose.yml`. Verify this service exists before DEV phase; if not, add it first.
- **T-FR-0001-07 (Kindling):** This ticket migrates code out of `apps/hub/api/spark/client.py`, `apps/hub/web/src/mantle/`, and `apps/hub/api/tinder/schema.py`. After completion, those paths in Hearth become thin wrappers or removed. Coordinate with any in-flight PRs that touch those paths.
- **Docker testing mandate:** All pytest runs must use `docker compose -f deploy/compose/docker-compose.yml run --rm hearth-test`. No host-local pytest.

---

## Next steps

1. `/develop-frontier` with T-FR-0001-05 and T-FR-0001-07 as the parallel batch.
2. If activating FR-0004: update `REGISTRY.md`, push, then add T-FR-0004-02 to the batch.
3. After T-FR-0001-07 completes, next wave is T-FR-0001-08 (groceries plugin, external repo).
4. After T-FR-0001-05 + T-FR-0001-08 complete, T-FR-0001-10 (install + backup) becomes eligible — that is the feature-complete gate for FR-0001.
