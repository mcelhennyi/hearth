# Next-step handoff — parallel frontier (2026-05-11)

**Audience:** Next agent or maintainer.  
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md`, `tasks/feature-history/REGISTRY.md`.

**Integration drift:** If **`feat/FR-0003-hearth-pi-docker-cli`** ticket PRs merged on GitHub but **`main`** was not updated, **`ticket-progress`** and **`triadDone`** here may lag — **`git pull`** / merge integration branches and **re-run `/identify-frontier`**.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (workspace checkout) |
|------|----------------------------|
| **Active ticket** | FR-0003 batch emphasis **`T-FR-0003-01`**; FR-0002 **`T-FR-0002-01`** / **`T-FR-0002-02`** |
| **Active phase** | Per-stream TEST → DEV → VAL in listed worktrees |
| **Branch / worktree** | FR-0002: `.worktrees/FR-0002-iphone-pwa-prototype/…`; FR-0003: `.worktrees/FR-0003-hearth-pi-docker-cli/feature/` + **`T-FR-0003-01-deployment-docker-pi`** ticket path |
| **Session status** | `developing` |
| **Next agent should** | FR-0002 HOWTO + **`/finish-feature`** when closing prototype; FR-0003 parallel streams per [`REGISTRY.md`](../feature-history/REGISTRY.md) (**`in-progress`**). FR-0001 parked. |

**Triad-complete (summary):** **`T-FR-0000-01`** only — [`docs/design/tickets-initial.md`](../../docs/design/tickets-initial.md) in this workspace lists **`TFR0000_01_*`** **`triadDone`** only.

**Still incomplete:** All other Progress rows with any phase not **`done`** (including **`T-FR-0003-01`** as **`—`** locally unless merged).

---

## Snapshot: dependency-eligible ∩ incomplete (global)

**Rule:** Ticket **B** is **eligible** when every id in **B**’s **`Deps:`** has **VAL** = **`done`** in **`ticket-progress.md`**. **Parallel-capable** = **eligible** and not triad-complete.

With only **`T-FR-0000-01`** VAL-complete as a dependency target, tickets with **`Deps: none`** are eligible:

| Ticket | Title | FR | Notes |
|--------|-------|-----|--------|
| [T-FR-0002-01](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md#t-fr-0002-01--caddy--tls-internal--static-placeholder) | Caddy + tls internal + static placeholder | FR-0002 | Incomplete (VAL open) |
| [T-FR-0002-02](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md#t-fr-0002-02--mantle-pwa-bones-manifest--sw--bottom-tab-placeholder) | Mantle PWA bones | FR-0002 | Incomplete |
| [T-FR-0003-01](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-01--design-contract-amend-deployment-for-docker-on-pi) | Design contract: amend deployment for Docker-on-Pi | FR-0003 | Incomplete on **`main`**; may already be done on **`feat/*`** PR branch |
| [T-FR-0001-01](../feature-history/FR-0001-hearth-platform/tickets.md#t-fr-0001-01--repo-scaffold-and-dev-loop) | Repo scaffold and Compose dev loop | FR-0001 | **Parked** — out of scope until registry flips |

**Practical parallel width (DAG + policy):** up to **three** streams — **FR-0002** **-01**, **-02**, **FR-0003** **-01** — when staffed.

---

## FR-0003 — next wave after **`T-FR-0003-01` VAL**

When **`T-FR-0003-01`** is VAL **`done`** on **`ticket-progress.md`**:

| Ticket | Title | Deps |
|--------|-------|------|
| [T-FR-0003-02](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-02--install-layout-heart-versionjson-readme) | Install layout: `heart/`, VERSION.json, README | **T-FR-0003-01** |
| [T-FR-0003-13](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-13--project-rules-hearth-cli-parity-cursor--claude) | Project rules: Hearth CLI parity | **T-FR-0003-01** |

After **`T-FR-0003-02`** VAL **`done`**, batch **T-FR-0003-04**, **-05**, **-10** (each needs **-01** + **-02** VAL).

**Blocked until deps advance**

- **T-FR-0003-03** — needs **T-FR-0003-02** and **T-FR-0003-05** VAL.
- **T-FR-0002-03** — needs **T-FR-0002-01** and **T-FR-0002-02** VAL.

---

## Process note (queue vs graph)

[`tasks/ticket-progress.md`](../ticket-progress.md) **Parallel streams** may mix **FR-0002** and **FR-0003** — no cross-feature **Deps** between them (`docs/ai-context.md`, parallel streams across features).

---

## Cross-cutting work

- Keep **`triadDone`** in [`docs/design/tickets-initial.md`](../../docs/design/tickets-initial.md) aligned with **`ticket-progress`** VAL **`done`** rows after merges.
- Repo-root **`CURRENT.md`** on active **`feat/*`** branches.

---

## First concrete steps

1. **Merge / integrate** open **`feat/FR-0003-hearth-pi-docker-cli`** PRs so **`T-FR-0003-01`** row and **`TFR0003_01_*`** styling match reality.
2. **`/develop-frontier 0003`** or single ticket worktrees for **T-FR-0003-02** + **T-FR-0003-13** once **-01** is VAL-complete on **`main`**.
3. Re-run **`/identify-frontier`** after integration.

---

## Related files

- [`tasks/ticket-progress.md`](../ticket-progress.md)
- [`tasks/handoffs/2026-05-10-parallel-frontier-b.md`](2026-05-10-parallel-frontier-b.md)
- [`docs/design/tickets-initial.md`](../../docs/design/tickets-initial.md)
