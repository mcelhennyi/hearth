# Ticket progress

## Current focus

| Field | Value |
|-------|--------|
| **Active ticket** | **FR-0003** — all **`T-FR-0003-xx`** implementation rows are **VAL `done`** on **`feat/FR-0003-hearth-pi-docker-cli`** (Pi hardware VAL confirmed). |
| **Active phase** | `integrating` — **PR #13** (`feat/FR-0003-hearth-pi-docker-cli` → **`main`**) ready for human merge. |
| **Branch / worktree** | Feature: `.worktrees/FR-0003-hearth-pi-docker-cli/feature/` → **`feat/FR-0003-hearth-pi-docker-cli`**. Remote **`feat/*`** ticket branches retained for audit. |
| **Session status** | `integrating` |
| **Next agent should** | Merge [**PR #13**](https://github.com/mcelhennyi/hearth/pull/13); on merge to **`main`**, remove repo-root **`CURRENT.md`**, write **`90-closeout.md`**, update **`REGISTRY.md`**. Operator guide: repo-root **`SETUP.md`**. |

### Parallel streams

`T-FR-0002-01` and `T-FR-0002-02` are independent. **FR-0003** implementation is complete on the feature branch. **`T-FR-0002-01`** and **`T-FR-0002-02`** must land before `T-FR-0002-03`.

| Stream label | Ticket(s) | `FR-NNNN` | Branch / worktree | Owner / note |
|----------------|------------|-----------|-------------------|--------------|
| caddy-tls | `T-FR-0002-01` | `FR-0002` | `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls` at `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls/` | unassigned |
| mantle-bones | `T-FR-0002-02` | `FR-0002` | `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones` at `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones/` | unassigned |
| install-smoke-arm-ci | `T-FR-0003-12` | `FR-0003` | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-12-smoke-arm-ci` at `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-12-smoke-arm-ci/` | Merged into **`feat/FR-0003-hearth-pi-docker-cli`** |

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
| T-FR-0003-02 | Install layout: `hearth/`, VERSION.json, README | done | done | done | `FR-0003`. `deploy/hearth-install/` + `./develop test`; schema `deploy/hearth-install/schemas/version-1.schema.json`. |
| T-FR-0003-03 | `./install` bootstrap: Docker + layout + first `compose up` | done | done | done | `FR-0003`. `./install` + `hearth_install.bootstrap`; hub-smoke compose placeholder; PR into feature branch. |
| T-FR-0003-04 | `hearth` CLI core: argparse, paths, doctor, compose passthrough | done | done | done | `FR-0003`. `deploy/hearth-cli/` + `bin/hearth`; `./develop test` passes; smoke: `hearth version`, `hearth doctor`, `hearth compose -- ps` against fixture install. |
| T-FR-0003-05 | Plugin registry file + Compose fragment generation | done | done | done | `FR-0003`. Generator writes `state/plugins.yaml` and `compose/overrides/generated.plugins.yml`; `./develop test`, `docker compose config`, and two-fake-plugin `compose up` smoke pass. |
| T-FR-0003-06 | `hearth --update` | done | done | done | `FR-0003`. Branch `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-06-update`; `./develop test` + dry-run VAL on temp install. |
| T-FR-0003-07 | `hearth --plugin --add` and `list` | done | done | done | `FR-0003`. `hearth_install.plugin_add` + Tinder MVP validation; `./develop test`; git installed in hearth-test Docker entry for clone coverage. |
| T-FR-0003-08 | `hearth --plugin enter` | done | done | done | `FR-0003`. Branch `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-08-plugin-enter`; VAL: Docker `hearth-test` 59 passed; manual REPL enter/exit noted in `serial-diary.md`. |
| T-FR-0003-09 | `hearth` stack control: start/stop/restart/status/logs | done | done | done | `FR-0003`. `hearth start|stop|restart|status|logs` + shared compose project/env-file; hub `/api/health` optional. VAL: `./develop test`. |
| T-FR-0003-10 | Kindling contract: `scripts/install` + `plugin` template | done | done | done | `FR-0003`. Hearth-side Kindling mirror implemented under `deploy/kindling-contract/`; Docker validation passes (`./develop test tests/test_kindling_plugin_contract.py`, `./develop test`). No upstream Kindling repo/submodule present. |
| T-FR-0003-11 | Per-plugin `plugin` executable: lifecycle + passthrough | done | done | done | `FR-0003`. `deploy/hearth-plugin-cli`, Kindling `plugin` shim, `plugin_lifecycle.py`, compose override `-f`; VAL: Docker `hearth-test` pytest (66 passed). |
| T-FR-0003-12 | Smoke tests + ARM CI for install path | done | done | done | `FR-0003`. CI smoke + **Pi hardware VAL PASS** (operator); see **`SETUP.md`** and `serial-diary.md`. |
| T-FR-0003-13 | Project rules: Hearth CLI parity (Cursor + Claude) | done | done | done | `FR-0003`. Deps: `T-FR-0003-01`. Rules + FR-0003 README process rule; PR into `feat/FR-0003-hearth-pi-docker-cli`. |
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
2. **FR-0003 (`hearth` / `./install` / per-plugin `plugin`):** All **`T-FR-0003-xx`** tickets are **VAL `done`** including Pi hardware. Merge [**PR #13**](https://github.com/mcelhennyi/hearth/pull/13) to **`main`**, then **`90-closeout.md`** when the team closes the FR line.
3. After FR-0002 closes: re-flip FR-0001 to `design`/`in-progress` in `REGISTRY.md`, apply any FR-0002-driven amendments, and start `T-FR-0001-01`. **FR-0003** may also overlap FR-0001 once work is staffed (see `tasks/feature-history/FR-0003-hearth-pi-docker-cli/README.md`).
4. If **Session status** is `blocked`, resolve the blocker before starting new parallel batches.
