# Feature request registry (`FR-NNNN`)

**Rules:** Four-digit zero-padded ids. **Never** reuse an **`FR-NNNN`** for a different feature. Increment **`next_id`** when allocating a new number.

**Parallel features:** Multiple rows may be **`design`** or **`in-progress`** at the same time. Each row points at a **distinct** directory **`tasks/feature-history/FR-NNNN-<slug>/`**.

| FR id | Slug (directory) | Status | Tickets (when known) | Notes |
|-------|------------------|--------|------------------------|-------|
| FR-0000 | `FR-0000-bootstrap/` | `active` | **`T-FR-0000-01`** in [`FR-0000-bootstrap/tickets.md`](FR-0000-bootstrap/tickets.md) | Core / repo bootstrap. |
| FR-0001 | `FR-0001-hearth-platform/` | `parked` | **`T-FR-0001-01`** … **`T-FR-0001-10`** in [`FR-0001-hearth-platform/tickets.md`](FR-0001-hearth-platform/tickets.md) | MVP platform. **Parked pending FR-0002 prototype findings** — design stays authoritative; implementation order may be revised by what FR-0002 learns about Caddy + iPhone PWA + Web Push. |
| FR-0002 | `FR-0002-iphone-pwa-prototype/` | `in-progress` | **`T-FR-0002-01`** … **`T-FR-0002-04`** in [`FR-0002-iphone-pwa-prototype/tickets.md`](FR-0002-iphone-pwa-prototype/tickets.md) | Thinner-slice prototype to de-risk the "feels native on iPhone" claim before investing in registry/Tinder/Spark. Caddy + static Mantle shell + manifest + service worker + iPhone CA trust + one Web Push round-trip. |
| FR-0003 | `FR-0003-hearth-pi-docker-cli/` | `in-progress` | **`T-FR-0003-01`** … **`T-FR-0003-13`** in [`FR-0003-hearth-pi-docker-cli/tickets.md`](FR-0003-hearth-pi-docker-cli/tickets.md) | **`/develop-frontier 0003`** (operator): implementation active alongside FR-0002 when staffed — scheduling-only park superseded. Docker Compose Pi install, `./install`, `hearth` + per-plugin `plugin` CLI. Feature branch **`feat/FR-0003-hearth-pi-docker-cli`**. |

**next_id:** `4`

**Allocating a new `FR-NNNN`:** Create directory **`tasks/feature-history/FR-NNNN-<slug>/`**, add a row to the table, set **`next_id`** to **NNNN+1**, and add the ticket file path to **`TICKET-SOURCES.md`**.
