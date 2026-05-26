# FR-0004 / T-FR-0004-02 — hearth-users scaffold

Branch: `feat/FR-0004-centralized-users-auth-T-FR-0004-02-hearth-users-scaffold`

Worktree: `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-02-hearth-users-scaffold/`

Feature base: merged `origin/feat/FR-0004-centralized-users-auth` at `5f461e4` (includes `.skeleton` `5a007a8` and the downstream compliance changelog rule in `docs/ai-context.md`).

Phase: VAL complete; ready to commit.

Scope:

- Add the built-in `apps/builtin/hearth-users/` scaffold.
- Validate `[plugin].builtin = true` in Tinder.
- Register `hearth-users` as a built-in on first hub boot.
- Keep built-ins from normal uninstall.
- Make dev Compose expose `/hearth-users/` where feasible.

TEST:

- Added RED tests for the hearth-users Tinder manifest, built-in registration, uninstall guard, and `/health` plus placeholder UI.
- Initial targeted `./develop test tests/tinder/test_loader.py::TestValidManifest::test_hearth_users_builtin_manifest_loads tests/api/test_builtins.py tests/builtin/test_hearth_users.py` failed at collection because `app.builtins` was not implemented yet.

DEV:

- Added `apps/builtin/hearth-users/` with a FastAPI `create_app`, `GET /health`, and Vite placeholder login UI.
- Added `[plugin].builtin = true` schema support, registry storage, first-boot built-in registration, and uninstall protection.
- Added dev Compose/Caddy wiring for `/hearth-users/`.
- Targeted tests pass: 5 passed via `./develop test`.

Next:

- Commit and push this ticket branch.
- Open a ticket PR against `feat/FR-0004-centralized-users-auth` if GitHub auth/network allows it.

VAL:

- Merged `origin/feat/FR-0004-centralized-users-auth` at `5f461e4`; conflict was limited to `CURRENT.md`.
- `./develop test tests/tinder/test_loader.py::TestValidManifest::test_hearth_users_builtin_manifest_loads tests/api/test_builtins.py tests/builtin/test_hearth_users.py` passes: 5 tests.
- `./develop test` passes: 243 passed, 3 skipped.
- Dev Compose smoke passes through Caddy:
  - `https://hearth.home.arpa/hearth-users/` returns HTTP 200 placeholder login HTML.
  - `https://hearth.home.arpa/hearth-users/health` returns HTTP 200 `{"ok":true,"service":"hearth-users"}`.
