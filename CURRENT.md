# FR-0004 — centralized users auth

Branch: `feat/FR-0004-centralized-users-auth`

Worktree: `.worktrees/FR-0004-centralized-users-auth/feature/`

Status: `T-FR-0004-05` is merged into the feature branch. Starting feature branch includes `T-FR-0004-02`, `T-FR-0004-03`, `T-FR-0004-04`, `T-FR-0004-05`, and `T-FR-0004-06`.

Current ticket branch:

- `T-FR-0004-07` — Kindling template trust middleware and no local login. PR #51 is open; local validation passed, but amd64 install smoke failed and needs repair before merge.
- `T-FR-0004-08` — Mantle shell login via `hearth-users` and `useUser` contract. Now dependency-eligible after T05.
- `T-FR-0004-09` — External auth provider stub and operator settings UI.

Completed:

- `T-FR-0004-01` — design amendments and 2026-05-26 audit.
- `T-FR-0004-02` — built-in `hearth-users` scaffold, built-in registry support, Tinder `builtin` schema, uninstall guard, dev Caddy/Compose route, tests.
- `T-FR-0004-03` — `hearth-users` password setup, Argon2id storage, login/logout, session cookie, session API, verify claims, tests.
- `T-FR-0004-04` — hub `/api/auth/verify`, auth provider settings, signed `X-Hearth-User-*` headers, fail-closed provider behavior, persisted signing secret, plugin Compose secret injection.
- `T-FR-0004-05` — Caddy route protection, forward-auth through hub `/api/auth/verify`, verified `X-Hearth-User-*` injection, HTML redirect to `/hearth-users/login`, API 401 preservation.
- `T-FR-0004-06` — Spark `session.current`, session capability/events, auth/session audit JSONL, and builtin disable guard.

VAL result:

- `./develop test tests/proxy/test_caddy.py tests/test_plugin_compose_generation.py` — 15 passed, 1 skipped.
- `./develop test` — 269 passed, 3 skipped, 3 warnings.

Next action:

- Repair PR #51 amd64 install smoke for `T-FR-0004-07`, then merge it into the feature branch.
- Staff `T-FR-0004-08` and `T-FR-0004-09` next.
