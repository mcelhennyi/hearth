# Feature request registry (`FR-NNNN`)

**Rules:** Four-digit zero-padded ids. **Never** reuse an **`FR-NNNN`** for a different feature. Increment **`next_id`** when allocating a new number.

**Parallel features:** Multiple rows may be **`design`** or **`in-progress`** at the same time. Each row points at a **distinct** directory **`tasks/feature-history/FR-NNNN-<slug>/`**.

| FR id | Slug (directory) | Status | Tickets (when known) | Notes |
|-------|------------------|--------|------------------------|-------|
| FR-0000 | `FR-0000-bootstrap/` | `active` | **`T-FR-0000-01`** in [`FR-0000-bootstrap/tickets.md`](FR-0000-bootstrap/tickets.md) | Core / repo bootstrap. |
| FR-0001 | `FR-0001-hearth-platform/` | `parked` | **`T-FR-0001-01`** … **`T-FR-0001-10`** in [`FR-0001-hearth-platform/tickets.md`](FR-0001-hearth-platform/tickets.md) | MVP platform. **Parked pending FR-0002 prototype findings** — design stays authoritative; implementation order may be revised by what FR-0002 learns about Caddy + iPhone PWA + Web Push. |
| FR-0002 | `FR-0002-iphone-pwa-prototype/` | `closeout` | **`T-FR-0002-01`** … **`T-FR-0002-04`** in [`FR-0002-iphone-pwa-prototype/tickets.md`](FR-0002-iphone-pwa-prototype/tickets.md) | PWA prototype validated on Pi + iPhone (TLS + push). Feature PR → **`main`** pending. Operator guide: **`SETUP.md`**. Report: [`40-prototype-report.md`](FR-0002-iphone-pwa-prototype/40-prototype-report.md). |
| FR-0003 | `FR-0003-hearth-pi-docker-cli/` | `done` | **`T-FR-0003-01`** … **`T-FR-0003-13`** in [`FR-0003-hearth-pi-docker-cli/tickets.md`](FR-0003-hearth-pi-docker-cli/tickets.md) | **Merged to `main`** via [**PR #13**](https://github.com/mcelhennyi/hearth/pull/13) (2026-05-18). Docker Compose Pi install, `./install`, `hearth` + per-plugin `plugin` CLI. Closeout: [`FR-0003-hearth-pi-docker-cli/90-closeout.md`](FR-0003-hearth-pi-docker-cli/90-closeout.md). Operator guide: **`SETUP.md`**. |
| FR-0004 | `FR-0004-centralized-users-auth/` | `parked` | **`T-FR-0004-01`** … **`T-FR-0004-10`** in [`FR-0004-centralized-users-auth/tickets.md`](FR-0004-centralized-users-auth/tickets.md) | Built-in **`hearth-users`** + gateway auth. **Parked** until **FR-0002** Pi CA/certificate VAL (**`T-FR-0002-01`**, closeout **`T-FR-0002-04`**) and **FR-0001** initial Mantle UI (**`T-FR-0001-04`** VAL). Design: **`T-FR-0004-01`** done in feature tree; promote `docs/design/` amendments on resume if not on `main`. |

**next_id:** `5`

**Allocating a new `FR-NNNN`:** Create directory **`tasks/feature-history/FR-NNNN-<slug>/`**, add a row to the table, set **`next_id`** to **NNNN+1**, and add the ticket file path to **`TICKET-SOURCES.md`**.
