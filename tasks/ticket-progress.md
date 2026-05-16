# Ticket progress

## Current focus

| Field | Value |
|-------|--------|
| **Active ticket** | **`/develop-frontier` (FR-0003 only):** **`T-FR-0003-12`** — Smoke tests + ARM CI for install path (capstone; all deps landed on **`feat/FR-0003-hearth-pi-docker-cli`**). |
| **Active phase** | **TEST → DEV → VAL** in **`.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-12-smoke-arm-ci/`** on **`feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-12-smoke-arm-ci`**. |
| **Branch / worktree** | FR-0003 feature integration: `.worktrees/FR-0003-hearth-pi-docker-cli/feature/` → **`feat/FR-0003-hearth-pi-docker-cli`**. Ticket branches use **`feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-xx-…`** (hyphenated remote style). |
| **Session status** | `developing` |
| **Next agent should** | Complete **`T-FR-0003-12`** per **`tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`**; PR **base** **`feat/FR-0003-hearth-pi-docker-cli`**; update **only** the **`T-FR-0003-12`** Progress row until VAL `done`. FR-0002 work is unchanged—pick up from Progress rows there if staffed separately. |

### Parallel streams

FR-0003 capstone only for this orchestration slice.

| Stream label | Ticket(s) | `FR-NNNN` | Branch / worktree | Owner / note |
|----------------|------------|-----------|-------------------|--------------|
| smoke-arm-ci | `T-FR-0003-12` | `FR-0003` | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-12-smoke-arm-ci` at `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-12-smoke-arm-ci/` | `/develop-frontier` FR-0003 only (2026-05-10) |

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
| T-FR-0003-02 | Install layout: `heart/`, VERSION.json, README | done | done | done | `FR-0003`. Landed on **`feat/FR-0003-hearth-pi-docker-cli`**; see feature **`CURRENT.md`**. |
| T-FR-0003-03 | `./install` bootstrap: Docker + layout + first `compose up` | done | done | done | `FR-0003`. Landed on feature branch; `./develop test` green on integration (see feature **`CURRENT.md`**). |
| T-FR-0003-04 | `hearth` CLI core: argparse, paths, doctor, compose passthrough | done | done | done | `FR-0003`. Landed on feature branch. |
| T-FR-0003-05 | Plugin registry file + Compose fragment generation | done | done | done | `FR-0003`. Landed on feature branch. |
| T-FR-0003-06 | `hearth --update` | done | done | done | `FR-0003`. Landed on feature branch. |
| T-FR-0003-07 | `hearth --plugin --add` and `list` | done | done | done | `FR-0003`. Landed on feature branch. |
| T-FR-0003-08 | `hearth --plugin enter` | done | done | done | `FR-0003`. Landed on feature branch. |
| T-FR-0003-09 | `hearth` stack control: start/stop/restart/status/logs | done | done | done | `FR-0003`. Landed on feature branch. |
| T-FR-0003-10 | Kindling contract: `scripts/install` + `plugin` template | done | done | done | `FR-0003`. Landed on feature branch. |
| T-FR-0003-11 | Per-plugin `plugin` executable: lifecycle + passthrough | done | done | done | `FR-0003`. Landed on feature branch. |
| T-FR-0003-12 | Smoke tests + ARM CI for install path | — | — | — | `FR-0003`. Capstone; deps satisfied on feature branch. **In progress** via `/develop-frontier` (FR-0003 only). |
| T-FR-0003-13 | Project rules: Hearth CLI parity (Cursor + Claude) | done | done | done | `FR-0003`. Landed on feature branch. |
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
2. **FR-0003 (`hearth` / `./install` / per-plugin `plugin`):** **`in-progress`** (2026-05-10). Feature branch **`feat/FR-0003-hearth-pi-docker-cli`** carries **`T-FR-0003-01`..`-11`** and **`-13`**; remaining implementation ticket is **`T-FR-0003-12`** (smoke + ARM CI). FR-0003 has **no ticket dependency** on FR-0002. FR-0003 may run **in parallel with FR-0002** if capacity allows.
3. After FR-0002 closes: re-flip FR-0001 to `design`/`in-progress` in `REGISTRY.md`, apply any FR-0002-driven amendments, and start `T-FR-0001-01`. **FR-0003** may also overlap FR-0001 once work is staffed (see `tasks/feature-history/FR-0003-hearth-pi-docker-cli/README.md`).
4. If **Session status** is `blocked`, resolve the blocker before starting new parallel batches.
