# Ticket progress

## Current focus

| Field | Value |
|-------|--------|
| **Active ticket** | `T-FR-0002-01` and `T-FR-0002-02` (parallel-eligible; not yet started) |
| **Active phase** | TEST kickoff (`T-FR-0002-01`, `T-FR-0002-02`) |
| **Branch / worktree** | `feat/FR-0002-iphone-pwa-prototype` at `.worktrees/FR-0002-iphone-pwa-prototype/feature/`; ticket branches next: `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls`, `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones` |
| **Session status** | `developing` |
| **Next agent should** | Launch one subagent per frontier ticket and execute TEST → DEV → VAL in each ticket worktree, then merge both ticket branches into `feat/FR-0002-iphone-pwa-prototype` using `finish-feature` flow. Keep FR-0001 parked until FR-0002 closes. **VAL:** server-first (Mac mini / Pi + desktop browser) per `tasks/feature-history/FR-0002-iphone-pwa-prototype/tickets.md`; iPhone checks are follow-up only (`40-prototype-report.md` → **Follow-up: iPhone**). |

### Parallel streams

`T-FR-0002-01` and `T-FR-0002-02` are independent and can run in parallel — one builds the proxy + TLS, the other builds the static Mantle shell. Both must land before `T-FR-0002-03` (Web Push needs the SW reachable over `https://`).

| Stream label | Ticket(s) | `FR-NNNN` | Branch / worktree | Owner / note |
|----------------|------------|-----------|-------------------|--------------|
| caddy-tls | `T-FR-0002-01` | `FR-0002` | `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls` at `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls/` | unassigned |
| mantle-bones | `T-FR-0002-02` | `FR-0002` | `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones` at `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones/` | unassigned |

---

## Progress

| Ticket | Title | TEST | DEV | VAL | Notes |
|--------|-------|------|-----|-----|-------|
| T-FR-0000-01 | Choose stack and scaffold repository | done | done | done | Stack chosen; FR-0000 tooling/process scaffold complete via `init-skeleton`. Implementation scaffold lives in `T-FR-0001-01` (parked). |
| T-FR-0002-01 | Caddy + tls internal + static placeholder | — | — | — | `FR-0002`. Reuses into `T-FR-0001-05`. |
| T-FR-0002-02 | Mantle PWA bones (manifest + SW + nav) | — | — | — | `FR-0002`. Reuses into `T-FR-0001-04`. |
| T-FR-0002-03 | Web Push round-trip (VAPID + subscribe + send) | — | — | — | `FR-0002`. Reuses into `T-FR-0001-09`. Deps: `T-FR-0002-01`, `T-FR-0002-02`. |
| T-FR-0002-04 | Real-iPhone walkthrough + closeout report | — | — | — | `FR-0002`. No FR-0001 reuse target. Deps: `T-FR-0002-01..03`. |
| T-FR-0003-01 | Design contract: amend deployment for Docker-on-Pi | — | — | — | `FR-0003` design. Deps: none. |
| T-FR-0003-02 | Install layout: `heart/`, VERSION.json, README | — | — | — | `FR-0003`. Deps: `T-FR-0003-01`. |
| T-FR-0003-03 | `./install` bootstrap: Docker + layout + first `compose up` | — | — | — | `FR-0003`. Deps: `T-FR-0003-02`, `T-FR-0003-05`. |
| T-FR-0003-04 | `hearth` CLI core: argparse, paths, doctor, compose passthrough | — | — | — | `FR-0003`. Deps: `T-FR-0003-01`, `T-FR-0003-02`. |
| T-FR-0003-05 | Plugin registry file + Compose fragment generation | — | — | — | `FR-0003`. Deps: `T-FR-0003-01`, `T-FR-0003-02`. |
| T-FR-0003-06 | `hearth --update` | — | — | — | `FR-0003`. Deps: `T-FR-0003-04`, `T-FR-0003-05`. |
| T-FR-0003-07 | `hearth --plugin --add` and `list` | — | — | — | `FR-0003`. Deps: `T-FR-0003-04`, `T-FR-0003-05`. |
| T-FR-0003-08 | `hearth --plugin enter` | — | — | — | `FR-0003`. Deps: `T-FR-0003-07`. |
| T-FR-0003-09 | `hearth` stack control: start/stop/restart/status/logs | — | — | — | `FR-0003`. Deps: `T-FR-0003-04`, `T-FR-0003-05`. |
| T-FR-0003-10 | Kindling contract: `scripts/install` + `plugin` template | — | — | — | `FR-0003`. Deps: `T-FR-0003-01`, `T-FR-0003-02`. |
| T-FR-0003-11 | Per-plugin `plugin` executable: lifecycle + passthrough | — | — | — | `FR-0003`. Deps: `T-FR-0003-07`, `T-FR-0003-10`. |
| T-FR-0003-12 | Smoke tests + ARM CI for install path | — | — | — | `FR-0003`. Deps: `T-FR-0003-03`, `T-FR-0003-06`, `T-FR-0003-08`, `T-FR-0003-09`, `T-FR-0003-11`. |
| T-FR-0003-13 | Project rules: Hearth CLI parity (Cursor + Claude) | — | — | — | `FR-0003`. Deps: `T-FR-0003-01`. |
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

1. While FR-0002 is `in-progress`: pick the smallest **`T-FR-0002-xx`** with all `Deps:` satisfied. Ignore FR-0001 tickets — they are parked.
2. **FR-0003 (`hearth` / `./install` / per-plugin `plugin`):** design-stage tickets are listed in **`tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`**. When starting implementation, prefer **`/identify-frontier`** after **`T-FR-0003-02`** is VAL-done to batch **T-FR-0003-04**, **-05**, **-10**, **-13** (and later **-06**, **-07**, **-09**). Do not let FR-0003 change **Current focus** away from FR-0002 unless the session owner explicitly switches streams.
3. After FR-0002 closes: re-flip FR-0001 to `design`/`in-progress` in `REGISTRY.md`, apply any FR-0002-driven amendments, and start `T-FR-0001-01`.
4. If **Session status** is `blocked`, resolve the blocker before starting new parallel batches.
