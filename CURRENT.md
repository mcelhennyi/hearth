# FR-0004 — centralized users auth

Branch: `feat/FR-0004-centralized-users-auth`

Worktree: `.worktrees/FR-0004-centralized-users-auth/feature/`

Status: `T-FR-0004-02` is merged into the feature branch. Skeleton sync is applied at `.skeleton` `5a007a8` and root `docs/ai-context.md` includes the downstream compliance changelog rule.

Latest validation:

- `./develop test tests/tinder/test_loader.py::TestValidManifest::test_hearth_users_builtin_manifest_loads tests/api/test_builtins.py tests/builtin/test_hearth_users.py` — 5 passed.
- `./develop test` — 243 passed, 3 skipped, 1 warning.

Completed:

- `T-FR-0004-01` — design amendments and 2026-05-26 audit.
- `T-FR-0004-02` — built-in `hearth-users` scaffold, built-in registry support, Tinder `builtin` schema, uninstall guard, dev Caddy/Compose route, tests.

Next frontier:

- `T-FR-0004-03` — Users plugin: password, session, verify API.
- Ticket branch suggestion: `feat/FR-0004-centralized-users-auth-T-FR-0004-03-users-session-verify`.
- Ticket worktree suggestion: `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-03-users-session-verify/`.
