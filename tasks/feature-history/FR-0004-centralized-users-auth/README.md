# FR-0004 — Centralized users auth (built-in plugin + gateway)

**Status:** `done`
**Allocated:** 2026-05-17
**Registry:** [`REGISTRY.md`](../REGISTRY.md)

## Resume status

Implementation is feature-complete on **`feat/FR-0004-centralized-users-auth`** as of 2026-05-26. [**PR #56**](https://github.com/mcelhennyi/hearth/pull/56) to **`main`** is pending. Closeout: [`90-closeout.md`](90-closeout.md).

| Gate | Feature | Ticket(s) | What “done” means |
|------|---------|-----------|-------------------|
| **1. Pi certificate / PWA prototype** | **FR-0002** | [**Caddy + tls internal + static placeholder**](../FR-0002-iphone-pwa-prototype/tickets.md) (`T-FR-0002-01`) **VAL** | Real Pi or Mac mini: local CA trusted on iPhone, `https://hearth.home.arpa/` loads over TLS |
| | | [**Real-iPhone walkthrough + closeout report**](../FR-0002-iphone-pwa-prototype/tickets.md) (`T-FR-0002-04`) **VAL** | FR-0002 prototype closed; cert + install path validated on device |
| **2. Initial platform UI** | **FR-0001** | [**Mantle PWA shell and iframe embed**](../FR-0001-hearth-platform/tickets.md) (`T-FR-0001-04`) **VAL** | Hub shell at `/` with Mantle chrome, plugin iframe, `useUser()` / postMessage contract (typically after reusing FR-0002 Mantle bones) |

**Design-only progress:** [**Design amendments: centralized auth architecture**](tickets.md) (`T-FR-0004-01`) — complete in feature history and refreshed by the 2026-05-26 audit. Implementation starts with the built-in provider scaffold.

## Charter (one sentence)

Move login, session, and authorization for every plugin behind a **built-in Hearth users plugin** and a **single public gateway** (Caddy → hub-or-plugin routes), so new Kindling-scaffolded apps inherit the contract by default and operators can later swap in a custom user service.

## Artifacts

| Stage | Path |
|-------|------|
| Intake | [`00-intake.md`](00-intake.md) |
| Design L0 | [`10-design-00-skeleton.md`](10-design-00-skeleton.md) |
| Design L1 | [`10-design-01-gateway-and-trust.md`](10-design-01-gateway-and-trust.md) |
| Tickets (draft DAG) | [`20-tickets-dag.md`](20-tickets-dag.md) |
| Tickets (canonical) | [`tickets.md`](tickets.md) |
| Diary | [`serial-diary.md`](serial-diary.md) |
| Closeout | [`90-closeout.md`](90-closeout.md) |

## Relationship to other FRs

| FR | Relationship |
|----|----------------|
| **FR-0001** | **Amends** MVP identity: **`T-FR-0001-09`** split (login → FR-0004; push may stay hub). **Blocked on** **`T-FR-0001-04`** before FR-0004 implementation. |
| **FR-0002** | **Blocked on** Pi CA trust + iPhone prototype closeout (**`T-FR-0002-01` VAL**, **`T-FR-0002-04` VAL**). Mantle bones feed FR-0001-04. |
| **FR-0003** | **Done** on `main` — Compose/Caddy/`hearth` CLI available for later FR-0004 proxy + settings work. |
