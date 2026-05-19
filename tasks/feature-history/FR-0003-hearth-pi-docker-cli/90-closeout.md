# FR-0003 closeout — Hearth Pi Docker CLI and install bootstrap

**Merged:** 2026-05-18 — [**PR #13**](https://github.com/mcelhennyi/hearth/pull/13) → **`main`** @ `3e4404f`

## Executive summary

**FR-0003** delivered the **Docker Compose on Pi** operator path: repo-root **`./install`**, **`<install-dir>/hearth/`** layout, **`hearth`** admin CLI (update, plugins, stack control, doctor, compose passthrough), per-plugin **`plugin`** lifecycle, Kindling contract mirror under **`deploy/kindling-contract/`**, and CI + Pi install smoke (**`scripts/ci/hearth-install-smoke.sh`**, **`.github/workflows/hearth-install-smoke.yml`**).

All **`T-FR-0003-01` … `T-FR-0003-13`** reached **VAL `done`**, including **Pi hardware validation** (operator). Design amendment **HRT-DEP-001** renamed the install tree from **`heart/`** to **`hearth/`**. Operator guide: repo-root **`SETUP.md`**.

## Delivered surfaces

| Surface | Location |
|---------|----------|
| `./install` | Repo root |
| `hearth` CLI | `bin/hearth`, `deploy/hearth-cli/` |
| Layout generator | `deploy/hearth-install/` |
| Per-plugin `plugin` | `deploy/hearth-plugin-cli/`, Kindling template |
| Deployment authority | `docs/design/deployment.md` (Docker profile) |
| Pi setup guide | `SETUP.md` |

## Validation

- **`./develop test`** — 76 passed (feature integration)
- **`./scripts/ci/hearth-install-smoke.sh`** — PASS (host/CI)
- **Pi hardware** — PASS (operator, per `serial-diary.md`)

## Deferred / follow-up

| Item | Tracking |
|------|----------|
| Published ARM hub/plugin images | DESIGN-GAP in `deployment.md` |
| Central plugin registry names for `hearth --plugin --add` | DESIGN-GAP; MVP git URL |
| Admin web UI wrapping same operations | Separate FR when hub auth exists |
| Replace hub-smoke placeholder with FR-0001 hub images | FR-0001 |
| Upstream Kindling submodule (vs Hearth mirror) | When Kindling repo is public |

## Suggested next step

Staff **FR-0002** (iPhone PWA prototype) or unpark **FR-0001** platform work; use **`/identify-frontier`** after FR-0002 ticket progress advances. New Pi installs: follow **`SETUP.md`**.

## Options

| Option | When |
|--------|------|
| **Continue FR-0002** | Default parallel product line (`T-FR-0002-02` …) |
| **Start FR-0001** | After FR-0002 learnings land; reconcile install stories with FR-0003 Docker path |
| **FR-0004 auth** | When gateway + `hearth-users` plugin design is ready to implement |

## Audit

- **Merge commit:** `3e4404ff1ce8e21db6afca3234bdafa229d9afd1`
- **Feature branch:** `feat/FR-0003-hearth-pi-docker-cli` (retained on remote)
- **Ticket branches:** `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-*` (retained on remote)
- **Handoff:** [`handoffs/2026-05-16-finish-feature.md`](handoffs/2026-05-16-finish-feature.md)
