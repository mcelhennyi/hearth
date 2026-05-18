# Ticket progress

## Current focus

| Field | Value |
|-------|--------|
| **Active ticket** | **FR-0002** — pick next eligible **`T-FR-0002-xx`** (FR-0003 **closed** on **`main`**). |
| **Active phase** | `developing` / `handoff` per staffed stream. |
| **Branch / worktree** | FR-0002: `.worktrees/FR-0002-iphone-pwa-prototype/` (see **Parallel streams**). |
| **Session status** | `handoff` |
| **Next agent should** | Run **`/identify-frontier`** or continue **`T-FR-0002-02`** / **`T-FR-0002-01` VAL** per [`tasks/feature-history/FR-0002-iphone-pwa-prototype/`](feature-history/FR-0002-iphone-pwa-prototype/). FR-0003 closeout: [`FR-0003-hearth-pi-docker-cli/90-closeout.md`](feature-history/FR-0003-hearth-pi-docker-cli/90-closeout.md). |

### Parallel streams

**FR-0003** is **done** on **`main`** ([PR #13](https://github.com/mcelhennyi/hearth/pull/13)). **`T-FR-0002-01`** and **`T-FR-0002-02`** must land before `T-FR-0002-03`.

| Stream label | Ticket(s) | `FR-NNNN` | Branch / worktree | Owner / note |
|----------------|------------|-----------|-------------------|--------------|
| caddy-tls | `T-FR-0002-01` | `FR-0002` | `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls` at `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls/` | unassigned |
| mantle-bones | `T-FR-0002-02` | `FR-0002` | `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones` at `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones/` | unassigned |

---

## Progress

| Ticket | Title | TEST | DEV | VAL | Notes |
|--------|-------|------|-----|-----|-------|
| T-FR-0000-01 | Choose stack and scaffold repository | done | done | done | Stack chosen; FR-0000 tooling/process scaffold complete via `init-skeleton`. Implementation scaffold lives in `T-FR-0001-01` (parked). |
| T-FR-0002-01 | Caddy + tls internal + static placeholder | done | done | — | `FR-0002`. Local smoke PASS (`scripts/test-t-fr-0002-01.sh`); branch `feat/...-T-FR-0002-01-caddy-tls` merged with `main`. **VAL:** server-first on Pi or Mac mini still required per `tickets.md` + HOWTO — log in `serial-diary.md`. |
| T-FR-0002-02 | Mantle PWA bones (manifest + SW + nav) | — | — | — | `FR-0002`. Reuses into `T-FR-0001-04`. |
| T-FR-0002-03 | Web Push round-trip (VAPID + subscribe + send) | — | — | — | `FR-0002`. Reuses into `T-FR-0001-09`. Deps: `T-FR-0002-01`, `T-FR-0002-02`. |
| T-FR-0002-04 | Real-iPhone walkthrough + closeout report | — | — | — | `FR-0002`. No FR-0001 reuse target. Deps: `T-FR-0002-01..03`. |
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
| T-FR-0003-12 | Smoke tests + ARM CI for install path | done | done | done | `FR-0003` **done** on `main`; Pi VAL PASS; **`SETUP.md`**. |
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

---

## How to choose next work

1. **FR-0003** is **closed** on **`main`** — see [`90-closeout.md`](feature-history/FR-0003-hearth-pi-docker-cli/90-closeout.md).
2. While FR-0002 is `in-progress`: pick the smallest **`T-FR-0002-xx`** with all `Deps:` satisfied. Ignore FR-0001 tickets — they are parked.
3. After FR-0002 closes: re-flip FR-0001 to `design`/`in-progress` in `REGISTRY.md`, apply FR-0002-driven amendments, and start `T-FR-0001-01`.
4. If **Session status** is `blocked`, resolve the blocker before starting new parallel batches.
