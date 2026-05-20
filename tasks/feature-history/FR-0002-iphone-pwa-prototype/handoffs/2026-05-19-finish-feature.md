# 2026-05-19 — finish-feature (FR-0002)

## Merged branches

All ticket branches were integrated on `feat/FR-0002-iphone-pwa-prototype` before this closeout:

- `T-FR-0002-01` (Caddy TLS)
- `T-FR-0002-02` (Mantle PWA bones)
- `T-FR-0002-03` (Web Push)
- `T-FR-0002-04` (closeout — this handoff)

Latest integration commits include merge with `origin/main` (`91a912e`), TS build fix (`cf35e3e`), and finish-feature closeout (install PWA stack + `hearth ca-export` / `hearth pwa`).

## Validation summary

- Container preflight: `./develop vapid-gen`, `api pytest`, `web npm run test`, `scripts/test-t-fr-0002-01.sh`
- Pi operator: TLS + Web Push on iPhone (`hearth-server`, 2026-05-19)
- `./scripts/ci/hearth-install-smoke.sh` (install layout + compose config)
- `pytest` hearth CLI / install tests

## PR

- Feature PR → `main`: (created/updated by finish-feature run)

## Executive summary

FR-0002 proves the home-server PWA slice: Caddy `tls internal` on `hearth.home.arpa`, Mantle static shell with service worker, FastAPI Web Push, and real iPhone delivery after the two-step iOS CA trust flow. Docker-profile operators use **`./install`** + **`hearth pwa build`** + **`hearth ca-export`** per **`SETUP.md`**.

## Suggested next step

Human review and merge PR to `main`; delete repo-root **`CURRENT.md`** on merge. Unpark FR-0001 per registry; apply FR-0002 reuse into `T-FR-0001-04`, `-05`, `-09`.

## Options

- **Merge** when CI green and report accepted.
- **Request changes** if additional iPhone Home Screen evidence is required before close.
