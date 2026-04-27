# Ticket progress

## Current focus

| Field | Value |
|-------|--------|
| **Active ticket** | `T-FR-0001-01` (eligible; not yet started) |
| **Active phase** | — |
| **Branch / worktree** | — (next worker creates `feat/FR-0001-hearth-platform/T-FR-0001-01-repo-scaffold` under `.worktrees/FR-0001-hearth-platform/T-FR-0001-01-repo-scaffold/`) |
| **Session status** | `planning` |
| **Next agent should** | Read `docs/design/architecture/overview.md`, `docs/design/deployment.md`, and `tasks/feature-history/FR-0001-hearth-platform/tickets.md`. Start `T-FR-0001-01` (TEST → DEV → VAL): scaffold repo + Compose dev loop; smoke test serves `https://hearth.local/` over local TLS. |

### Parallel streams (optional)

Use when **more than one** ticket id or **`FR-NNNN`** is actively developed in parallel. Each stream: own `.worktrees/FR-NNNN-<slug>/...` worktree and feature-prefixed branch; update **only** your **Progress** row for your ticket.

| Stream label | Ticket(s) | `FR-NNNN` (if any) | Branch / worktree | Owner / note |
|----------------|------------|--------------------|-------------------|--------------|
| *(none — single stream)* | — | — | — | — |

After `T-FR-0001-01` lands, the next frontier batch (`T-FR-0001-02`, `T-FR-0001-04`, `T-FR-0001-05` partial) is parallel-capable. Use `/identify-frontier` then `/develop-frontier`.

---

## Progress

| Ticket | Title | TEST | DEV | VAL | Notes |
|--------|-------|------|-----|-----|-------|
| T-FR-0000-01 | Choose stack and scaffold repository | done | done | done | Stack chosen and scaffold deferred to `T-FR-0001-01` (which carries the actual scaffold). FR-0000 tooling/process scaffold complete via `init-skeleton`. |
| T-FR-0001-01 | Repo scaffold and Compose dev loop | — | — | — | `FR-0001` |
| T-FR-0001-02 | Hub API skeleton and SQLite registry | — | — | — | `FR-0001` |
| T-FR-0001-03 | Tinder loader and manifest schema | — | — | — | `FR-0001` |
| T-FR-0001-04 | Mantle PWA shell and iframe embed | — | — | — | `FR-0001` |
| T-FR-0001-05 | Caddy generation and local TLS | — | — | — | `FR-0001` |
| T-FR-0001-06 | Spark v1 broker and client libs | — | — | — | `FR-0001` |
| T-FR-0001-07 | Kindling repo and CLI | — | — | — | `FR-0001` |
| T-FR-0001-08 | groceries reference plugin | — | — | — | `FR-0001` |
| T-FR-0001-09 | Auth, VAPID, Web Push + ntfy | — | — | — | `FR-0001` |
| T-FR-0001-10 | Pi/Mac mini install.sh + backup | — | — | — | `FR-0001` (closeout) |

---

## How to choose next work

1. Prefer the **smallest incomplete ticket** whose **Deps** are all **VAL** = `done`.
2. If **Session status** is `blocked`, resolve the blocker before starting new parallel batches.
3. The DAG (`tasks/feature-history/FR-0001-hearth-platform/20-tickets-dag.md`) lists frontier batches — once the prerequisite triad turns green, the next batch can run in parallel via `/develop-frontier`.
