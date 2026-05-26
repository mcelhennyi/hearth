# FR-0004 — T-FR-0004-06 Spark session and builtin registry

Branch: `feat/FR-0004-centralized-users-auth-T-FR-0004-06-spark-session-builtin-rules`

Worktree: `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-06-spark-session-builtin-rules/`

Status: VAL complete for `T-FR-0004-06`; pushed and PR opened.

Scope:

- Add/verify Spark `session.current` for the built-in `hearth-users` provider.
- Add login/logout event contracts where supported by the current Spark broker.
- Harden built-in registry rules for skip/uninstall rejection; document or stub provider-disable policy if it belongs to T04.
- Add audit log entries for auth/session events where the existing audit model supports it.

Recent context:

- `T-FR-0004-02` and `T-FR-0004-03` are merged into the starting feature branch.
- Avoid implementing hub `/api/auth/verify` provider settings; that remains `T-FR-0004-04`.

Latest TEST:

- `./develop test tests/tinder/test_loader.py::TestValidManifest::test_hearth_users_builtin_manifest_loads tests/api/test_builtins.py tests/spark/test_broker.py::test_local_session_current_handler_for_hearth_users tests/spark/test_broker.py::test_local_session_current_handler_enforces_call_permissions tests/builtin/test_hearth_users.py::test_spark_session_current_returns_claims_for_session_token tests/builtin/test_hearth_users.py::test_spark_session_current_returns_unauthenticated_without_session tests/builtin/test_hearth_users.py::test_login_and_logout_write_session_audit_events` — expected failures: missing session capability manifest, builtin disable guard, broker local method registry, users `session.current`, and auth/session audit JSONL.

Latest DEV:

- Same targeted command — 9 passed.
- Implemented `hearth-users` Tinder `session.current` plus login/logout event contract.
- Added Spark broker local method registration with permission checks and audit records.
- Added users plugin `spark_session_current` and auth/session JSONL audit entries.
- Rejected disabling built-in plugins until T04 external-provider settings can prove a healthy alternate provider.

Latest VAL:

- `./develop test` — 257 passed, 3 skipped, 1 warning.
- Updated `tasks/ticket-progress.md` for `T-FR-0004-06` only.
- Updated `docs/design/tickets-initial.md` `triadDone` for `T-FR-0004-06`.

Commit:

- `788889f` — `feat(auth): add Spark session builtin rules`.

PR:

- https://github.com/mcelhennyi/hearth/pull/49

Next:

- Integration owner should review and merge PR #49 into `feat/FR-0004-centralized-users-auth` with the parallel T04 stream.
