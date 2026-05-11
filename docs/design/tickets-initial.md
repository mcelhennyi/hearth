# Tickets — index and global DAG

**Canonical definitions:** Implementation tickets (**`### T-FR-NNNN-xx`**, phases, **Deps:**) live under **`tasks/feature-history/FR-NNNN-<slug>/tickets.md`** — one file per feature line. See **`tasks/feature-history/TICKET-SOURCES.md`** and **`docs/design/documentation-style.md`**.

**This doc (`docs/design/tickets-initial.md`):** registry of **where** tickets live + **global** mermaid (cross-feature when needed) + **`triadDone`** styling for the published DAG. Do **not** duplicate full ticket bodies here; edit the per-feature **`tickets.md`** instead.

**Queue / progress:** **`tasks/ticket-progress.md`**.

**Deps:** `none` means no ticket dependency. A ticket is **eligible** when all **Deps** are **VAL** = `done` in **`ticket-progress.md`**.

**Mermaid triad nodes:** For **`T-FR-NNNN-xx`**, node ids are **`TFR` + `NNNN` + `_` + `xx` + `_` + `TEST|DEV|VAL`**. When a ticket is fully complete, add the corresponding `class … triadDone` line below (union when merging parallel work).

---

## Per-feature ticket files (canonical)

| FR id | Path (repo root) |
|-------|------------------|
| FR-0000 | `tasks/feature-history/FR-0000-bootstrap/tickets.md` |
| FR-0001 | `tasks/feature-history/FR-0001-hearth-platform/tickets.md` *(parked pending FR-0002)* |
| FR-0002 | `tasks/feature-history/FR-0002-iphone-pwa-prototype/tickets.md` |
| FR-0003 | `tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md` |

---

## DAG Overview (global)

Extend this diagram when new **`FR-NNNN`** lines add tickets that chain to existing work.

```mermaid
graph LR
  %% FR-0000 — bootstrap
  TFR0000_01_TEST --> TFR0000_01_DEV --> TFR0000_01_VAL

  %% FR-0002 — iPhone PWA prototype (active; parks FR-0001)
  TFR0002_01_TEST --> TFR0002_01_DEV --> TFR0002_01_VAL
  TFR0002_02_TEST --> TFR0002_02_DEV --> TFR0002_02_VAL
  TFR0002_03_TEST --> TFR0002_03_DEV --> TFR0002_03_VAL
  TFR0002_04_TEST --> TFR0002_04_DEV --> TFR0002_04_VAL
  TFR0002_01_VAL --> TFR0002_03_TEST
  TFR0002_02_VAL --> TFR0002_03_TEST
  TFR0002_03_VAL --> TFR0002_04_TEST

  %% FR-0001 reuse hooks (parked; FR-0002 outputs feed these)
  TFR0002_01_VAL -.reuse.-> TFR0001_05_TEST
  TFR0002_02_VAL -.reuse.-> TFR0001_04_TEST
  TFR0002_03_VAL -.reuse.-> TFR0001_09_TEST

  %% FR-0001 — Hearth platform
  TFR0001_01_TEST --> TFR0001_01_DEV --> TFR0001_01_VAL
  TFR0001_02_TEST --> TFR0001_02_DEV --> TFR0001_02_VAL
  TFR0001_03_TEST --> TFR0001_03_DEV --> TFR0001_03_VAL
  TFR0001_04_TEST --> TFR0001_04_DEV --> TFR0001_04_VAL
  TFR0001_05_TEST --> TFR0001_05_DEV --> TFR0001_05_VAL
  TFR0001_06_TEST --> TFR0001_06_DEV --> TFR0001_06_VAL
  TFR0001_07_TEST --> TFR0001_07_DEV --> TFR0001_07_VAL
  TFR0001_08_TEST --> TFR0001_08_DEV --> TFR0001_08_VAL
  TFR0001_09_TEST --> TFR0001_09_DEV --> TFR0001_09_VAL
  TFR0001_10_TEST --> TFR0001_10_DEV --> TFR0001_10_VAL

  %% inter-ticket deps (Hearth platform)
  TFR0001_01_VAL --> TFR0001_02_TEST
  TFR0001_01_VAL --> TFR0001_04_TEST
  TFR0001_01_VAL --> TFR0001_05_TEST
  TFR0001_02_VAL --> TFR0001_03_TEST
  TFR0001_02_VAL --> TFR0001_06_TEST
  TFR0001_03_VAL --> TFR0001_05_TEST
  TFR0001_04_VAL --> TFR0001_05_TEST
  TFR0001_03_VAL --> TFR0001_07_TEST
  TFR0001_04_VAL --> TFR0001_07_TEST
  TFR0001_06_VAL --> TFR0001_07_TEST
  TFR0001_07_VAL --> TFR0001_08_TEST
  TFR0001_02_VAL --> TFR0001_09_TEST
  TFR0001_04_VAL --> TFR0001_09_TEST
  TFR0001_05_VAL --> TFR0001_10_TEST
  TFR0001_08_VAL --> TFR0001_10_TEST
  TFR0001_09_VAL --> TFR0001_10_TEST

  %% FR-0003 — Pi Docker CLI + hearth/plugin tooling
  TFR0003_01_TEST --> TFR0003_01_DEV --> TFR0003_01_VAL
  TFR0003_02_TEST --> TFR0003_02_DEV --> TFR0003_02_VAL
  TFR0003_03_TEST --> TFR0003_03_DEV --> TFR0003_03_VAL
  TFR0003_04_TEST --> TFR0003_04_DEV --> TFR0003_04_VAL
  TFR0003_05_TEST --> TFR0003_05_DEV --> TFR0003_05_VAL
  TFR0003_06_TEST --> TFR0003_06_DEV --> TFR0003_06_VAL
  TFR0003_07_TEST --> TFR0003_07_DEV --> TFR0003_07_VAL
  TFR0003_08_TEST --> TFR0003_08_DEV --> TFR0003_08_VAL
  TFR0003_09_TEST --> TFR0003_09_DEV --> TFR0003_09_VAL
  TFR0003_10_TEST --> TFR0003_10_DEV --> TFR0003_10_VAL
  TFR0003_11_TEST --> TFR0003_11_DEV --> TFR0003_11_VAL
  TFR0003_12_TEST --> TFR0003_12_DEV --> TFR0003_12_VAL
  TFR0003_13_TEST --> TFR0003_13_DEV --> TFR0003_13_VAL

  TFR0003_01_VAL --> TFR0003_02_TEST
  TFR0003_01_VAL --> TFR0003_13_TEST
  TFR0003_02_VAL --> TFR0003_04_TEST
  TFR0003_02_VAL --> TFR0003_05_TEST
  TFR0003_02_VAL --> TFR0003_10_TEST
  TFR0003_05_VAL --> TFR0003_03_TEST
  TFR0003_04_VAL --> TFR0003_06_TEST
  TFR0003_05_VAL --> TFR0003_06_TEST
  TFR0003_04_VAL --> TFR0003_07_TEST
  TFR0003_05_VAL --> TFR0003_07_TEST
  TFR0003_04_VAL --> TFR0003_09_TEST
  TFR0003_05_VAL --> TFR0003_09_TEST
  TFR0003_07_VAL --> TFR0003_08_TEST
  TFR0003_07_VAL --> TFR0003_11_TEST
  TFR0003_10_VAL --> TFR0003_11_TEST
  TFR0003_03_VAL --> TFR0003_12_TEST
  TFR0003_06_VAL --> TFR0003_12_TEST
  TFR0003_08_VAL --> TFR0003_12_TEST
  TFR0003_09_VAL --> TFR0003_12_TEST
  TFR0003_11_VAL --> TFR0003_12_TEST

  class TFR0000_01_TEST,TFR0000_01_DEV,TFR0000_01_VAL triadDone
  class TFR0003_01_TEST,TFR0003_01_DEV,TFR0003_01_VAL triadDone
  class TFR0003_02_TEST,TFR0003_02_DEV,TFR0003_02_VAL triadDone
  class TFR0003_13_TEST,TFR0003_13_DEV,TFR0003_13_VAL triadDone
  class TFR0003_04_TEST,TFR0003_04_DEV,TFR0003_04_VAL triadDone
  class TFR0003_05_TEST,TFR0003_05_DEV,TFR0003_05_VAL triadDone
  class TFR0003_07_TEST,TFR0003_07_DEV,TFR0003_07_VAL triadDone
  class TFR0003_10_TEST,TFR0003_10_DEV,TFR0003_10_VAL triadDone
  class TFR0003_03_TEST,TFR0003_03_DEV,TFR0003_03_VAL triadDone
  class TFR0003_06_TEST,TFR0003_06_DEV,TFR0003_06_VAL triadDone
  class TFR0003_09_TEST,TFR0003_09_DEV,TFR0003_09_VAL triadDone
  class TFR0003_08_TEST,TFR0003_08_DEV,TFR0003_08_VAL triadDone
  class TFR0003_11_TEST,TFR0003_11_DEV,TFR0003_11_VAL triadDone
  class TFR0003_12_TEST,TFR0003_12_DEV,TFR0003_12_VAL triadDone

  classDef triadDone fill:#2e7d32,color:#fff
```

When ticket **`T-FR-NNNN-xx`** is fully complete (TEST/DEV/VAL all `done` in **`ticket-progress.md`**), add:

`class TFRNNNN_xx_TEST,TFRNNNN_xx_DEV,TFRNNNN_xx_VAL triadDone`

(Example for `T-FR-0000-01`: `class TFR0000_01_TEST,TFR0000_01_DEV,TFR0000_01_VAL triadDone`.)
