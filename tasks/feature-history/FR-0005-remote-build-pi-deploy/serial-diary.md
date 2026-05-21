# FR-0005 — Serial diary

## 2026-05-21 — Restored after lost uncommitted session

Prior **FR-0005** intake/design/tickets were written in an earlier session but **never committed**; tree had reverted (`REGISTRY.md` still showed **next_id: 5**). Re-created full feature folder from session transcript. Operator LAN note preserved: Hearth Pi **`192.168.1.62`** (`.62`).

## 2026-05-20 — Operator LAN note

Home Hearth Pi is at **`192.168.1.62`** (`.62` on the LAN). Use for `HEARTH_PUBLISH_TARGET` / SETUP examples when implementing publish workflow.

## 2026-05-20 — Intake + L0 design + tickets

Registered **FR-0005** (`remote-build-pi-deploy`) from operator request: PWA build on Pi is too slow; build on Mac and deploy artifacts to Pi without on-device `npm`/vite. Baseline: `hearth pwa build` shells to `./develop web npm ci` + `npm run build` (see `deploy/hearth-cli/hearth_cli/pwa_ops.py`). Planned **T-FR-0005-02** `hearth pwa publish` (rsync static); optional **T-FR-0005-03** hub image bundle. Five tickets, DAG in `20-tickets-dag.md`.
