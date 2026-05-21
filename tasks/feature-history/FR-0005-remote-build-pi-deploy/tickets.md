# Tickets — FR-0005 Remote build, Pi deploy

**Feature id:** **`FR-0005`**
**Canonical ids:** **`T-FR-0005-xx`**
**DAG:** [`20-tickets-dag.md`](20-tickets-dag.md)
**Progress tracker:** [`tasks/ticket-progress.md`](../../ticket-progress.md)

Phases follow `docs/ai-context.md`: **TEST → DEV → VAL** per ticket.

---

### T-FR-0005-01 — Remote-build profile in deployment.md

**Title:** Remote-build profile in deployment.md
**Deps:** `none`

#### Purpose

Add a **Remote build (Mac → Pi)** subsection to [`docs/design/deployment.md`](../../../docs/design/deployment.md) under the Docker profile: actors, artifact paths (`hearth/compose/static/`), explicit “do not run `hearth pwa build` on Pi for routine UI updates”, and pointer to forthcoming `hearth pwa publish`. Relate to **DG-D1** (registry images) vs operator-local image bundle.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Acceptance checklist | Intake success criteria map 1:1 to doc bullets or **DESIGN-GAP**. |
| **DEV** | Amend `deployment.md` | Mermaid or table for Mac build → rsync → Pi restart; no contradiction with existing `hearth pwa build` on-Pi path. |
| **VAL** | Cross-read | FR-0003 README + `SETUP.md` links still coherent. |

---

### T-FR-0005-02 — `hearth pwa publish` (rsync static to Pi)

**Title:** `hearth pwa publish` (rsync static to Pi)
**Deps:** `T-FR-0005-01`

#### Purpose

Implement **`hearth pwa publish`** in `deploy/hearth-cli/hearth_cli/pwa_ops.py` (and CLI wiring): rsync local **`hearth/compose/static/`** to a remote Pi install over SSH; flags `--target`, `--install-remote`, `--build`, `--dry-run`; env `HEARTH_PUBLISH_TARGET`, `HEARTH_PUBLISH_INSTALL`.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Unit tests | Mock subprocess/rsync: verifies argv, remote path, dry-run; fails clearly when static dir missing. |
| **DEV** | CLI + implementation | `hearth pwa publish --help`; successful publish prints remote path + reminder to `hearth restart caddy` on Pi. |
| **VAL** | Manual Mac → Pi | Diary entry: build on Mac, publish to **`192.168.1.62`**, confirm UI updates without `npm` on Pi. |

#### Notes

- Dependency: **`rsync`** and **`ssh`** on Mac PATH (document in SETUP).
- v0: remote install root may be **required** via flag/env (no magic autodetect).

---

### T-FR-0005-03 — Hub image build and publish (arm64 bundle)

**Title:** Hub image build and publish (arm64 bundle)
**Deps:** `T-FR-0005-01`

#### Purpose

Add **`hearth image build`** and **`hearth image publish`** so the hub API image can be built on Mac for **`linux/arm64`**, transferred to the Pi (`docker save` / `scp` / `docker load`), and referenced from a generated Compose override so Pi **`docker compose up`** does not run `build:` for hub on routine updates.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Contract tests | Dry-run documents buildx/save/load commands; tag naming stable. |
| **DEV** | CLI module | New `hearth_cli/image_ops.py` (or equivalent); override fragment under `hearth/compose/overrides/`; does not break default on-Pi `build:` when override absent. |
| **VAL** | ARM load | Pi at **`192.168.1.62`** loads image and `hearth status` healthy without `compose build` on Pi for hub. |

#### Notes

- **Out of scope:** plugin images, registry push (**DG-D1**).
- Requires **Docker buildx** on Mac; document fallback “build on Pi once” in SETUP.

---

### T-FR-0005-04 — SETUP.md Mac-build / Pi-runtime operator guide

**Title:** SETUP.md Mac-build / Pi-runtime operator guide
**Deps:** `T-FR-0005-02`

#### Purpose

Update repo-root [`SETUP.md`](../../../SETUP.md): new section for operators who use a **Mac build host** and **Pi runtime** — env vars, `hearth pwa build` on Mac, `hearth pwa publish`, SSH keys, Pi-side `hearth restart caddy` only; deprecate “run `hearth pwa build` on the Pi” as the **recommended** path.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Doc checklist | Every command in skeleton sequence appears in SETUP with expected host (Mac vs Pi). |
| **DEV** | Edit SETUP.md | Copy-paste blocks; link to `deployment.md` remote-build subsection. |
| **VAL** | Walkthrough | Fresh reader can follow without opening `pwa_ops.py`. |

---

### T-FR-0005-05 — Publish smoke test and doctor hints

**Title:** Publish smoke test and doctor hints
**Deps:** `T-FR-0005-02`

#### Purpose

Extend CI or `scripts/ci/` smoke: `hearth pwa publish --dry-run` with fixture install tree; **`hearth doctor`** warns when `HEARTH_PUBLISH_TARGET` unset on Mac-like hosts (optional heuristic) or always prints “remote publish available” when `rsync` missing.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | pytest | Dry-run publish exits 0; missing static exits non-zero. |
| **DEV** | Implement | Wired in existing hearth-cli test layout under `tests/`. |
| **VAL** | CI green | `./develop test` (or documented host pytest) passes. |
