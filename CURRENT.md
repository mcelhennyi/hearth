# FR-0004 — centralized users auth

Branch: `feat/FR-0004-centralized-users-auth`

Worktree: `.worktrees/FR-0004-centralized-users-auth/feature/`

Status: `T-FR-0004-05` TEST, DEV, and VAL are complete. Starting feature branch includes `T-FR-0004-02`, `T-FR-0004-03`, `T-FR-0004-04`, and `T-FR-0004-06`.

Current ticket branch:

- `T-FR-0004-05` — Caddy auth_request and header injection.
- Phase: VAL complete on 2026-05-26.
- Scope guard: proxy/Caddy generation only; no Kindling trust middleware, Mantle shell login/useUser, or external auth settings UI.

T-FR-0004-05 TEST:

- Added focused golden tests for hub and install Caddy fragments.
- Red run: `./develop test tests/proxy/test_caddy.py tests/test_plugin_compose_generation.py` failed on the legacy direct-proxy fragments, as expected.

Latest validation after merging T04:

- Focused merged slice — 75 passed.
- `./develop test` — 266 passed, 3 skipped, 3 warnings.
- Caddy sidecar `/api/auth/verify` probe returned 401 without session and 200 with signed `X-Hearth-User-*` headers after login.

Completed:

- `T-FR-0004-01` — design amendments and 2026-05-26 audit.
- `T-FR-0004-02` — built-in `hearth-users` scaffold, built-in registry support, Tinder `builtin` schema, uninstall guard, dev Caddy/Compose route, tests.
- `T-FR-0004-03` — `hearth-users` password setup, Argon2id storage, login/logout, session cookie, session API, verify claims, tests.
- `T-FR-0004-04` — hub `/api/auth/verify`, auth provider settings, signed `X-Hearth-User-*` headers, fail-closed provider behavior, persisted signing secret, plugin Compose secret injection.
- `T-FR-0004-06` — Spark `session.current`, session capability/events, auth/session audit JSONL, and builtin disable guard.

VAL result:

- `./develop test tests/proxy/test_caddy.py tests/test_plugin_compose_generation.py` — 15 passed, 1 skipped.
- `./develop test` — 269 passed, 3 skipped, 3 warnings.

Next action:

- Commit, push, and open a ticket PR against `feat/FR-0004-centralized-users-auth`.
