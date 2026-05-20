# Ticket progress

## Current focus

| Field | Value |
|-------|--------|
| **Active ticket** | T-FR-0001-01 |
| **Active phase** | VAL complete |
| **Branch / worktree** | `feat/FR-0001-hearth-platform-T-FR-0001-01-repo-scaffold` / `.worktrees/FR-0001-hearth-platform/T-FR-0001-01-repo-scaffold/` |
| **Session status** | `integrating` |
| **Next agent should** | Merge T-FR-0001-01 PR into `feat/FR-0001-hearth-platform`; then start T-FR-0001-02 (Hub API skeleton and SQLite registry). |

### Parallel streams

**FR-0002** and **FR-0003** are **done** on **`main`** ([PR #3](https://github.com/mcelhennyi/hearth/pull/3), [PR #13](https://github.com/mcelhennyi/hearth/pull/13)).

| Stream label | Ticket(s) | `FR-NNNN` | Branch / worktree | Owner / note |
|----------------|------------|-----------|-------------------|--------------|
| T-FR-0001-01 scaffold | T-FR-0001-01 | FR-0001 | `feat/FR-0001-hearth-platform-T-FR-0001-01-repo-scaffold` | PR open → merge into `feat/FR-0001-hearth-platform` |

---

## Progress

| Ticket | Title | TEST | DEV | VAL | Notes |
|--------|-------|------|-----|-----|-------|
| T-FR-0000-01 | Choose stack and scaffold repository | done | done | done | Stack chosen; FR-0000 tooling/process scaffold complete via `init-skeleton`. Implementation scaffold lives in `T-FR-0001-01` (parked). |
| T-FR-0002-01 | Caddy + tls internal + static placeholder | done | done | done | `FR-0002`. Caddy `tls internal` stack + `./develop` `up/down/ca-export`. |
| T-FR-0002-02 | Mantle PWA bones (manifest + SW + nav) | done | done | done | `FR-0002`. Reuses into `T-FR-0001-04`. `apps/hub/web` with Vite-PWA + responsive nav. |
| T-FR-0002-03 | Web Push round-trip (VAPID + subscribe + send) | done | done | done | `FR-0002`. Reuses into `T-FR-0001-09`. FastAPI push endpoints + SW/UI + VAPID generator. |
| T-FR-0002-04 | Real-iPhone walkthrough + closeout report | done | done | done | `FR-0002`. Pi + iPhone TLS/push validated; report at `40-prototype-report.md`; optional Home Screen items deferred. |
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
| T-FR-0001-01 | Repo scaffold and Compose dev loop | done | done | done | `FR-0001`. Smoke test passes: HTTP 200 + "Hearth" body. `.dockerignore`, pnpm workspace, static placeholder updated. Host-only VAL (Docker-in-Docker not available in hearth-test). |
| T-FR-0001-02 | Hub API skeleton and SQLite registry | done | done | done | `FR-0001`. FastAPI routes, SQLAlchemy models, Alembic migration. 26 tests pass via Docker. |
| T-FR-0001-03 | Tinder loader and manifest schema | — | — | — | `FR-0001` parked. |
| T-FR-0001-04 | Mantle PWA shell and iframe embed | — | — | — | `FR-0001` parked. Will reuse `T-FR-0002-02` output. |
| T-FR-0001-05 | Caddy generation and local TLS | — | — | — | `FR-0001` parked. Will reuse `T-FR-0002-01` output. |
| T-FR-0001-06 | Spark v1 broker and client libs | — | — | — | `FR-0001` parked. |
| T-FR-0001-07 | Kindling repo and CLI | — | — | — | `FR-0001` parked. |
| T-FR-0001-08 | groceries reference plugin | — | — | — | `FR-0001` parked. |
| T-FR-0001-09 | Auth, VAPID, Web Push + ntfy | — | — | — | `FR-0001` parked. Will reuse `T-FR-0002-03` output. |
| T-FR-0001-10 | Pi/Mac mini install.sh + backup | — | — | — | `FR-0001` parked (closeout). |
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

---

## How to choose next work

1. **FR-0003** is **closed** on **`main`** — see [`90-closeout.md`](feature-history/FR-0003-hearth-pi-docker-cli/90-closeout.md).
2. **FR-0004** is **`parked`** — do not staff **`T-FR-0004-02`…`10`** until FR-0002 Pi certificate VAL (**`T-FR-0002-01`**, **`T-FR-0002-04`**) and FR-0001 Mantle shell VAL (**`T-FR-0001-04`**) are done. See [`FR-0004-centralized-users-auth/README.md`](feature-history/FR-0004-centralized-users-auth/README.md).
3. **FR-0002 is `done` on `main`** — resume FR-0001: start `T-FR-0001-01` (or `/identify-frontier`); reuse FR-0002 artifacts for **`T-FR-0001-04`**, **`-05`**, **`-09`**.
4. After **`T-FR-0001-04` VAL**: set FR-0004 to `in-progress` in `REGISTRY.md` and resume with **`T-FR-0004-02`**.
6. If **Session status** is `blocked`, resolve the blocker before starting new parallel batches.
