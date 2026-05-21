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
| DG-U2 | U | allocated | 2026-05-21 | Dashboard edit-mode UX: entry trigger, long-press duration, exit, per viewport | `docs/design/dashboard.md` |
| DG-U3 | U | allocated | 2026-05-21 | Dashboard collision visual & save-blocking in edit mode | `docs/design/dashboard.md` |
| DG-U4 | U | allocated | 2026-05-21 | Dashboard empty-state (first-run, no plugins/blocks) | `docs/design/dashboard.md` |
| DG-U5 | U | allocated | 2026-05-21 | Dashboard responsive grid metrics (gap/padding/radius per viewport) | `docs/design/dashboard.md` |
| DG-U6 | U | allocated | 2026-05-21 | Mantle chrome-slot contract (semantics, indexing, overflow, max per zone) | `docs/design/mantle-ui.md`, `docs/design/plugin-contract.md` |
| DG-U7 | U | allocated | 2026-05-21 | Plugin iframe loading / error / crash / offline state UI | `docs/design/mantle-ui.md` |
| DG-U8 | U | allocated | 2026-05-21 | Settings modal UX + dynamic theming persistence (user setting vs OS) | `docs/design/mantle-ui.md` |
| DG-U9 | U | allocated | 2026-05-21 | `hearth.title` scope (browser tab vs top-bar h1) | `docs/design/mantle-ui.md` |
| DG-U10 | U | allocated | 2026-05-21 | Widget content overflow rules per layout tier (deferred to P3 widget host) | `docs/design/dashboard.md` |
| DG-U11 | U | allocated | 2026-05-21 | Overlay primitives: toast/haptic placement + duration + styles | `docs/design/mantle-ui.md` |
| DG-T1 | T | allocated | 2026-05-21 | In-frame sticky plugin tab bar contract (allowed shape, headers) | `docs/design/plugin-contract.md` |

**Next free:** DG-D5, DG-I2, DG-N2, DG-S2, DG-A1, DG-U12, DG-T2 …

---

## Design flaws (`DF-`)

**`next_df`:** 1 per area when needed.

| Id | Status | Date | Intent | Owning doc(s) |
|----|--------|------|--------|----------------|
| DF-U1 | allocated | 2026-05-21 | Dashboard `system` block type is underspecified (when shown, configurable, MVP status) | `docs/design/dashboard.md` |
| DF-U2 | allocated | 2026-05-21 | Dashboard `strip` block type appears in mocks but is not in the block-types table | `docs/design/dashboard.md`, `docs/design/mockups/` |
| DF-U3 | allocated | 2026-05-21 | Desktop mantle `.dock-layer` decision: keep (promote to spec) or drop (remove from mocks) | `docs/design/mantle-ui.md`, `docs/design/mockups/` |

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
| RW-U3 | U | allocated | 2026-05-21 | dashboard.md does not cross-reference mantle-ui.md bottom-bar launcher ownership and sourcing | `docs/design/dashboard.md` |
| RW-U4 | U | allocated | 2026-05-21 | Edit-mode jiggle/badge visual treatment exists in mocks only; promote required visuals to dashboard.md or relabel mocks as reference-impl | `docs/design/dashboard.md`, `docs/design/mockups/` |

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
| FR-0005 | design | remote-build-pi-deploy |
| FR-0006 | design | design-language |

---

## Implementation tickets (summary)

Canonical definitions: per-feature **`tickets.md`**. Active platform batch: **`T-FR-0001-01`…`10`** (see **`tasks/ticket-progress.md`**).
