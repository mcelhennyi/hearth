# FR-0004 — T-FR-0004-03 users session verify

Branch: `feat/FR-0004-centralized-users-auth-T-FR-0004-03-users-session-verify`

Worktree: `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-03-users-session-verify/`

Status: TEST, DEV, and VAL complete for `T-FR-0004-03` on 2026-05-26. Ticket PR opened: https://github.com/mcelhennyi/hearth/pull/48.

Completed context:

- `T-FR-0004-01` — centralized auth design amendments.
- `T-FR-0004-02` — built-in `hearth-users` scaffold, first-boot registration, uninstall guard, and dev route.

TEST result:

- Added plugin pytest for first-run password setup, login/logout, session expiry, lockout, and verify 200/401 claims.
- `./develop test tests/builtin/test_hearth_users.py` currently fails before implementation (`2 passed, 8 errors`) because auth/session symbols and endpoints are absent.

DEV result:

- Implemented plugin-owned `users.sqlite` under `HEARTH_USERS_DATA_DIR` or `HEARTH_VAR_DIR/plugins/hearth-users`.
- Added Argon2id password setup, opaque server-side sessions, secure `hearth_session` cookie, login/logout, `/api/session`, and `/api/verify` claims.
- `./develop test tests/builtin/test_hearth_users.py` — 10 passed.

VAL result:

- `./develop test` — 251 passed, 3 skipped, 1 warning.
- `./develop test tests/builtin/test_hearth_users.py::test_login_sets_session_cookie_and_session_returns_claims tests/builtin/test_hearth_users.py::test_verify_returns_claims_with_valid_session` — 2 passed.
- `./develop test tests/builtin/test_hearth_users.py` — 10 passed after routing all plugin tests through a temp data dir.
- Updated `tasks/ticket-progress.md` and `docs/design/tickets-initial.md` for T-FR-0004-03 only.

Current phase:

- Complete; branch pushed and PR #48 is open against `feat/FR-0004-centralized-users-auth`.

Next action:

- After PR, the feature branch owner can merge T03 and identify the next eligible FR-0004 wave.
