# Ticket progress

## Current focus

| Field | Value |
|-------|--------|
| **Active ticket** | T-FR-0006-01 (W0 batch leader) |
| **Active phase** | TEST/DEV/VAL in flight per-ticket |
| **Branch / worktree** | `feat/FR-0006-design-language` @ `.worktrees/FR-0006-design-language/feature/`; ticket worktrees under `.worktrees/FR-0006-design-language/T-FR-0006-{01,02,03,10}-*` |
| **Session status** | `developing` |
| **Next agent should** | Merge W0 PRs #31–#34 into `feat/FR-0006-design-language`, revalidate in `.worktrees/FR-0006-design-language/feature/`, then `/identify-frontier` for W1 (T-FR-0006-04/05/06/07/11/12/14). |

### Parallel streams

**FR-0002** and **FR-0003** are **done** on **`main`** ([PR #3](https://github.com/mcelhennyi/hearth/pull/3), [PR #13](https://github.com/mcelhennyi/hearth/pull/13)).

| Stream label | Ticket(s) | `FR-NNNN` | Branch / worktree | Owner / note |
|----------------|------------|-----------|-------------------|--------------|
| W0/hearth-systems | T-FR-0006-01 | FR-0006 | `feat/FR-0006-design-language-T-FR-0006-01-system-tiles` @ `.worktrees/FR-0006-design-language/T-FR-0006-01-system-tiles/` | parallel subagent |
| W0/hearth-dashboard-layout | T-FR-0006-02 | FR-0006 | `feat/FR-0006-design-language-T-FR-0006-02-dashboard-layout` @ `.worktrees/FR-0006-design-language/T-FR-0006-02-dashboard-layout/` | parallel subagent |
| W0/hearth-postmessage | T-FR-0006-03 | FR-0006 | `feat/FR-0006-design-language-T-FR-0006-03-postmessage-bridge` @ `.worktrees/FR-0006-design-language/T-FR-0006-03-postmessage-bridge/` | parallel subagent |
| W0/hearth-mantle-pkg | T-FR-0006-10 | FR-0006 | `feat/FR-0006-design-language-T-FR-0006-10-mantle-package` @ `.worktrees/FR-0006-design-language/T-FR-0006-10-mantle-package/` | parallel subagent |

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
| T-FR-0004-01 | Design amendments: centralized auth architecture | done | done | done | `FR-0004` **parked**. Design in feature tree; see diary. |
| T-FR-0004-02 | Built-in hearth-users plugin scaffold | — | — | — | `FR-0004` **parked** — after FR-0002 cert VAL + FR-0001-04 VAL. |
| T-FR-0004-03 | Users plugin: password, session, verify API | — | — | — | `FR-0004` **parked**. |
| T-FR-0004-04 | Hub auth verify alias and provider settings | — | — | — | `FR-0004` **parked**. |
| T-FR-0004-05 | Caddy auth_request and header injection | — | — | — | `FR-0004` **parked**. |
| T-FR-0004-06 | Spark session capabilities and builtin registry rules | — | — | — | `FR-0004` **parked**. |
| T-FR-0004-07 | Kindling template: trust middleware and no local login | — | — | — | `FR-0004` **parked**. |
| T-FR-0004-08 | Mantle shell: login via hearth-users and useUser contract | — | — | — | `FR-0004` **parked**. |
| T-FR-0004-09 | External auth provider stub and operator settings UI | — | — | — | `FR-0004` **parked**. |
| T-FR-0004-10 | E2E: plugin trusts gateway identity | — | — | — | `FR-0004` **parked** (capstone). |
| T-FR-0005-01 | Remote-build profile in deployment.md | — | — | — | `FR-0005` **design**. |
| T-FR-0005-02 | `hearth pwa publish` (rsync static to Pi) | — | — | — | `FR-0005` **design**; Pi **`192.168.1.62`**. Deps: T-FR-0005-01. |
| T-FR-0005-03 | Hub image build and publish (arm64 bundle) | — | — | — | `FR-0005` **design** P1. Deps: T-FR-0005-01. |
| T-FR-0005-04 | SETUP.md Mac-build / Pi-runtime operator guide | — | — | — | `FR-0005` **design**. Deps: T-FR-0005-02. |
| T-FR-0005-05 | Publish smoke test and doctor hints | — | — | — | `FR-0005` **design**. Deps: T-FR-0005-02. |
| T-FR-0006-01 | System tiles & strips API | done | done | done | `FR-0006`. DF-U1, DF-U2. 16 pytest; [PR #31](https://github.com/mcelhennyi/hearth/pull/31) → `feat/FR-0006-design-language`. |
| T-FR-0006-02 | Dashboard layout API | done | done | done | `FR-0006`. GET/PUT layout; 10 pytest; [PR #32](https://github.com/mcelhennyi/hearth/pull/32). |
| T-FR-0006-03 | Mantle postMessage bridge | done | done | done | `FR-0006`. Shell bridge; 24 Vitest; [PR #33](https://github.com/mcelhennyi/hearth/pull/33). |
| T-FR-0006-04 | User preferences API + Settings modal | — | — | — | `FR-0006` **design**. DG-U8, RW-U2. Deps: T-FR-0006-01, T-FR-0006-03. |
| T-FR-0006-05 | Plugin frame state UI | — | — | — | `FR-0006` **design**. DG-U7. Deps: T-FR-0006-03. |
| T-FR-0006-06 | Chrome slot DOM + rendering | — | — | — | `FR-0006` **design**. DG-U6 shell-side. Deps: T-FR-0006-03. |
| T-FR-0006-07 | Dashboard grid + block primitives | — | — | — | `FR-0006` **design**. Core RW-U1. Deps: T-FR-0006-02. |
| T-FR-0006-08 | Empty state | — | — | — | `FR-0006` **design**. DG-U4. Deps: T-FR-0006-07. |
| T-FR-0006-09 | Edit mode | — | — | — | `FR-0006` **design**. DG-U2, DG-U3, RW-U4. Deps: T-FR-0006-07, T-FR-0006-02. |
| T-FR-0006-10 | @kindling/mantle package scaffold | done | done | done | `FR-0006`. `packages/mantle/`; [PR #34](https://github.com/mcelhennyi/hearth/pull/34). |
| T-FR-0006-11 | @kindling/mantle base components | — | — | — | `FR-0006` **design**. Deps: T-FR-0006-10. |
| T-FR-0006-12 | @kindling/mantle hooks | done | done | done | `FR-0006`. Plugin bridge + 7 hooks; 15 Vitest (jsdom). |
| T-FR-0006-13 | @kindling/mantle overlays | — | — | — | `FR-0006` **design**. Deps: T-FR-0006-10, T-FR-0006-12. |
| T-FR-0006-14 | @kindling/mantle vanilla bridge | — | — | — | `FR-0006` **design**. Deps: T-FR-0006-10, T-FR-0006-03. |
| T-FR-0006-15 | @kindling/mantle publish | — | — | — | `FR-0006` **design**. Deps: T-FR-0006-10..14. |

---

## How to choose next work

1. **FR-0003** is **closed** on **`main`** — see [`90-closeout.md`](feature-history/FR-0003-hearth-pi-docker-cli/90-closeout.md).
2. **FR-0001** is **done** on **`main`** — merged [PR #30](https://github.com/mcelhennyi/hearth/pull/30) @ `0811ed2`; [`90-closeout.md`](feature-history/FR-0001-hearth-platform/90-closeout.md).
3. **FR-0004** is **`parked`** — unblocked; set `in-progress` in `REGISTRY.md` when staffing **`T-FR-0004-02`**. **FR-0005** is **`design`** — start with [**Remote-build profile**](feature-history/FR-0005-remote-build-pi-deploy/tickets.md#t-fr-0005-01--remote-build-profile-in-deploymentmd) ([`T-FR-0005-01`](feature-history/FR-0005-remote-build-pi-deploy/tickets.md#t-fr-0005-01--remote-build-profile-in-deploymentmd)), then [**`hearth pwa publish`**](feature-history/FR-0005-remote-build-pi-deploy/tickets.md#t-fr-0005-02--hearth-pwa-publish-rsync-static-to-pi) ([`T-FR-0005-02`](feature-history/FR-0005-remote-build-pi-deploy/tickets.md#t-fr-0005-02--hearth-pwa-publish-rsync-static-to-pi)); home Pi **`192.168.1.62`**. See [`REGISTRY.md`](feature-history/REGISTRY.md).
4. If **Session status** is `blocked`, resolve the blocker before starting new parallel batches.
