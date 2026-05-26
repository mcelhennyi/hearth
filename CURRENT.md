# FR-0004 — centralized users auth

Branch: `feat/FR-0004-centralized-users-auth`

Worktree: `.worktrees/FR-0004-centralized-users-auth/feature/`

Status: `T-FR-0004-02` and `T-FR-0004-03` are merged into the feature branch. Skeleton sync is applied at `.skeleton` `5a007a8` and root `docs/ai-context.md` includes the downstream compliance changelog rule.

Latest validation:

- `./develop test tests/builtin/test_hearth_users.py` — 10 passed.
- `./develop test` — 251 passed, 3 skipped, 1 warning.

Completed:

- `T-FR-0004-01` — design amendments and 2026-05-26 audit.
- `T-FR-0004-02` — built-in `hearth-users` scaffold, built-in registry support, Tinder `builtin` schema, uninstall guard, dev Caddy/Compose route, tests.
- `T-FR-0004-03` — `hearth-users` password setup, Argon2id storage, login/logout, session cookie, session API, verify claims, tests.

Next frontier:

- `T-FR-0004-04` — Hub auth verify alias and provider settings.
- `T-FR-0004-06` — Spark session capabilities and builtin registry rules.
