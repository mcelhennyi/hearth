# FR-0004 — centralized users auth

Branch: `feat/FR-0004-centralized-users-auth`

Worktree: `.worktrees/FR-0004-centralized-users-auth/feature/`

Status: `T-FR-0004-02`, `T-FR-0004-03`, `T-FR-0004-04`, and `T-FR-0004-06` are merged into the feature branch.

Latest validation before merging T04:

- T06 targeted frontier tests — 9 passed.
- `./develop test` — 257 passed, 3 skipped, 1 warning.

T04 worker validation before integration:

- Focused merged slice — 75 passed.
- `./develop test` — 266 passed, 3 skipped.
- Caddy sidecar `/api/auth/verify` probe returned 401 without session and 200 with signed `X-Hearth-User-*` headers after login.

Completed:

- `T-FR-0004-01` — design amendments and 2026-05-26 audit.
- `T-FR-0004-02` — built-in `hearth-users` scaffold, built-in registry support, Tinder `builtin` schema, uninstall guard, dev Caddy/Compose route, tests.
- `T-FR-0004-03` — `hearth-users` password setup, Argon2id storage, login/logout, session cookie, session API, verify claims, tests.
- `T-FR-0004-04` — hub `/api/auth/verify`, auth provider settings, signed `X-Hearth-User-*` headers, fail-closed provider behavior, persisted signing secret, plugin Compose secret injection.
- `T-FR-0004-06` — Spark `session.current`, session capability/events, auth/session audit JSONL, and builtin disable guard.

Next frontier:

- `T-FR-0004-05` — Caddy auth_request and header injection.
- `T-FR-0004-07` — Kindling template: trust middleware and no local login.
- `T-FR-0004-09` — External auth provider stub and operator settings UI.
