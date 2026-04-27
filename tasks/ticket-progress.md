# Ticket progress

## Current focus

| Field | Value |
|-------|--------|
| **Active ticket** | `T-FR-0002-01` and `T-FR-0002-02` (parallel-eligible; not yet started) |
| **Active phase** | — |
| **Branch / worktree** | — (next worker: `feat/FR-0002-iphone-pwa-prototype` at `.worktrees/FR-0002-iphone-pwa-prototype/feature/`, then per-ticket child branches) |
| **Session status** | `handoff` |
| **Next agent should** | Read [`tasks/feature-history/FR-0002-iphone-pwa-prototype/handoffs/2026-04-27-continue.md`](feature-history/FR-0002-iphone-pwa-prototype/handoffs/2026-04-27-continue.md) **first**. Then `README.md` + `10-design/risks.md` + `tickets.md` for FR-0002. Start `T-FR-0002-01` and `T-FR-0002-02` in parallel via `/identify-frontier` → `/develop-frontier` (or serially if a single worker). FR-0001 is `parked`; do not start FR-0001 tickets until FR-0002 closes. |

### Parallel streams

`T-FR-0002-01` and `T-FR-0002-02` are independent and can run in parallel — one builds the proxy + TLS, the other builds the static Mantle shell. Both must land before `T-FR-0002-03` (Web Push needs the SW reachable over `https://`).

| Stream label | Ticket(s) | `FR-NNNN` | Branch / worktree | Owner / note |
|----------------|------------|-----------|-------------------|--------------|
| caddy-tls | `T-FR-0002-01` | `FR-0002` | `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls` at `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-01-caddy-tls/` | unassigned |
| mantle-bones | `T-FR-0002-02` | `FR-0002` | `feat/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones` at `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones/` | unassigned |

---

## Progress

| Ticket | Title | TEST | DEV | VAL | Notes |
|--------|-------|------|-----|-----|-------|
| T-FR-0000-01 | Choose stack and scaffold repository | done | done | done | Stack chosen; FR-0000 tooling/process scaffold complete via `init-skeleton`. Implementation scaffold lives in `T-FR-0001-01` (parked). |
| T-FR-0002-01 | Caddy + tls internal + static placeholder | — | — | — | `FR-0002`. Reuses into `T-FR-0001-05`. |
| T-FR-0002-02 | Mantle PWA bones (manifest + SW + nav) | done | done | done | `FR-0002`. Reuses into `T-FR-0001-04`. Implemented at `apps/hub/web` with Vite+TS+Tailwind+Vite-PWA, responsive nav shell, and Vitest coverage for breakpoint/SW. |
| T-FR-0002-03 | Web Push round-trip (VAPID + subscribe + send) | — | — | — | `FR-0002`. Reuses into `T-FR-0001-09`. Deps: `T-FR-0002-01`, `T-FR-0002-02`. |
| T-FR-0002-04 | Real-iPhone walkthrough + closeout report | — | — | — | `FR-0002`. No FR-0001 reuse target. Deps: `T-FR-0002-01..03`. |
| T-FR-0001-01 | Repo scaffold and Compose dev loop | — | — | — | `FR-0001` parked — eligible after FR-0002 closes. |
| T-FR-0001-02 | Hub API skeleton and SQLite registry | — | — | — | `FR-0001` parked. |
| T-FR-0001-03 | Tinder loader and manifest schema | — | — | — | `FR-0001` parked. |
| T-FR-0001-04 | Mantle PWA shell and iframe embed | — | — | — | `FR-0001` parked. Will reuse `T-FR-0002-02` output. |
| T-FR-0001-05 | Caddy generation and local TLS | — | — | — | `FR-0001` parked. Will reuse `T-FR-0002-01` output. |
| T-FR-0001-06 | Spark v1 broker and client libs | — | — | — | `FR-0001` parked. |
| T-FR-0001-07 | Kindling repo and CLI | — | — | — | `FR-0001` parked. |
| T-FR-0001-08 | groceries reference plugin | — | — | — | `FR-0001` parked. |
| T-FR-0001-09 | Auth, VAPID, Web Push + ntfy | — | — | — | `FR-0001` parked. Will reuse `T-FR-0002-03` output. |
| T-FR-0001-10 | Pi/Mac mini install.sh + backup | — | — | — | `FR-0001` parked (closeout). |

---

## How to choose next work

1. While FR-0002 is `in-progress`: pick the smallest **`T-FR-0002-xx`** with all `Deps:` satisfied. Ignore FR-0001 tickets — they are parked.
2. After FR-0002 closes: re-flip FR-0001 to `design`/`in-progress` in `REGISTRY.md`, apply any FR-0002-driven amendments, and start `T-FR-0001-01`.
3. If **Session status** is `blocked`, resolve the blocker before starting new parallel batches.
