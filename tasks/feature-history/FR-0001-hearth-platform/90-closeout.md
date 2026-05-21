# FR-0001 closeout

**Closed:** 2026-05-20
**PR:** [#30](https://github.com/mcelhennyi/hearth/pull/30) — `feat/FR-0001-hearth-platform` → `main`
**Status:** feature-complete gate met; PR open for human review and merge

## All 10 tickets done

| Ticket | Title | TEST | DEV | VAL |
|--------|-------|------|-----|-----|
| T-FR-0001-01 | Repo scaffold and Compose dev loop | done | done | done |
| T-FR-0001-02 | Hub API skeleton and SQLite registry | done | done | done |
| T-FR-0001-03 | Tinder loader and manifest schema | done | done | done |
| T-FR-0001-04 | Mantle PWA shell and iframe embed | done | done | done |
| T-FR-0001-05 | Caddy generation and local TLS | done | done | done |
| T-FR-0001-06 | Spark v1 broker and client libs | done | done | done |
| T-FR-0001-07 | Kindling repo and CLI | done | done | done |
| T-FR-0001-08 | groceries reference plugin | done | done | done |
| T-FR-0001-09 | Auth, VAPID, Web Push + ntfy | done | done | done |
| T-FR-0001-10 | Pi/Mac mini install.sh + backup | done | done | done |

235 tests pass via Docker; 3 skipped (HEARTH_INTEGRATION=1 gated).

## Manual VAL deferred (not blocking gate)

Same pattern as FR-0002 closeout — manual iPhone walkthrough steps deferred for a real-device session:
- T05/T08/T09: iPhone certificate trust + PWA install + Web Push receive

These are validation steps that require a physical Pi + iPhone; they are documented in `serial-diary.md` and can be picked up as a follow-up session.

## What shipped

- **Hub API** — FastAPI, SQLite registry, Tinder manifest loader, plugin install/enable/disable, argon2id auth
- **Mantle PWA** — dynamic nav, iframe embed, install prompt, Web Push subscription, dark/light theme
- **Caddy** — fragment renderer + reload hook; generated per-plugin reverse proxy blocks
- **Spark v1** — Unix-socket JSON-RPC broker; Python + TS client libs
- **Kindling** — plugin template layer; `mcelhennyi/kindling` repo (skeleton consumer); `kindling new <slug>` scaffold
- **Groceries reference plugin** — `mcelhennyi/grocery-list` submodule at `apps/groceries/`
- **Bare-metal deploy** — `deploy/install.sh`, `deploy/systemd/`, `deploy/launchd/`, `hearth backup/restore`

## On merge to main

- Remove `CURRENT.md` from main (or it will be absent as the feature branch file is not in main baseline)
- Update `tasks/feature-history/REGISTRY.md` FR-0001 → `done`
- Update `tasks/ticket-progress.md` Current focus on main
