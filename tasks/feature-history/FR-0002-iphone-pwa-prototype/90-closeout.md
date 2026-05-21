# FR-0002 closeout — iPhone PWA prototype

**Merged:** 2026-05-20 — [**PR #3**](https://github.com/mcelhennyi/hearth/pull/3) → **`main`** @ `8bb7eff`

## Executive summary

**FR-0002** de-risked the home-server **PWA slice** before FR-0001 MVP work: Caddy **`tls internal`** on `hearth.home.arpa`, a static **Mantle** shell (`apps/hub/web`) with manifest and service worker, **FastAPI Web Push** (VAPID), and operator-validated TLS + push on **Raspberry Pi** with **iPhone** on the LAN. Docker-profile installs use **`./install`**, **`hearth pwa build`**, and **`hearth ca-export`** per **`SETUP.md`**. Findings and risk verdicts: [`40-prototype-report.md`](40-prototype-report.md). **Mac mini** acceptance is a **later phase** (SETUP §11).

All **`T-FR-0002-01` … `T-FR-0002-04`** reached **VAL `done`**.

## Delivered surfaces

| Surface | Location |
|---------|----------|
| Caddy dev stack + CA export | `deploy/caddy/`, `deploy/compose/`, `./develop` |
| Mantle PWA shell | `apps/hub/web/` |
| Hub push API | `apps/hub/api/` |
| VAPID generator | `scripts/gen-vapid.py` (or `./develop vapid-gen`) |
| Operator guide | `SETUP.md` |
| Prototype report | [`40-prototype-report.md`](40-prototype-report.md) |

## Tickets

| Ticket | Summary | Status |
|--------|---------|--------|
| `T-FR-0002-01` | Caddy `tls internal` + static placeholder | TEST / DEV / VAL **done** |
| `T-FR-0002-02` | Mantle PWA bones (manifest + SW + nav) | TEST / DEV / VAL **done** |
| `T-FR-0002-03` | Web Push round-trip (VAPID + subscribe + send) | TEST / DEV / VAL **done** |
| `T-FR-0002-04` | Pi walkthrough + closeout report | TEST / DEV / VAL **done** |

## Validation

- **CI:** `hearth-install-smoke` (amd64 + arm64) green on PR #3
- **Container:** `./develop` api pytest, web tests, `scripts/test-t-fr-0002-01.sh`
- **Pi operator:** Pi-hole DNS, CA trust, PWA + push on iPhone (`hearth-server`, 2026-05-19)

## Deferred / follow-up

| Item | Tracking |
|------|----------|
| Mac mini walkthrough (Environment A) | Later phase — `40-prototype-report.md`, SETUP §11 |
| Optional iPhone Home Screen polish | **Follow-up: iPhone** in `40-prototype-report.md` |
| Reuse into FR-0001 platform | `T-FR-0001-04`, `-05`, `-09` |
| nginx → Caddy doc cleanup | `REWORK-REQUIRED RW-P1` in `docs/design/architecture/overview.md` |

## Suggested next step

Resume **FR-0001** — complete **`T-FR-0001-01`** (repo scaffold + Compose dev loop), then reuse FR-0002 artifacts for Mantle, Caddy, and Web Push tickets.

## Options

| Option | When |
|--------|------|
| **Continue FR-0001** | Default — worktree `.worktrees/FR-0001-hearth-platform/T-FR-0001-01-repo-scaffold/` |
| **`/identify-frontier`** | After `T-FR-0001-01` merges to `feat/FR-0001-hearth-platform` |
| **Mac mini walkthrough** | Optional; does not reopen FR-0002 |

## Audit

- **Merge commit:** `8bb7eff87f7d80ba8e4e7888d6f34904dd67095a`
- **Feature branch:** `feat/FR-0002-iphone-pwa-prototype` (retained on remote)
- **Ticket branches:** `feat/FR-0002-iphone-pwa-prototype-T-FR-0002-*` (retained on remote)
- **Handoffs:** [`handoffs/2026-05-19-finish-feature.md`](handoffs/2026-05-19-finish-feature.md), [`handoffs/2026-05-20-merged-to-main.md`](handoffs/2026-05-20-merged-to-main.md)
