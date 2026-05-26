# FR-0004 — centralized users auth

Branch: `feat/FR-0004-centralized-users-auth`

Worktree: `.worktrees/FR-0004-centralized-users-auth/feature/`

Status: `T-FR-0004-08` is complete on this ticket branch. Starting feature branch includes `T-FR-0004-02`, `T-FR-0004-03`, `T-FR-0004-04`, `T-FR-0004-05`, `T-FR-0004-06`, and `T-FR-0004-07`.

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
- `T-FR-0004-08` — Mantle shell fetches `/hearth-users/api/session`, unauthenticated users link to `/hearth-users/login?next=...`, plugin iframes receive verified `hearth.user` claims, and the stale hub password form is replaced by a handoff link.

Latest T-FR-0004-07 validation:

- PR #51 amd64 install smoke failed during GitHub checkout with a 403 account-suspended response before repository code ran; arm64 install smoke passed.
- Local focused VAL on the ticket branch: `./develop test tests/test_kindling_plugin_contract.py` — 13 passed.
- Local full VAL on the ticket branch: `./develop test` — 272 passed, 3 skipped, 3 warnings.
- Combined feature VAL after merge: `./develop test tests/test_kindling_plugin_contract.py` — 13 passed; `./develop test` — 275 passed, 3 skipped, 3 warnings.

Latest T-FR-0004-08 validation:

- `./develop web npm ci` — installed web dependencies in the Docker web service.
- `./develop web npm run test -- App.test.tsx` — 8 passed after RED failures for the missing session/login/user-postMessage contract.
- `./develop web npm run test` — 11 passed.
- `./develop web npm run lint` — passed.
- `./develop web npm run build` — passed.
- Manual exception: real iPhone PWA login-once walkthrough was not available in this host environment; automated contract coverage verifies the session fetch, login link, and plugin iframe `hearth.user` payload.

Next action:

- Open and merge the `T-FR-0004-08` ticket PR into `feat/FR-0004-centralized-users-auth`.
- Continue `T-FR-0004-09`.
