# Ticket progress

## Current focus

| Field | Value |
|-------|--------|
| **Active ticket** | `T-FR-0004-11` Multi-user design amendment and migration plan |
| **Active phase** | TEST → DEV → VAL |
| **Branch / worktree** | `feat/FR-0004-centralized-users-auth-T-FR-0004-11-multi-user-design` at `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-11-multi-user-design/` |
| **Session status** | `developing` |
| **Next agent should** | Complete `T-FR-0004-11` in its child worktree, update only that progress row, push the ticket branch, and merge it back to `feat/FR-0004-centralized-users-auth`. Do not treat PR #56 as feature-complete until `T-FR-0004-11` through `T-FR-0004-16` are done. |

### Parallel streams

**FR-0006** feature-complete — PR to **`main`** pending. [`90-closeout.md`](feature-history/FR-0006-design-language/90-closeout.md).

**Kindling FR-0001** — merged [kindling PR #1](https://github.com/mcelhennyi/kindling/pull/1) @ `f64b6a1`; hearth submodule bumped on `feat/FR-0006-design-language` @ `df20872`.

**FR-0004** reopened for multi-user — `T-FR-0004-02` through `T-FR-0004-10` merged into `feat/FR-0004-centralized-users-auth`, but product correction requires `T-FR-0004-11` through `T-FR-0004-16` before feature closeout. [PR #56](https://github.com/mcelhennyi/hearth/pull/56) should remain a feature-branch preview, not final merge, until the multi-user wave lands.

---

## Progress

| Ticket | Title | TEST | DEV | VAL | Notes |
|--------|-------|------|-----|-----|-------|
| T-FR-0000-01 | Choose stack and scaffold repository | done | done | done | **FR-0000 closed** — [`90-closeout.md`](feature-history/FR-0000-bootstrap/90-closeout.md). Implementation scaffold: **FR-0001** `T-FR-0001-01` (active). |
| T-FR-0002-01 | Caddy + tls internal + static placeholder | done | done | done | `FR-0002`. Caddy `tls internal` stack + `./develop` `up/down/ca-export`. |
| T-FR-0002-02 | Mantle PWA bones (manifest + SW + nav) | done | done | done | `FR-0002`. Reuses into `T-FR-0001-04`. `apps/hub/web` with Vite-PWA + responsive nav. |
| T-FR-0002-03 | Web Push round-trip (VAPID + subscribe + send) | done | done | done | `FR-0002`. Reuses into `T-FR-0001-09`. FastAPI push endpoints + SW/UI + VAPID generator. |
| T-FR-0002-04 | Real-iPhone walkthrough + closeout report | done | done | done | **FR-0002 closed** — Pi + iPhone TLS/push validated; `40-prototype-report.md`. |
| T-FR-0003-01 | Design contract: amend deployment for Docker-on-Pi | done | done | done | `FR-0003` **done** on `main` (PR #13). |
| T-FR-0003-02 | Install layout: `hearth/`, VERSION.json, README | done | done | done | `FR-0003` **done** on `main`. |
| T-FR-0003-03 | `./install` bootstrap: Docker + layout + first `compose up` | done | done | done | `FR-0003` **done** on `main`. |
| T-FR-0003-04 | `hearth` CLI core: argparse, paths, doctor, compose passthrough | done | done | done | `FR-0003` **done** on `main`. |
| T-FR-0003-05 | Plugin registry file + Compose fragment generation | done | done | done | `FR-0003` **done** on `main`. |
| T-FR-0003-06 | `hearth --update` | done | done | done | `FR-0003` **done** on `main`. |
| T-FR-0003-07 | `hearth --plugin --add` and `list` | done | done | done | `FR-0003` **done** on `main`. |
| T-FR-0003-08 | `hearth --plugin enter` | done | done | done | `FR-0003` **done** on `main`. |
| T-FR-0003-09 | `hearth` stack control: start/stop/restart/status/logs | done | done | done | `FR-0003` **done** on `main`. |
| T-FR-0003-10 | Kindling contract: `scripts/install` + `plugin` template | done | done | done | `FR-0003` **done** on `main`. |
| T-FR-0003-11 | Per-plugin `plugin` executable: lifecycle + passthrough | done | done | done | `FR-0003` **done** on `main`. |
| T-FR-0003-12 | Smoke tests + ARM CI for install path | done | done | done | `FR-0003` **done** on `main`. |
| T-FR-0003-13 | Project rules: Hearth CLI parity (Cursor + Claude) | done | done | done | `FR-0003` **done** on `main`. |
| T-FR-0001-01 | Repo scaffold and Compose dev loop | done | done | done | `FR-0001`. Smoke test passes: HTTP 200 + "Hearth" body. `.dockerignore`, pnpm workspace, static placeholder. Host-only VAL (Docker-in-Docker not available in hearth-test). Merged to `feat/FR-0001-hearth-platform` via [PR #20](https://github.com/mcelhennyi/hearth/pull/20). |
| T-FR-0001-02 | Hub API skeleton and SQLite registry | done | done | done | `FR-0001`. FastAPI routes, SQLAlchemy models, Alembic migration. 26 tests pass via Docker. Merged to `feat/FR-0001-hearth-platform` via [PR #21](https://github.com/mcelhennyi/hearth/pull/21). |
| T-FR-0001-03 | Tinder loader and manifest schema | done | done | done | `FR-0001`. Pydantic schema + loader + 5 fixtures + 17 tests. Wired into POST /api/plugins/install. 43 total tests pass via Docker. [PR #23](https://github.com/mcelhennyi/hearth/pull/23). |
| T-FR-0001-04 | Mantle PWA shell and iframe embed | done | done | done | `FR-0001`. Dynamic nav from registry, `mantle/` components, no hardcoded plugin slugs. 7 tests pass via Docker. Merged to `feat/FR-0001-hearth-platform` via [PR #22](https://github.com/mcelhennyi/hearth/pull/22). |
| T-FR-0001-05 | Caddy generation and local TLS | done | done | done | `FR-0001`. Fragment renderer + reload hook (Caddy admin API) + Caddyfile.template. 8 unit tests; integration test gated on `HEARTH_INTEGRATION=1`. iPhone walkthrough deferred (manual). [PR #27](https://github.com/mcelhennyi/hearth/pull/27). |
| T-FR-0001-06 | Spark v1 broker and client libs | done | done | done | `FR-0001`. Broker + Python client + TS stub + 23 tests. 127 total tests pass. [PR #24](https://github.com/mcelhennyi/hearth/pull/24). |
| T-FR-0001-07 | Kindling repo and CLI | done | done | done | `FR-0001`. `kindling/` local dir created; CLI (`new`/`validate`/`install`); 17 new tests; 198 total pass. Separate repo/submodule deferred (DESIGN-GAP, scope-right). [PR #26](https://github.com/mcelhennyi/hearth/pull/26). |
| T-FR-0001-08 | groceries reference plugin | done | done | done | `FR-0001`. grocery-list repo pushed; submodule at apps/groceries; 4 install tests + conftest; 210 tests pass via Docker. iPhone walkthrough deferred (same as T05/T09). |
| T-FR-0001-09 | Auth, VAPID, Web Push + ntfy | done | done | done | `FR-0001`. argon2id auth, itsdangerous sessions, lockout, Web Push (VAPID+410 pruning), ntfy. 141 tests pass via Docker. Manual iPhone VAL deferred (needs real device). [PR #25](https://github.com/mcelhennyi/hearth/pull/25). |
| T-FR-0001-10 | Pi/Mac mini install.sh + backup | done | done | done | `FR-0001`. deploy/install.sh + systemd/launchd units + hearth backup/restore. 235 tests pass via Docker. [PR #30](https://github.com/mcelhennyi/hearth/pull/30). |
| T-FR-0004-01 | Design amendments: centralized auth architecture | done | done | done | `FR-0004` resumed; 2026-05-26 audit added built-in path, trust-header, and Kindling changelog requirements. |
| T-FR-0004-02 | Built-in hearth-users plugin scaffold | done | done | done | Built-in manifest/schema, first-boot registration, uninstall guard, FastAPI `/health`, placeholder Vite UI, and dev Caddy/Compose route implemented. Validation after merging feature @ `5f461e4`: targeted `./develop test` 5 passed; full `./develop test` 243 passed, 3 skipped; Compose Caddy `/hearth-users/` and `/hearth-users/health` HTTP 200. |
| T-FR-0004-03 | Users plugin: password, session, verify API | done | done | done | `FR-0004`. Plugin-owned SQLite, Argon2id setup, secure session cookie, login/logout, `/api/session`, and `/api/verify` claims implemented. Validation: `./develop test` 251 passed, 3 skipped; focused login-cookie/verify vectors 2 passed. PR #48. |
| T-FR-0004-04 | Hub auth verify alias and provider settings | done | done | done | Merged latest `feat/FR-0004-centralized-users-auth` with T06 preserved. Auth settings, hub `/api/auth/verify`, signed `X-Hearth-User-*` headers, fail-closed provider handling, persisted `HEARTH_USER_SIG_SECRET`, plugin Compose secret injection, and dev Compose `argon2-cffi` for `hearth-users` implemented. Validation: focused merged slice 75 passed; full `./develop test` 266 passed, 3 skipped; Caddy sidecar `/api/auth/verify` returned 401 without session and 200 with signed headers after login. |
| T-FR-0004-05 | Caddy auth_request and header injection | done | done | done | Hub and install Caddy fragments now strip inbound `X-Hearth-*`, forward-auth through `/api/auth/verify`, copy signed user headers, preserve API 401s, and redirect HTML to `/hearth-users/login?next=...`. Validation: focused proxy/compose tests 15 passed, 1 skipped; full `./develop test` 269 passed, 3 skipped. |
| T-FR-0004-06 | Spark session capabilities and builtin registry rules | done | done | done | `FR-0004`. Spark `session.current` works for `hub` via permission-checked local handler; `hearth-users` declares session capability/events, auth/session audit JSONL, and builtin disable/uninstall are rejected pending T04 external-provider settings. Validation: `./develop test` 257 passed, 3 skipped. |
| T-FR-0004-07 | Kindling template: trust middleware and no local login | done | done | done | Generated Python template now ships `require_hearth_user()` trust middleware, protected-route sample, no-local-login README/useUser guidance, and dense child-repo compliance changelog. Combined feature validation: focused template tests 13 passed; full `./develop test` 275 passed, 3 skipped. |
| T-FR-0004-08 | Mantle shell: login via hearth-users and useUser contract | done | done | done | `FR-0004`. Shell fetches `/hearth-users/api/session`, sends unauth users to `/hearth-users/login?next=...`, broadcasts verified `hearth.user` claims to plugin iframes, and removes hub password-form duplication. Validation: `./develop web npm run test` 11 passed; `./develop web npm run lint` passed; `./develop web npm run build` passed. Real iPhone PWA login-once walkthrough documented as host/manual exception. |
| T-FR-0004-09 | External auth provider stub and operator settings UI | done | done | done | `FR-0004`. Settings route records builtin/external provider toggles and external verify URLs; hub verify fails closed when builtin auth is disabled and preserves the external provider header contract. Combined feature validation: focused API 13 passed; full `./develop test` 276 passed, 3 skipped; web Vitest 4 files/12 tests passed; web build passed; web lint passed. |
| T-FR-0004-10 | E2E: plugin trusts gateway identity | done | done | done | `FR-0004` capstone. Hub verify signs identity for the public plugin URI; Caddy forwards original method/URI to the plugin; generated Kindling plugin rejects direct calls and accepts verified gateway headers. Validation: focused 16 passed, 1 skipped; full `./develop test` 277 passed, 3 skipped; web test/build/lint passed. |
| T-FR-0004-11 | Multi-user design amendment and migration plan | — | — | — | `FR-0004` multi-user extension. Deps: T-FR-0004-10. Next frontier seed. |
| T-FR-0004-12 | Users plugin: multi-user schema, migration, and auth API | — | — | — | `FR-0004` multi-user extension. Deps: T-FR-0004-11. |
| T-FR-0004-13 | Hearth Users UI: first admin setup and username login | — | — | — | `FR-0004` multi-user extension. Deps: T-FR-0004-12. |
| T-FR-0004-14 | Session, Spark, gateway, and Mantle claims use real users | — | — | — | `FR-0004` multi-user extension. Deps: T-FR-0004-12. |
| T-FR-0004-15 | Admin user management API and settings UI | — | — | — | `FR-0004` multi-user extension. Deps: T-FR-0004-12, T-FR-0004-14. |
| T-FR-0004-16 | Multi-user E2E and compliance changelog refresh | — | — | — | `FR-0004` multi-user extension. Deps: T-FR-0004-13, T-FR-0004-14, T-FR-0004-15. |
| T-FR-0005-01 | Remote-build profile in deployment.md | — | — | — | `FR-0005` **design**. |
| T-FR-0005-02 | `hearth pwa publish` (rsync static to Pi) | — | — | — | `FR-0005` **design**; Pi **`192.168.1.62`**. Deps: T-FR-0005-01. |
| T-FR-0005-03 | Hub image build and publish (arm64 bundle) | — | — | — | `FR-0005` **design** P1. Deps: T-FR-0005-01. |
| T-FR-0005-04 | SETUP.md Mac-build / Pi-runtime operator guide | — | — | — | `FR-0005` **design**. Deps: T-FR-0005-02. |
| T-FR-0005-05 | Publish smoke test and doctor hints | — | — | — | `FR-0005` **design**. Deps: T-FR-0005-02. |
| T-FR-0006-01 | System tiles & strips API | done | done | done | `FR-0006`. DF-U1, DF-U2. 16 pytest; [PR #31](https://github.com/mcelhennyi/hearth/pull/31) → `feat/FR-0006-design-language`. |
| T-FR-0006-02 | Dashboard layout API | done | done | done | `FR-0006`. GET/PUT layout; 10 pytest; [PR #32](https://github.com/mcelhennyi/hearth/pull/32). |
| T-FR-0006-03 | Mantle postMessage bridge | done | done | done | `FR-0006`. Shell bridge; 24 Vitest; [PR #33](https://github.com/mcelhennyi/hearth/pull/33). |
| T-FR-0006-04 | User preferences API + Settings modal | done | done | done | `FR-0006`. [PR #40](https://github.com/mcelhennyi/hearth/pull/40); merged to feature @ `8598fd5`. |
| T-FR-0006-05 | Plugin frame state UI | done | done | done | `FR-0006`. [PR #39](https://github.com/mcelhennyi/hearth/pull/39). |
| T-FR-0006-06 | Chrome slot DOM + rendering | done | done | done | `FR-0006`. [PR #37](https://github.com/mcelhennyi/hearth/pull/37). |
| T-FR-0006-07 | Dashboard grid + block primitives | done | done | done | `FR-0006`. Grid + blocks; merged to feature @ `8598fd5`. |
| T-FR-0006-08 | Empty state | done | done | done | `FR-0006`. [PR #42](https://github.com/mcelhennyi/hearth/pull/42); merged @ `f861c57`. |
| T-FR-0006-09 | Edit mode | done | done | done | `FR-0006`. [PR #44](https://github.com/mcelhennyi/hearth/pull/44); merged @ `f861c57`. |
| T-FR-0006-10 | @kindling/mantle package scaffold | done | done | done | `FR-0006`. `packages/mantle/`; [PR #34](https://github.com/mcelhennyi/hearth/pull/34). |
| T-FR-0006-11 | @kindling/mantle base components | done | done | done | `FR-0006`. [PR #41](https://github.com/mcelhennyi/hearth/pull/41). |
| T-FR-0006-12 | @kindling/mantle hooks | done | done | done | `FR-0006`. [PR #35](https://github.com/mcelhennyi/hearth/pull/35). |
| T-FR-0006-13 | @kindling/mantle overlays | done | done | done | `FR-0006`. [PR #43](https://github.com/mcelhennyi/hearth/pull/43); merged @ `f861c57`. |
| T-FR-0006-14 | @kindling/mantle vanilla bridge | done | done | done | `FR-0006`. [PR #36](https://github.com/mcelhennyi/hearth/pull/36). |
| T-FR-0006-15 | @kindling/mantle publish | done | done | done | `FR-0006`. [PR #45](https://github.com/mcelhennyi/hearth/pull/45); merged @ `110dd0a`. **`NPM_TOKEN`** for first publish. |

---

## How to choose next work

1. **FR-0003** is **closed** on **`main`** — see [`90-closeout.md`](feature-history/FR-0003-hearth-pi-docker-cli/90-closeout.md).
2. **FR-0001** is **done** on **`main`** — merged [PR #30](https://github.com/mcelhennyi/hearth/pull/30) @ `0811ed2`; [`90-closeout.md`](feature-history/FR-0001-hearth-platform/90-closeout.md).
3. **FR-0004** is **reopened for multi-user**. Run `/develop-frontier` from the FR-0004 feature worktree; the first eligible ticket is [`T-FR-0004-11`](feature-history/FR-0004-centralized-users-auth/tickets.md#t-fr-0004-11--multi-user-design-amendment-and-migration-plan). **FR-0005** remains **`design`** and should wait unless explicitly prioritized.
4. If **Session status** is `blocked`, resolve the blocker before starting new parallel batches.
