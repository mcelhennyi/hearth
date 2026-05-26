# FR-0004 — centralized users auth

Branch: `feat/FR-0004-centralized-users-auth-T-FR-0004-07-kindling-trust-template`

Worktree: `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-07-kindling-trust-template/`

Status: `T-FR-0004-07` TEST, DEV, and VAL are complete. The starting feature branch includes `T-FR-0004-02`, `T-FR-0004-03`, `T-FR-0004-04`, and `T-FR-0004-06`.

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

Current ticket:

- `T-FR-0004-07` — Kindling template: trust middleware and no local login.

TEST result:

- Added failing template coverage for generated `app.py`, `trust.py`, `require_hearth_user()`, auth README guidance, and `COMPLIANCE_CHANGELOG.md`.
- Focused red run: `./develop test tests/test_kindling_plugin_contract.py` → 7 failed, 6 passed.

DEV result:

- Generated Python plugins now include `trust.py` with `require_hearth_user()`, `app.py` with protected `/api/me`, README auth/no-local-login guidance, and a dense Kindling compliance changelog.
- `kindling/mantle` exports a cookie-free `useUser()` hook for plugin UI guidance.
- Focused green run: `./develop test tests/test_kindling_plugin_contract.py` → 13 passed.

VAL result:

- `./develop test tests/test_kindling_plugin_contract.py` — 13 passed.
- `./develop test` — 272 passed, 3 skipped, 3 warnings.

Next action:

- Commit, push, and open a ticket PR against `feat/FR-0004-centralized-users-auth`.
