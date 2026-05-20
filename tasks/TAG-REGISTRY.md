# Tag registry

**Authority:** Allocate durable numbered ids here before use in design docs, code traceability, or handoffs. **Commit and push to the default branch before** placing ids in prose (see **`.cursor/rules/tag-reservation.mdc`**).

**Traceability prefix:** `@HRT-<AREA>-<n>` in code (areas below).

## Area letters

| Letter | Area | Typical owning paths |
|--------|------|----------------------|
| **A** | Hub API, registry, settings, SQLite | `docs/design/architecture/overview.md`, `apps/hub/api/` |
| **U** | Mantle shell, dashboard UI | `docs/design/dashboard.md`, `docs/design/mantle-ui.md`, `apps/hub/web/` |
| **D** | Deployment, install, backup, ops | `docs/design/deployment.md`, `deploy/`, `SETUP.md` |
| **S** | Spark bus, inter-plugin API | `docs/design/spark-api.md` |
| **T** | Tinder manifest, plugin contract | `docs/design/plugin-contract.md` |
| **N** | Notifications, Web Push, ntfy | `docs/design/notifications.md` |
| **I** | Identity, auth, sessions | `docs/design/architecture/overview.md` §8, FR-0004 design |
| **P** | Reverse proxy, TLS, routing | `docs/design/deployment.md`, `deploy/caddy/` |

Define new letters in this table and in **`docs/design/documentation-style.md`** before first use.

---

## Design gaps (`DG-`)

**`next_dg`:** per-area counters below (bump the area row when allocating).

| Id | Area | Status | Date | Intent | Owning doc(s) |
|----|------|--------|------|--------|----------------|
| DG-D1 | D | allocated | 2026-05-19 | Published ARM hub/plugin images + CI for Docker-on-Pi | `docs/design/deployment.md` |
| DG-D2 | D | allocated | 2026-05-19 | Rootless Docker install semantics for Pi profile | `docs/design/deployment.md` |
| DG-D3 | D | allocated | 2026-05-19 | Plugin add by friendly name / central registry (Ember-era) | `docs/design/deployment.md` |
| DG-D4 | D | allocated | 2026-05-19 | Docker profile hub DB ↔ file registry sync with bare-metal hub | `docs/design/deployment.md` |
| DG-I1 | I | allocated | 2026-05-19 | MVP LAN trust bypass (`HEARTH_TRUST_LAN`) vs required auth before FR-0004 | `docs/design/deployment.md`, open Q4 |
| DG-N1 | N | allocated | 2026-05-19 | VAPID keypair rotation and subscription invalidation | `docs/design/notifications.md`, open Q11 |
| DG-S1 | S | allocated | 2026-05-19 | Widget plugin `widget.snapshot` Spark method naming | `docs/design/spark-api.md`, `dashboard.md` |

**Next free:** DG-D5, DG-I2, DG-N2, DG-S2, DG-A1, …

---

## Design flaws (`DF-`)

**`next_df`:** 1 per area when needed.

| Id | Status | Date | Intent | Owning doc(s) |
|----|--------|------|--------|----------------|
| *(none)* | — | — | — | — |

---

## Rework required (`RW-`)

| Id | Area | Status | Date | Intent | Deviating artifact(s) |
|----|------|--------|------|--------|------------------------|
| RW-P1 | P | allocated | 2026-05-19 | Proxy narrative still says nginx in diagrams/tables; Caddy is default | `docs/design/architecture/overview.md`, `docs/design/plugin-contract.md`, `docs/design/spark-api.md` |
| RW-D1 | D | allocated | 2026-05-19 | FR-0001 README in-scope list names nginx as default proxy | `tasks/feature-history/FR-0001-hearth-platform/README.md` |
| RW-U1 | U | allocated | 2026-05-19 | Dashboard is a plugin list, not home grid + blocks | `apps/hub/web/src/App.tsx` |
| RW-U2 | U | allocated | 2026-05-19 | Shell chrome missing Settings route/surface | `apps/hub/web/src/App.tsx` |
| RW-A1 | A | allocated | 2026-05-19 | Hub API lacks registry/plugins routes (FR-0002 prototype) | `apps/hub/api/app/main.py` |
| RW-I1 | I | allocated | 2026-05-19 | Identity §8 describes hub password + nginx; FR-0004 gateway design is target | `docs/design/architecture/overview.md` §8 |

---

## Growth (`GR-`)

| Id | Area | Status | Date | Intent | monitor |
|----|------|--------|------|--------|---------|
| GR-D1 | D | allocated | 2026-05-19 | Pi 4 (4 GB) memory budget when many plugins enabled | yes |
| GR-N1 | N | allocated | 2026-05-19 | Web Push fan-out scale (devices × plugins × rate limit) | no |

---

## Refinements (`R-`)

| Id | Area | Status | Date | Intent | Owning doc(s) |
|----|------|--------|------|--------|----------------|
| R-U1 | U | allocated | 2026-05-19 | P2 user edit mode + `PUT /api/dashboard/layout` detail | `docs/design/dashboard.md` |
| R-U2 | U | allocated | 2026-05-19 | Bottom-bar overflow “More (⋯)” sheet when >3 app tabs | `docs/design/mantle-ui.md` |

---

## Decisions (`DEC-`)

| Id | Status | Date | Intent | Owning doc(s) |
|----|--------|------|--------|----------------|
| *(none)* | — | — | — | — |

---

## Trade studies (`TS-`)

| Id | Status | Date | Intent | Owning doc(s) |
|----|--------|------|--------|----------------|
| *(none)* | — | — | — | — |

---

## Features (`FR-NNNN`)

Canonical list: **`tasks/feature-history/REGISTRY.md`**. Summary only:

| Id | Status | Slug |
|----|--------|------|
| FR-0000 | done | bootstrap |
| FR-0001 | design | hearth-platform |
| FR-0002 | done | iphone-pwa-prototype |
| FR-0003 | done | hearth-pi-docker-cli |
| FR-0004 | parked | centralized-users-auth |

---

## Implementation tickets (summary)

Canonical definitions: per-feature **`tickets.md`**. Active platform batch: **`T-FR-0001-01`…`10`** (see **`tasks/ticket-progress.md`**).
