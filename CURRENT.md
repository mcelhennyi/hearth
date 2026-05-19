## Current Branch

- Branch: `feat/FR-0002-iphone-pwa-prototype`
- Status: `testing`
- Merged tickets: `T-FR-0002-01`, `T-FR-0002-02`, `T-FR-0002-03`
- Active ticket: `T-FR-0002-04` (real-device walkthrough + closeout)

## Integrated Outcome

- Ticket 01: local TLS Caddy stack + CA export flow.
- Ticket 02: Mantle static PWA shell + SW + responsive nav.
- Ticket 03: FastAPI push endpoints, VAPID generation, push test wiring, and 410-pruning behavior.

## Preflight Validation (containerized)

- `./develop vapid-gen` passed.
- `./develop api pytest` passed.
- `./develop web npm run test` passed.
- `./develop up -d` + `curl ... /api/health` + `curl ... /api/push/test` + `./develop down` passed.

## Next Action

- Branch merged with **`origin/main`** (2026-05-19): includes **`./install`** and FR-0003 tooling; PWA stack unchanged (`./develop up`, `hearth.home.arpa`).
- Execute real-iPhone acceptance walkthrough on Mac mini and Pi 4.
- Fill evidence in `tasks/feature-history/FR-0002-iphone-pwa-prototype/40-prototype-report.md`.
- If any R1-R5 risk fails, file DESIGN-FLAW amendment(s) against `docs/design/mantle-ui.md`, `docs/design/deployment.md`, or `docs/design/notifications.md`.
