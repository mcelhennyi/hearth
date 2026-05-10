# Ticket progress

## Current focus

| Field | Value |
|-------|--------|
| **Active ticket** | **`/develop-frontier 0003` (wave 2):** **`T-FR-0003-01`** merged (**PR #6**). Next parallel FR-0003 tickets: **`T-FR-0003-02`**, **`T-FR-0003-13`**. **FR-0002:** unchanged. |
| **Active phase** | **TEST→DEV→VAL** for **-02** and **-13** in separate ticket worktrees. |
| **Branch / worktree** | Feature: `.worktrees/FR-0003-hearth-pi-docker-cli/feature/` → `feat/FR-0003-hearth-pi-docker-cli`. Ticket **-01:** `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-01-deployment-docker-pi` → `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-01-deployment-docker-pi/`. |
| **Session status** | `developing` |
| **Next agent should** | Run **`/develop-frontier 0003`** for **`T-FR-0003-02`** + **`T-FR-0003-13`** in parallel (separate ticket worktrees). |

### Parallel streams

`T-FR-0002-01` and `T-FR-0002-02` are independent. **`T-FR-0003-01`** has no FR-0002 **Deps** and may run in parallel. **`T-FR-0002-01`** and **`T-FR-0002-02`** must land before `T-FR-0002-03`.

| Stream label | Ticket(s) | `FR-NNNN` | Branch / worktree | Owner / note |
|----------------|------------|-----------|-------------------|--------------|
| caddy-tls | `T-FR-0002-01` | `FR-0002` | `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls` at `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls/` | unassigned |
| mantle-bones | `T-FR-0002-02` | `FR-0002` | `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones` at `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones/` | unassigned |
| deployment-docker-pi | `T-FR-0003-01` | `FR-0003` | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-01-deployment-docker-pi` at `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-01-deployment-docker-pi/` | **PR #6** merged into **`feat/FR-0003-hearth-pi-docker-cli`**; **-02** / **-13** unblocked |

---

## Progress

| Ticket | Title | TEST | DEV | VAL | Notes |
|--------|-------|------|-----|-----|-------|
| T-FR-0000-01 | Choose stack and scaffold repository | done | done | done | Stack chosen; FR-0000 tooling/process scaffold complete via `init-skeleton`. Implementation scaffold lives in `T-FR-0001-01` (parked). |
| T-FR-0002-01 | Caddy + tls internal + static placeholder | done | done | — | `FR-0002`. Local smoke PASS (`scripts/test-t-fr-0002-01.sh`); branch `feat/...-T-FR-0002-01-caddy-tls` merged with `main`. **VAL:** server-first on Pi or Mac mini still required per `tickets.md` + HOWTO — log in `serial-diary.md`. |
| T-FR-0002-02 | Mantle PWA bones (manifest + SW + nav) | — | — | — | `FR-0002`. Reuses into `T-FR-0001-04`. |
| T-FR-0002-03 | Web Push round-trip (VAPID + subscribe + send) | — | — | — | `FR-0002`. Reuses into `T-FR-0001-09`. Deps: `T-FR-0002-01`, `T-FR-0002-02`. |
| T-FR-0002-04 | Real-iPhone walkthrough + closeout report | — | — | — | `FR-0002`. No FR-0001 reuse target. Deps: `T-FR-0002-01..03`. |
| T-FR-0003-01 | Design contract: amend deployment for Docker-on-Pi | done | done | done | `FR-0003` design. `deployment.md`: Docker (Pi) profile + gaps; systemd install.sh path explicit alternative. Merged via **PR #6** into **`feat/FR-0003-hearth-pi-docker-cli`**. |
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
2. **FR-0003 (`hearth` / `./install` / per-plugin `plugin`):** **`in-progress`** (2026-05-10). Feature branch **`feat/FR-0003-hearth-pi-docker-cli`** is valid; scheduling-only “park until FR-0002” is **superseded** — FR-0003 has **no ticket dependency** on FR-0002 (hub/Mantle placeholders per design). Prefer **`/identify-frontier`** after **`T-FR-0003-02`** VAL to batch **T-FR-0003-04**, **-05**, **-10**, **-13**. FR-0003 may run **in parallel with FR-0002** if capacity allows.
3. After FR-0002 closes: re-flip FR-0001 to `design`/`in-progress` in `REGISTRY.md`, apply any FR-0002-driven amendments, and start `T-FR-0001-01`. **FR-0003** may also overlap FR-0001 once work is staffed (see `tasks/feature-history/FR-0003-hearth-pi-docker-cli/README.md`).
4. If **Session status** is `blocked`, resolve the blocker before starting new parallel batches.
