# Next-step handoff — parallel frontier (2026-05-10)

**Audience:** Next agent or maintainer picking up work from `main` or **`feat/*`** integration branches.  
**Focus requested:** **FR-0003** (global eligibility still computed across features per `docs/ai-context.md`, parallel streams across features).  
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md` (DAG), `docs/ai-context.md`.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | `T-FR-0002-02` (primary); `T-FR-0002-01` — server-first VAL still open |
| **Active phase** | FR-0002: `T-FR-0002-02` TEST → DEV → VAL; confirm `T-FR-0002-01` VAL in `serial-diary.md` |
| **Branch / worktree** | FR-0002 feature + ticket worktrees under `.worktrees/FR-0002-iphone-pwa-prototype/`. FR-0003: **`feat/FR-0003-hearth-pi-docker-cli`** (see repo-root `CURRENT.md` on that branch). |
| **Session status** | `developing` |
| **Next agent should** | Per `ticket-progress.md`: FR-0002 closeout via HOWTO when ready; FR-0003 start **`T-FR-0003-01`** on a ticket branch + worktree; FR-0001 remains parked unless registry policy changes. |

**Triad-complete (summary):** **`T-FR-0000-01`** only (`triadDone` in `docs/design/tickets-initial.md`).

**Still incomplete (summary):** All other tracked **`T-FR-NNNN-xx`** rows with any phase not `done`.

---

## FR-0003 — dependency-eligible + incomplete (parallel-capable today)

**Eligibility rule:** Every ticket in **`Deps:`** has **VAL** = `done` in `tasks/ticket-progress.md`.

No **`T-FR-0003-xx`** has **VAL** = `done` yet. With **no** FR-0003 predecessors VAL-complete, only tickets whose **`Deps:`** are empty qualify:

| Ticket | Title | Deps |
|--------|-------|------|
| [T-FR-0003-01](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-01--design-contract-amend-deployment-for-docker-on-pi) | Design contract: amend deployment for Docker-on-Pi | `none` |

So for **FR-0003**, **one** dependency-valid stream exists today: **`feat/FR-0003-hearth-pi-docker-cli/T-FR-0003-01-…`** under **`.worktrees/FR-0003-hearth-pi-docker-cli/<slug>/`**.

**Unlocks after `T-FR-0003-01` is VAL-done:**

- [T-FR-0003-02](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-02--install-layout-heart-versionjson-readme) — Install layout (`Deps:` **T-FR-0003-01**)
- [T-FR-0003-13](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-13--project-rules-hearth-cli-parity-cursor--claude) — Project rules: Hearth CLI parity (`Deps:` **T-FR-0003-01** only)

After **`T-FR-0003-02`** is VAL-done, the DAG allows **four** parallel streams (**T-FR-0003-04**, **-05**, **-10**, plus any worker finishing **-13** if **-01** already VAL-done): **-04**, **-05**, **-10** each require **-01** and **-02** VAL; **-13** requires **-01** VAL only — so once **-01** is VAL-done, **-13** can run in parallel with **-02** TEST/DEV/VAL.

**Examples of FR-0003 tickets blocked until more VAL-done rows exist:**

- **T-FR-0003-03** — needs **T-FR-0003-02** and **T-FR-0003-05** VAL-done (bootstrap after layout + compose generation exist).
- **T-FR-0003-06**, **-07**, **-09** — need **T-FR-0003-04** and **T-FR-0003-05** VAL-done.
- **T-FR-0003-08** — needs **T-FR-0003-07** VAL-done.
- **T-FR-0003-11** — needs **T-FR-0003-07** and **T-FR-0003-10** VAL-done.
- **T-FR-0003-12** — capstone; needs **-03**, **-06**, **-08**, **-09**, **-11** VAL-done.

Full **Deps:** edges: `tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`; global mermaid: `docs/design/tickets-initial.md`.

---

## Snapshot: global dependency-eligible + incomplete (other features)

Same eligibility rule across **`tasks/feature-history/**/tickets.md`**.

| Ticket | Title | FR | Deps satisfied? |
|--------|-------|-----|-----------------|
| [T-FR-0002-01](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md#t-fr-0002-01--caddy--tls-internal--static-placeholder) | Caddy + tls internal + static placeholder | FR-0002 | `none` — **eligible** (VAL not done) |
| [T-FR-0002-02](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md#t-fr-0002-02--mantle-pwa-bones-manifest--sw--bottom-tab-placeholder) | Mantle PWA bones | FR-0002 | `none` — **eligible** |
| [T-FR-0003-01](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-01--design-contract-amend-deployment-for-docker-on-pi) | Design contract: amend deployment for Docker-on-Pi | FR-0003 | `none` — **eligible** |
| [T-FR-0001-01](../feature-history/FR-0001-hearth-platform/tickets.md#t-fr-0001-01--repo-scaffold-and-dev-loop) | Repo scaffold and Compose dev loop | FR-0001 | `none` — **eligible** by graph |

**Policy note:** **FR-0001** is **parked** in [`REGISTRY.md`](../feature-history/REGISTRY.md); treat **`T-FR-0001-xx`** as **out of scope** for implementation until registry/ticket-progress policy flips, even though **`Deps:`** would allow **`T-FR-0001-01`**.

So **up to three parallel DAG-valid streams** are typical today (**FR-0002** **-01**, **-02**, **FR-0003** **-01**), plus **FR-0001-01** only if parking is lifted.

---

## Process note (queue vs graph)

The **Progress** table and **Current focus** row describe human priority (FR-0002 prototype **HOWTO**, FR-0003 unparked). The **parallel-capable set** is purely **`Deps:`** + **VAL** columns — it may recommend starting **FR-0003** **`-01`** while **FR-0002** tickets remain incomplete; that is intentional parallel capacity (`docs/ai-context.md`, parallel streams).

---

## Cross-cutting work (parallel to tickets)

- **`triadDone`** lines in `docs/design/tickets-initial.md` — add when a ticket’s TEST/DEV/VAL are all **`done`** in `ticket-progress.md`.
- Repo-root **`CURRENT.md`** on **`feat/FR-0003-hearth-pi-docker-cli`** — keep aligned with this frontier (updated in same change series as this handoff).

---

## First concrete steps (FR-0003 primary)

1. From **`main`** or **`feat/FR-0003-hearth-pi-docker-cli`**, create **`feat/FR-0003-hearth-pi-docker-cli/T-FR-0003-01-<short-name>`** and worktree **`.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-01-…/`**.
2. Run **TEST → DEV → VAL** for **[T-FR-0003-01](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-01--design-contract-amend-deployment-for-docker-on-pi)** — amend **`docs/design/deployment.md`** with the Docker-on-Pi profile; use **`./develop build`** or **`./develop up`** for doc **VAL** if `docs/` changes.
3. On VAL-done: update **`tasks/ticket-progress.md`**, add **`triadDone`** class line in **`docs/design/tickets-initial.md`** for **`TFR0003_01_*`**, merge ticket branch → **`feat/FR-0003-hearth-pi-docker-cli`**, then re-run **`/identify-frontier`** to pick up **T-FR-0003-02** + **T-FR-0003-13** (and later the wide batch after **-02**).
4. Refresh repo-root **`CURRENT.md`** on **`feat/FR-0003-hearth-pi-docker-cli`** after each merge or frontier change.

---

## Related files

- [`tasks/ticket-progress.md`](../ticket-progress.md)
- [`tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md)
- [`tasks/feature-history/TICKET-SOURCES.md`](../feature-history/TICKET-SOURCES.md)
- [`docs/design/tickets-initial.md`](../../docs/design/tickets-initial.md)
