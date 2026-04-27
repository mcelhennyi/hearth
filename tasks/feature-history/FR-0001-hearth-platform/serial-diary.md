# FR-0001 — serial diary

Append-only. Newest entries at the top of each session block.

---

## 2026-04-27 — `design`

- Allocated **`FR-0001`** in `REGISTRY.md`; `next_id` → `2`.
- Named the platform **Hearth**; companion names: **Mantle** (UI shell), **Spark** (app-to-app API), **Tinder** (plugin manifest), **Kindling** (templates repo), **Ember** (Phase-2 relay).
- Wrote charter, system architecture, plugin contract, Spark API, Mantle UI, deployment, and Kindling design docs.
- Resolved Q1 (iframe), Q2 (Unix sockets), Q3 (git-submodule plugins), Q5 (`/` is hub) for MVP. Q4 (auth default) left open pending stakeholder input.
- Drafted **`T-FR-0001-01`** … **`T-FR-0001-08`** in `tickets.md` and global DAG in `20-tickets-dag.md`.
- Sketched **Ember** as a separate FR placeholder (`docs/design/satellite-repos/ember.md`); intentionally not yet allocated an `FR-NNNN`.
- Branch / worktree: none yet — work continues on `main` until `T-FR-0001-01` opens `feat/FR-0001-hearth-platform`.
