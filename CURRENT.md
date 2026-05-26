# FR-0004 — centralized users auth

Branch: `feat/FR-0004-centralized-users-auth`

Worktree: `.worktrees/FR-0004-centralized-users-auth/feature/`

Status: finish-feature closeout is superseded by the multi-user correction. [PR #56](https://github.com/mcelhennyi/hearth/pull/56) is only a feature-branch preview until `T-FR-0004-11` through `T-FR-0004-16` land. Starting feature branch includes `T-FR-0004-02` through `T-FR-0004-10`.

Current ticket branch:

- `T-FR-0004-14` — Session, Spark, gateway, and Mantle claims use real users. Worktree `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-14-real-user-claims/`, branch `feat/FR-0004-centralized-users-auth-T-FR-0004-14-real-user-claims`.
- Phase: VAL complete. TEST added cross-contract coverage for two distinct users across hub verify, Spark/session/audit, Mantle shell postMessage, `@kindling/mantle useUser()`, and Kindling-relevant trust paths. DEV fixed `@kindling/mantle` `UserInfo` to expose `roles?: string[]`.

Completed:

- `T-FR-0004-01` — design amendments and 2026-05-26 audit.
- `T-FR-0004-02` — built-in `hearth-users` scaffold, built-in registry support, Tinder `builtin` schema, uninstall guard, dev Caddy/Compose route, tests.
- `T-FR-0004-03` — `hearth-users` password setup, Argon2id storage, login/logout, session cookie, session API, verify claims, tests.
- `T-FR-0004-04` — hub `/api/auth/verify`, auth provider settings, signed `X-Hearth-User-*` headers, fail-closed provider behavior, persisted signing secret, plugin Compose secret injection.
- `T-FR-0004-05` — Caddy route protection, forward-auth through hub `/api/auth/verify`, verified `X-Hearth-User-*` injection, HTML redirect to `/hearth-users/login`, API 401 preservation.
- `T-FR-0004-06` — Spark `session.current`, session capability/events, auth/session audit JSONL, and builtin disable guard.
- `T-FR-0004-07` — Kindling Python template trust middleware, protected-route sample, no-local-login README/useUser guidance, and dense child-repo compliance changelog.
- `T-FR-0004-08` — Mantle shell fetches `/hearth-users/api/session`, unauthenticated users link to `/hearth-users/login?next=...`, plugin iframes receive verified `hearth.user` claims, and the stale hub password form is replaced by a handoff link.
- `T-FR-0004-09` — hub builtin-disabled fail-closed verify behavior, Settings route/provider form, external verify URL save flow, and custom user service follow-up note.
- `T-FR-0004-10` — capstone gateway identity contract: hub verify signs identity for the public plugin URI, Caddy passes original method/URI to plugins, and a generated Kindling plugin rejects direct calls but accepts verified gateway headers.
- `T-FR-0004-11` — multi-user design/migration amendment: account schema, first-admin setup semantics, migration from the old local account, final-admin safety, classified single-user statements, and global DAG exposure for T12-T16.
- `T-FR-0004-12` — users plugin multi-user implementation: SQLite migration from the old `local` row, opaque first-admin ids for new setup, username/password login, stored user claims in sessions/verify/Spark/audit, disabled-user fail-closed checks, and bootstrap password file compatibility as `local` / `Local user` admin.

Latest T-FR-0004-08 validation:

- `./develop web npm ci` — installed web dependencies in the Docker web service.
- `./develop web npm run test -- App.test.tsx` — 8 passed after RED failures for the missing session/login/user-postMessage contract.
- `./develop web npm run test` — 11 passed.
- `./develop web npm run lint` — passed.
- `./develop web npm run build` — passed.
- Manual exception: real iPhone PWA login-once walkthrough was not available in this host environment; automated contract coverage verifies the session fetch, login link, and plugin iframe `hearth.user` payload.

Latest T-FR-0004-09 validation:

- `./develop test tests/api/test_auth_verify_alias.py tests/api/test_settings.py` — 13 passed, 3 warnings.
- `./develop test` — 276 passed, 3 skipped, 3 warnings.
- `./develop web npm run test` — 4 files passed, 9 tests passed.
- `./develop web npm run build` — production build passed.
- `./develop web npm run lint` — blocked by pre-existing lint errors in `src/mantle/InstallPrompt.tsx` and `src/sw.ts`; no T09 files reported after the hook-order fix.

Combined T-FR-0004-08/T-FR-0004-09 feature validation:

- `./develop web npm ci` — installed dependencies.
- `./develop web npm run test -- App.test.tsx` — 9 passed.
- `./develop test tests/api/test_auth_verify_alias.py tests/api/test_settings.py` — 13 passed, 3 warnings.
- `./develop web npm run test` — 4 files passed, 12 tests passed.
- `./develop test` — 276 passed, 3 skipped, 3 warnings.
- `./develop web npm run build` — passed.
- `./develop web npm run lint` — passed.

Latest T-FR-0004-10 validation:

- `./develop test tests/api/test_gateway_identity_contract.py tests/proxy/test_caddy.py tests/test_plugin_compose_generation.py` — 16 passed, 1 skipped, 2 warnings.
- `./develop test` — 277 passed, 3 skipped, 4 warnings.
- `./develop web npm ci` — installed dependencies.
- `./develop web npm run test` — 4 files passed, 12 tests passed.
- `./develop web npm run build` — passed.
- `./develop web npm run lint` — passed.

Combined feature validation after T10 merge:

- `./develop test` — 277 passed, 3 skipped, 4 warnings.
- `./develop web npm run test` — 4 files passed, 12 tests passed.
- `./develop web npm run build` — passed.
- `./develop web npm run lint` — passed.

Latest T-FR-0004-11 validation:

- `rg -n "single local user|One local user|MVP: single" docs/design tasks/feature-history/FR-0004-centralized-users-auth` — no matches after replacing the ticket wording.
- `rg -n -i "single-user|single user|local user password|One local user|MVP: single|single local user" docs/design tasks/feature-history/FR-0004-centralized-users-auth` — remaining hits are classified in `10-design-01-gateway-and-trust.md` as updated, intentionally deferred, ticketed, or historical diary text.
- `git diff --check` — passed.

Next action:

- Push `feat/FR-0004-centralized-users-auth-T-FR-0004-14-real-user-claims` and open a PR targeting `feat/FR-0004-centralized-users-auth`. Do not merge or alter the parallel `T-FR-0004-13` stream.

Latest T-FR-0004-12 validation:

- Rebasing note: ticket branch was rebased onto refreshed `origin/feat/FR-0004-centralized-users-auth` at `e3a7dc9` after `main` was merged into the feature branch.
- RED phase: `./develop test tests/builtin/test_hearth_users.py` failed against the old single-user implementation with 12 expected failures covering setup, migration, username login, disabled users, lockout, and stored claims.
- `./develop test tests/builtin/test_hearth_users.py` — 23 passed.
- `./develop test tests/builtin/test_hearth_users.py tests/spark/test_broker.py tests/api/test_auth_verify_alias.py` — 55 passed, 2 warnings.
- `git diff --check` — passed.

Latest T-FR-0004-14 validation:

- RED: `./develop web sh -lc 'corepack enable && cd /workspace && corepack pnpm --filter @kindling/mantle test'` failed before DEV because `UserInfo` did not expose `roles?: string[]`.
- `./develop test tests/builtin/test_hearth_users.py tests/api/test_auth_verify_alias.py tests/api/test_gateway_identity_contract.py tests/test_kindling_plugin_contract.py tests/spark/test_broker.py tests/proxy/test_caddy.py` — 83 passed, 1 skipped, 8 warnings.
- `./develop web npm run test -- App.test.tsx` — 9 passed.
- `./develop web sh -lc 'corepack enable && cd /workspace && corepack pnpm --filter @kindling/mantle test'` — 38 passed.
- `./develop web npm run test` — 64 passed.
- `./develop web npm run build` — passed.
- `./develop web npx eslint src/App.test.tsx` — passed.
- `git diff --check` — passed.
- `./develop web npm run lint` — blocked by pre-existing non-T14 lint errors in dashboard/edit, shell chrome/frame hooks, SettingsContext, and ThemeProvider.
