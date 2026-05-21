# FR-0005 — Intake

| Field | Value |
|------|--------|
| **Title** | Remote build on Mac, deploy to Pi without on-device builds |
| **Requester** (optional) | Operator (home Pi deployment) |
| **Target timeline** (optional) | After FR-0001 on `main` |
| **Constraints** | SSH access Mac → Pi; existing `HEARTH_INSTALL_ROOT` / `hearth/` layout; no new cloud registry required for v0 |
| **Success definition** | (1) PWA static can be built on Mac and published to the Pi install in one documented command sequence. (2) Pi routine UI update does not run `npm ci` / `vite build`. (3) `SETUP.md` documents the Mac → Pi workflow. |
| **Out of scope** | CI publishing pipeline to a public registry (partially overlaps **DG-D1**); plugin image matrix; replacing `git pull` on the Pi for deploy-repo updates |
| **Links** | [`SETUP.md`](../../../SETUP.md) §4, [`deploy/hearth-cli/hearth_cli/pwa_ops.py`](../../../deploy/hearth-cli/hearth_cli/pwa_ops.py), [`docs/design/deployment.md`](../../../docs/design/deployment.md) |

**Operator environment (home LAN):**

| Host | Address | Notes |
|------|---------|--------|
| Hearth Pi | **`192.168.1.62`** | Runtime; SSH/rsync publish target (last octet **`.62`**) |

Example publish target when implementing **T-FR-0005-02**: `HEARTH_PUBLISH_TARGET=pi@192.168.1.62` (adjust SSH user if not `pi`).

**Raw details** (prose the user or PM provided):

Hearth PWA build takes forever on the Pi. Set up a way to build on the Mac instead, then move the result to the Pi for deployment so the Pi does not need to build anything (for UI updates at minimum).

**Current behavior (baseline):**

- `hearth pwa build` on the Pi invokes `./develop web npm ci` and `npm run build` inside a Node container, then copies `apps/hub/web/dist` → `hearth/compose/static/`.
- Install Compose still uses `build:` for the hub API image when `hearth --update` runs on the Pi (**DG-D1**).

**Desired behavior:**

- **Mac:** build static (existing tooling), **publish** to Pi `hearth/compose/static/` via SSH/rsync.
- **Pi:** `hearth restart caddy` (or `compose up` if needed) — no frontend compile on the device.
- **Optional follow-on:** pre-built **linux/arm64** hub image tarball loaded on the Pi so hub `build:` is also skipped.
