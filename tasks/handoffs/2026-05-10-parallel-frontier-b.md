# Next-step handoff — parallel frontier (2026-05-10, refresh **b**)

**Audience:** Next agent or maintainer.  
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md`, `tasks/feature-history/REGISTRY.md`.

**Workspace note:** This snapshot uses **`tasks/ticket-progress.md` on the current checkout** (`main`, aligned with `origin/main` when last refreshed). If **`feat/*`** PRs merged remotely but are not merged locally, **`git pull`** / merge integration branches and **re-run `/identify-frontier`** — **`triadDone`** lines in `docs/design/tickets-initial.md` should then match **`ticket-progress`** VAL rows.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | `T-FR-0002-02` (primary); `T-FR-0002-01` — merge ticket branch into feature branch when ready |
| **Active phase** | `T-FR-0002-02` TEST → DEV → VAL; `T-FR-0002-01` server-first VAL still open |
| **Branch / worktree** | `.worktrees/FR-0002-iphone-pwa-prototype/` feature + ticket worktrees (see tracker **Parallel streams**) |
| **Session status** | `developing` |
| **Next agent should** | FR-0002 closeout per [`HOWTO-complete-FR-0002.md`](../feature-history/FR-0002-iphone-pwa-prototype/HOWTO-complete-FR-0002.md); parallel ticket work per frontier below. **`T-FR-0001-xx`** remains **parked** ([`REGISTRY.md`](../feature-history/REGISTRY.md)). |

**Triad-complete (summary):** **`T-FR-0000-01`** only — matches **`triadDone`** in [`docs/design/tickets-initial.md`](../../docs/design/tickets-initial.md) (workspace copy).

**Still incomplete:** All other rows in the Progress table with any phase not **`done`**.

---

## Snapshot: dependency graph — eligible ∩ incomplete

**Eligibility:** Every ticket listed under **`Deps:`** in the owning **`tickets.md`** has **VAL** = **`done`** in **`ticket-progress.md`**.

With **only `T-FR-0000-01`** VAL-complete among dependencies, any ticket whose **`Deps:`** is **`none`** is **eligible**. Among those, **incomplete** rows are parallel-capable **by DAG**:

| Ticket | Title | FR | Deps |
|--------|-------|-----|------|
| [T-FR-0002-01](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md#t-fr-0002-01--caddy--tls-internal--static-placeholder) | Caddy + tls internal + static placeholder | FR-0002 | `none` |
| [T-FR-0002-02](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md#t-fr-0002-02--mantle-pwa-bones-manifest--sw--bottom-tab-placeholder) | Mantle PWA bones | FR-0002 | `none` |
| [T-FR-0003-01](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-01--design-contract-amend-deployment-for-docker-on-pi) | Design contract: amend deployment for Docker-on-Pi | FR-0003 | `none` |
| [T-FR-0001-01](../feature-history/FR-0001-hearth-platform/tickets.md#t-fr-0001-01--repo-scaffold-and-dev-loop) | Repo scaffold and Compose dev loop | FR-0001 | `none` *(parked — see below)* |

So **up to three** practical parallel streams (**FR-0002** **-01**, **-02**, **FR-0003** **-01**) if policy allows FR-0003 work; **four** if FR-0001 parking is lifted.

### Registry / tracker policy vs DAG

- **[`REGISTRY.md`](../feature-history/REGISTRY.md):** **FR-0003** is **`parked`** (“implementation deferred until FR-0002 closes”).
- **`ticket-progress.md` → How to choose #2:** Do **not** start **`T-FR-0003-xx`** while FR-0002 is in flight.

**Recommendation:** Treat **`T-FR-0003-01`** as **DAG-eligible but policy-deferred** until **FR-0003** is **`in-progress`** in the registry and the “park until FR-0002” lines are superseded. **Do not** ignore **`REGISTRY.md`** without an explicit policy amend.

### Examples blocked until more VAL-done rows

- **[T-FR-0002-03](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md)** — needs **`T-FR-0002-01`** and **`T-FR-0002-02`** VAL-done (both still open in tracker).
- **[T-FR-0003-02](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md)** — needs **`T-FR-0003-01`** VAL-done.
- **[T-FR-0003-03](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md)** — needs **`T-FR-0003-02`** and **`T-FR-0003-05`** VAL-done.

Full edges: per-feature **`tickets.md`**; global mermaid: [`docs/design/tickets-initial.md`](../../docs/design/tickets-initial.md).

---

## Process note (queue vs graph)

Human priority (HOWTO, merge queue) may emphasize **FR-0002** before **FR-0003**. The **parallel-capable** set is still computed **globally** from **`Deps:`** + VAL (`docs/ai-context.md`, parallel streams across features).

---

## Cross-cutting work

- After merges from **`feat/*`**, reconcile **`tasks/ticket-progress.md`** with **`triadDone`** unions in **`docs/design/tickets-initial.md`**.
- Repo-root **`CURRENT.md`** on active **`feat/FR-NNNN-<slug>`** and ticket branches per **feature-request** skill.

---

## First concrete steps

1. **FR-0002:** Finish **[T-FR-0002-01](VAL)** (server-first Pi/Mac mini) and/or complete **[T-FR-0002-02](TEST→VAL)** in the listed worktrees; merge ticket branches → **`feat/FR-0002-iphone-pwa-prototype`**.
2. **FR-0003:** If policy allows, unpark **FR-0003** in **`REGISTRY.md`** and align **`ticket-progress.md` “How to choose”** — then implement **[T-FR-0003-01](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md)** on **`feat/FR-0003-hearth-pi-docker-cli`**.
3. When **`T-FR-0002-01`** and **`T-FR-0002-02`** are both VAL-done, **[T-FR-0002-03](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md)** becomes eligible — run **`/identify-frontier`** again.

---

## Related files

- [`tasks/ticket-progress.md`](../ticket-progress.md)
- [`tasks/feature-history/TICKET-SOURCES.md`](../feature-history/TICKET-SOURCES.md)
- [`docs/design/tickets-initial.md`](../../docs/design/tickets-initial.md)
- Prior snapshot: [`2026-05-10-parallel-frontier.md`](2026-05-10-parallel-frontier.md)
