## Current Branch

- Branch: `feat/FR-0002-iphone-pwa-prototype`
- Status: `closeout` (PR to `main` pending)
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

- Human: review and merge feature PR to **`main`**; delete this **`CURRENT.md`** on merge.
- Pi validation done (TLS + push). Optional Home Screen checklist items deferred in `40-prototype-report.md`.
- Operator docs: repo-root **`SETUP.md`** (`./install`, `hearth pwa build`, `hearth ca-export`).
