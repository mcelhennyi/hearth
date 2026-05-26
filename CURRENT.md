# FR-0004 — centralized users auth

Branch: `feat/FR-0004-centralized-users-auth-T-FR-0004-09-external-auth-settings`

Worktree: `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-09-external-auth-settings/`

Status: `T-FR-0004-09` reached VAL locally. This branch adds the operator settings UI for `auth.provider`, records external verify URL toggles, forwards hub verify to external providers through the existing contract, and fails closed when the builtin provider is disabled.

Current ticket branch:

- `T-FR-0004-09` — External auth provider stub and operator settings UI.

Completed:

- `T-FR-0004-01` — design amendments and 2026-05-26 audit.
- `T-FR-0004-02` — built-in `hearth-users` scaffold, built-in registry support, Tinder `builtin` schema, uninstall guard, dev Caddy/Compose route, tests.
- `T-FR-0004-03` — `hearth-users` password setup, Argon2id storage, login/logout, session cookie, session API, verify claims, tests.
- `T-FR-0004-04` — hub `/api/auth/verify`, auth provider settings, signed `X-Hearth-User-*` headers, fail-closed provider behavior, persisted signing secret, plugin Compose secret injection.
- `T-FR-0004-05` — Caddy route protection, forward-auth through hub `/api/auth/verify`, verified `X-Hearth-User-*` injection, HTML redirect to `/hearth-users/login`, API 401 preservation.
- `T-FR-0004-06` — Spark `session.current`, session capability/events, auth/session audit JSONL, and builtin disable guard.
- `T-FR-0004-07` — Kindling Python template trust middleware, protected-route sample, no-local-login README/useUser guidance, and dense child-repo compliance changelog.
- `T-FR-0004-09` — hub builtin-disabled fail-closed verify behavior, Settings route/provider form, external verify URL save flow, and custom user service follow-up note.

Latest T-FR-0004-09 validation:

- `./develop test tests/api/test_auth_verify_alias.py tests/api/test_settings.py` — 13 passed, 3 warnings.
- `./develop test` — 276 passed, 3 skipped, 3 warnings.
- `./develop web npm run test` — 4 files passed, 9 tests passed.
- `./develop web npm run build` — production build passed.
- `./develop web npm run lint` — blocked by pre-existing lint errors in `src/mantle/InstallPrompt.tsx` and `src/sw.ts`; no T09 files reported after the hook-order fix.

Next action:

- Push this branch and open a ticket PR against `feat/FR-0004-centralized-users-auth`.
