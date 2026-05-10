# CURRENT — `T-FR-0002-01` Caddy + local TLS placeholder

**Branch:** `feat/FR-0002-iphone-pwa-prototype-T-FR-0002-01-caddy-tls`  
**Feature:** `FR-0002` — iPhone PWA prototype  
**Ticket:** `T-FR-0002-01`

## Phase status

| Phase | Status |
|-------|--------|
| TEST | done — `scripts/test-t-fr-0002-01.sh` |
| DEV | done — `deploy/compose/docker-compose.yml`, `deploy/caddy/Caddyfile.dev`, `./develop up \| down \| ca-export`, static `deploy/static/` |
| VAL | **pending** — server-first on Mac mini or Pi + trusted CA in desktop browser (`tasks/feature-history/FR-0002-iphone-pwa-prototype/tickets.md`) |

## Blocker

Automated session cannot complete LAN hardware VAL. Evidence and checklist: `tasks/feature-history/FR-0002-iphone-pwa-prototype/parallel/T-FR-0002-01-val-evidence.md`.

## Next actions

1. Open or refresh PR **into** `feat/FR-0002-iphone-pwa-prototype` (not `main`).
2. Operator: run stack on target host, trust exported CA on client, verify `https://hearth.home.arpa/` without TLS warnings; then set VAL done in `tasks/ticket-progress.md` and add `triadDone` for `TFR0002_01_*` in `docs/design/tickets-initial.md`.
