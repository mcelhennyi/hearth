# FR-0004 — centralized users auth

Branch: `feat/FR-0004-centralized-users-auth`

Worktree: `.worktrees/FR-0004-centralized-users-auth/feature/`

Status: `T-FR-0004-02`, `T-FR-0004-03`, and `T-FR-0004-06` are merged into the feature branch. `T-FR-0004-04` is still in flight in a parallel child worktree.

Latest validation:

- T06 targeted frontier tests — 9 passed.
- `./develop test` — 257 passed, 3 skipped, 1 warning.

Completed:

- `T-FR-0004-01` — design amendments and 2026-05-26 audit.
- `T-FR-0004-02` — built-in `hearth-users` scaffold, built-in registry support, Tinder `builtin` schema, uninstall guard, dev Caddy/Compose route, tests.
- `T-FR-0004-03` — `hearth-users` password setup, Argon2id storage, login/logout, session cookie, session API, verify claims, tests.
- `T-FR-0004-06` — Spark `session.current`, session capability/events, auth/session audit JSONL, and builtin disable guard.

In flight:

- `T-FR-0004-04` — Hub auth verify alias and provider settings.

Next after T04:

- `T-FR-0004-05`, `T-FR-0004-07`, and `T-FR-0004-09` become dependency-eligible once T04 is merged.
