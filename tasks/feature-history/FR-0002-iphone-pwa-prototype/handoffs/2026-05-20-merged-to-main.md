# 2026-05-20 — FR-0002 merged to `main`

## Merge

- **PR:** [#3](https://github.com/mcelhennyi/hearth/pull/3) — `feat/FR-0002-iphone-pwa-prototype` → `main`
- **Merge commit:** `8bb7eff`
- **Repo-root `CURRENT.md`:** deleted on `main` (post-merge bookkeeping)

## Tickets integrated

| Ticket | Summary |
|--------|---------|
| `T-FR-0002-01` | Caddy `tls internal` + `./develop` / `hearth ca-export` |
| `T-FR-0002-02` | Mantle PWA shell (`apps/hub/web`) |
| `T-FR-0002-03` | Web Push API + VAPID |
| `T-FR-0002-04` | Pi + iPhone closeout report |

## Validation (pre-merge)

- CI: `hearth-install-smoke` (amd64 + arm64) green on PR #3
- Operator: Pi (`hearth-server`) — Pi-hole DNS, CA trust, PWA + push on iPhone
- Container: `./develop` pytest / web tests / `scripts/test-t-fr-0002-01.sh`

## Executive summary

FR-0002 is **done**. `main` now ships the home-server PWA slice: Caddy on `hearth.home.arpa`, static Mantle shell with service worker, FastAPI Web Push, and operator paths via **`./install`**, **`hearth pwa build`**, and **`hearth ca-export`** (`SETUP.md`). Mac mini acceptance remains a **later phase** (SETUP §11).

## Suggested next step

Resume **FR-0001** platform MVP: **`T-FR-0001-01`** (scaffold/registry) or **`/identify-frontier`**. Reuse FR-0002 code for **`T-FR-0001-04`**, **`-05`**, **`-09`**.

## Options

- Start FR-0001 on `main` with feature branch `feat/FR-0001-hearth-platform`.
- Optional: run Mac mini walkthrough (Environment A in `40-prototype-report.md`) without reopening FR-0002.

## Branch hygiene

Remote **`feat/FR-0002-*`** branches retained as audit trail (not deleted).
