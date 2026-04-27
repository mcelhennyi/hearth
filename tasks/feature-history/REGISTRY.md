# Feature request registry (`FR-NNNN`)

**Rules:** Four-digit zero-padded ids. **Never** reuse an **`FR-NNNN`** for a different feature. Increment **`next_id`** when allocating a new number.

**Parallel features:** Multiple rows may be **`design`** or **`in-progress`** at the same time. Each row points at a **distinct** directory **`tasks/feature-history/FR-NNNN-<slug>/`**.

| FR id | Slug (directory) | Status | Tickets (when known) | Notes |
|-------|------------------|--------|------------------------|-------|
| FR-0000 | `FR-0000-bootstrap/` | `active` | **`T-FR-0000-01`** in [`FR-0000-bootstrap/tickets.md`](FR-0000-bootstrap/tickets.md) | Core / repo bootstrap. |
| FR-0001 | `FR-0001-hearth-platform/` | `design` | **`T-FR-0001-01`** … **`T-FR-0001-08`** in [`FR-0001-hearth-platform/tickets.md`](FR-0001-hearth-platform/tickets.md) | MVP platform: hub gateway, plugin loader, Mantle shell, Spark API, Tinder manifest, deploy story. Satellite repos: **Kindling** (templates), **Ember** (relay, Phase 2). |

**next_id:** `2`

**Allocating a new `FR-NNNN`:** Create directory **`tasks/feature-history/FR-NNNN-<slug>/`**, add a row to the table, set **`next_id`** to **NNNN+1**, and add the ticket file path to **`TICKET-SOURCES.md`**.
