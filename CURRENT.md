## Current Branch State

- Ticket: `T-FR-0002-01`
- Branch: `feat/FR-0002-iphone-pwa-prototype-T-FR-0002-01-caddy-tls`
- Phase: `complete`
- Status: `ready_for_review`

## TEST

- `scripts/test-t-fr-0002-01.sh`: stack up, `curl` HTTPS placeholder (`hearth.home.arpa` → 127.0.0.1), `ca-export` serves PEM at `:8080/ca.crt`, teardown on exit.

## DEV

- `deploy/compose/docker-compose.yml`: `caddy` (TLS) + `ca-export`; optional `docs` + `caddy-http` profiles from merged `main`.
- `deploy/caddy/Caddyfile.dev`: `tls internal`, static root, site `hearth.home.arpa` (canonical per feature `tickets.md`).
- `deploy/static/index.html`: placeholder body marker for tests.
- `deploy/compose/README.md`: hostname + commands.
- `./develop`: `up`, `down`, `ca-export`, `ps`, plus `up-quick` and `docs`.

## VAL

- Automated: `bash scripts/test-t-fr-0002-01.sh` ⇒ PASS (Docker).
- Server-first manual steps: see `tasks/feature-history/FR-0002-iphone-pwa-prototype/serial-diary.md` (2026-05-09 entry).

## Caveat

- Git cannot use branch name `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls` while `feat/FR-0002-iphone-pwa-prototype` exists (ref namespace conflict). This work uses `feat/FR-0002-iphone-pwa-prototype-T-FR-0002-01-caddy-tls`.
