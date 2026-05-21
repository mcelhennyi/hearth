# FR-0005 — Remote build, Pi deploy (no on-device PWA build)

**Status:** `design`  
**Canonical tickets:** [`tickets.md`](tickets.md)  
**DAG draft:** [`20-tickets-dag.md`](20-tickets-dag.md)

## One-screen summary

Operators develop on a **Mac** (fast `npm`/Docker) and run Hearth on a **Raspberry Pi** (slow ARM builds). This feature adds a documented **remote-build profile**: build the Mantle PWA (and optionally hub images) on the Mac, **publish** artifacts to the Pi over SSH, and run **`docker compose up`** on the Pi **without** `npm ci` / `vite build` or local `docker compose build` for routine UI updates.

**Builds on:** FR-0002 (`hearth pwa build`), FR-0003 (Docker profile, `hearth` CLI, `SETUP.md`).

**Home Pi (operator LAN):** `192.168.1.62` — see [`00-intake.md`](00-intake.md).

## Artifact index

| File | Role |
|------|------|
| [`00-intake.md`](00-intake.md) | Goals, constraints, Pi address, raw request |
| [`10-design-00-skeleton.md`](10-design-00-skeleton.md) | L0 contracts (`hearth pwa publish`, optional image bundle) |
| [`20-tickets-dag.md`](20-tickets-dag.md) | Ticket table + Mermaid DAG |
| [`tickets.md`](tickets.md) | Canonical **`### T-FR-0005-xx`** sections |
| [`serial-diary.md`](serial-diary.md) | Serial session log |
