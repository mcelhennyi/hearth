# Ticket progress

## Current focus

| Field | Value |
|-------|--------|
| **Active ticket** | `T-FR-0002-04` (closeout and real-device walkthrough) |
| **Active phase** | TEST (real-device acceptance capture) |
| **Branch / worktree** | `feat/FR-0002-iphone-pwa-prototype` at `.worktrees/FR-0002-iphone-pwa-prototype/feature/` (merged **`origin/main`** 2026-05-19) |
| **Session status** | `testing` |
| **Next agent should** | Run the full iPhone acceptance flow on Mac mini and Pi 4, fill `40-prototype-report.md` evidence + R1-R5 verdicts, then apply any required DESIGN-FLAW amendments and finish FR-0002 closeout. FR-0003 is **done** on **`main`** ([`90-closeout.md`](feature-history/FR-0003-hearth-pi-docker-cli/90-closeout.md)). |

### Parallel streams

**FR-0003** is **done** on **`main`** ([PR #13](https://github.com/mcelhennyi/hearth/pull/13)). FR-0002 closeout (`T-FR-0002-04`) is the active stream.

| Stream label | Ticket(s) | `FR-NNNN` | Branch / worktree | Owner / note |
|----------------|------------|-----------|-------------------|--------------|
| closeout | `T-FR-0002-04` | `FR-0002` | `feat/FR-0002-iphone-pwa-prototype` at `.worktrees/FR-0002-iphone-pwa-prototype/feature/` | real-device walkthrough |

---

## Progress

| Ticket | Title | TEST | DEV | VAL | Notes |
|--------|-------|------|-----|-----|-------|
| T-FR-0000-01 | Choose stack and scaffold repository | done | done | done | Stack chosen; FR-0000 tooling/process scaffold complete via `init-skeleton`. Implementation scaffold lives in `T-FR-0001-01` (parked). |
| T-FR-0002-01 | Caddy + tls internal + static placeholder | done | done | done | `FR-0002`. Caddy `tls internal` stack + `./develop` `up/down/ca-export`. |
| T-FR-0002-02 | Mantle PWA bones (manifest + SW + nav) | done | done | done | `FR-0002`. Reuses into `T-FR-0001-04`. `apps/hub/web` with Vite-PWA + responsive nav. |
| T-FR-0002-03 | Web Push round-trip (VAPID + subscribe + send) | done | done | done | `FR-0002`. Reuses into `T-FR-0001-09`. FastAPI push endpoints + SW/UI + VAPID generator. |
| T-FR-0002-04 | Real-iPhone walkthrough + closeout report | in-progress | — | — | `FR-0002`. Preflight passed; awaiting real-device evidence (Mac mini + Pi 4). |
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
| T-FR-0001-01 | Repo scaffold and Compose dev loop | — | — | — | `FR-0001` parked — eligible after FR-0002 closes. |
| T-FR-0001-02 | Hub API skeleton and SQLite registry | — | — | — | `FR-0001` parked. |
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
3. While FR-0002 is `in-progress`: pick the smallest **`T-FR-0002-xx`** with all `Deps:` satisfied. Ignore FR-0001 tickets — they are parked.
4. After FR-0002 closes: re-flip FR-0001 to `design`/`in-progress` in `REGISTRY.md`, apply FR-0002-driven amendments, and start `T-FR-0001-01` (then **`T-FR-0001-04`** for the UI gate FR-0004 needs).
5. After FR-0002 cert closeout **and** **`T-FR-0001-04` VAL**: set FR-0004 to `in-progress` in `REGISTRY.md` and resume with **`T-FR-0004-02`**.
6. If **Session status** is `blocked`, resolve the blocker before starting new parallel batches.
