# Parallel frontier — 2026-05-09 (refreshed for `/develop-frontier`)

## Eligible tickets (incomplete ∩ deps satisfied)

| Ticket | Title | `FR` | Notes |
|--------|-------|------|--------|
| [T-FR-0002-01](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md#t-fr-0002-01--caddy--tls-internal--static-placeholder) | Caddy + `tls internal` + static placeholder | FR-0002 | Deps: none |
| [T-FR-0002-02](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md#t-fr-0002-02--mantle-pwa-bones-manifest--sw--bottom-tab-placeholder) | Mantle PWA bones (manifest + SW + nav) | FR-0002 | Deps: none |

## Explicitly excluded

- **All `T-FR-0003-xx`** — [FR-0003 parked](../feature-history/REGISTRY.md) until FR-0002 closes (operator option A).
- **`T-FR-0001-xx`** — FR-0001 parked.

## Worktrees (this repo)

Stale `project_04` worktree registrations were **pruned**; checkouts recreated under **`hearth/.worktrees/`** (gitignored):

| Role | Path | Branch |
|------|------|--------|
| Feature integration | `.worktrees/FR-0002-iphone-pwa-prototype/feature/` | `feat/FR-0002-iphone-pwa-prototype` |
| Ticket T-01 | `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls/` | `feat/FR-0002-iphone-pwa-prototype-T-FR-0002-01-caddy-tls` |
| Ticket T-02 | `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones/` | `feat/FR-0002-iphone-pwa-prototype-T-FR-0002-02-mantle-bones` |

Absolute prefix: **`/Users/ianmcelhenny/projects/hearth/`** (adjust on other machines).

## Orchestrator note

Run **TEST → DEV → VAL** per ticket in **only** that ticket’s worktree; use **`./develop`** / Docker Compose for verification; update **`tasks/ticket-progress.md`** for the ticket row only; on VAL done, add **`triadDone`** in **`docs/design/tickets-initial.md`**, push branch, open PR **into** **`feat/FR-0002-iphone-pwa-prototype`** (not `main`).
