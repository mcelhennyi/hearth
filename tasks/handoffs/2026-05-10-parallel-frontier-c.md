# Next-step handoff — parallel frontier (2026-05-10, refresh c)

**Audience:** Next agent or maintainer picking up global ticket work.
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md`, `docs/ai-context.md`.

**Integration note:** The root `main` checkout still lags FR-0003 feature-branch state. This handoff reconciles the current root tracker with updated `feat/FR-0003-hearth-pi-docker-cli` state after fast-forwarding that feature worktree: **T-FR-0003-02** is VAL-done and merged via PR #9; **T-FR-0003-13** is implemented on its ticket branch with PR #8 open into the feature branch.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | FR-0003 wave after **T-FR-0003-02**; FR-0002 remains unchanged. |
| **Active phase** | Next FR-0003 implementation wave: TEST -> DEV -> VAL for **T-FR-0003-04**, **T-FR-0003-05**, **T-FR-0003-10** in separate worktrees. |
| **Branch / worktree** | Feature: `.worktrees/FR-0003-hearth-pi-docker-cli/feature/` -> `feat/FR-0003-hearth-pi-docker-cli`; ticket branches use hyphenated suffixes such as `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-04-cli-core`. |
| **Session status** | `handoff` |
| **Next agent should** | Review/merge PR #8 for **T-FR-0003-13** or leave it to human review; start the next FR-0003 wave for **-04**, **-05**, **-10** once the feature branch is current. |

**Triad-complete (summary):** `T-FR-0000-01`, `T-FR-0003-01`, and `T-FR-0003-02`.

**Still incomplete (summary):** FR-0002 `-01` VAL remains open; FR-0002 `-02` is still unstarted in the root tracker. FR-0003 `-04`, `-05`, and `-10` are now dependency-eligible. FR-0003 `-13` is dependency-eligible but already has open PR #8 rather than needing a duplicate implementation stream.

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in **Deps:** has **VAL** = `done` in `tasks/ticket-progress.md` or in the reconciled FR-0003 feature branch state noted above.

With **T-FR-0003-01** and **T-FR-0003-02** VAL-done, these tickets are eligible and mutually non-blocking:

| Ticket | Title | FR | Deps | Action |
|--------|-------|----|------|--------|
| [T-FR-0002-01](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md#t-fr-0002-01--caddy--tls-internal--static-placeholder) | Caddy + tls internal + static placeholder | FR-0002 | `none` | Finish server-first VAL if hardware is available. |
| [T-FR-0002-02](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md#t-fr-0002-02--mantle-pwa-bones-manifest--sw--bottom-tab-placeholder) | Mantle PWA bones | FR-0002 | `none` | Implement when capacity exists. |
| [T-FR-0003-04](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-04--hearth-cli-core-argparse-paths-doctor-compose-passthrough) | `hearth` CLI core: argparse, paths, doctor, compose passthrough | FR-0003 | `T-FR-0003-01`, `T-FR-0003-02` | Start new ticket worktree. |
| [T-FR-0003-05](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-05--plugin-registry-file--compose-fragment-generation) | Plugin registry file + Compose fragment generation | FR-0003 | `T-FR-0003-01`, `T-FR-0003-02` | Start new ticket worktree. |
| [T-FR-0003-10](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-10--kindling-contract-scriptsinstall--plugin-template) | Kindling contract: `scripts/install` + `plugin` template | FR-0003 | `T-FR-0003-01`, `T-FR-0003-02` | Start new ticket worktree. |
| [T-FR-0003-13](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-13--project-rules-hearth-cli-parity-cursor--claude) | Project rules: Hearth CLI parity | FR-0003 | `T-FR-0003-01` | PR #8 is open; review/merge instead of duplicating work. |
| [T-FR-0001-01](../feature-history/FR-0001-hearth-platform/tickets.md#t-fr-0001-01--repo-scaffold-and-dev-loop) | Repo scaffold and Compose dev loop | FR-0001 | `none` | Parked by registry policy until FR-0002 closes. |

So **up to five practical parallel streams** are dependency-valid if staffing allows: FR-0002 `-01`, FR-0002 `-02`, and FR-0003 `-04`, `-05`, `-10`. Treat FR-0003 `-13` as review/integration work, not a new implementation stream.

**Examples of what stays blocked until more VAL-done rows exist:**

- **T-FR-0002-03** needs **T-FR-0002-01** and **T-FR-0002-02** VAL-done.
- **T-FR-0003-03** needs **T-FR-0003-02** and **T-FR-0003-05** VAL-done.
- **T-FR-0003-06**, **T-FR-0003-07**, and **T-FR-0003-09** need both **T-FR-0003-04** and **T-FR-0003-05** VAL-done.
- **T-FR-0003-11** needs **T-FR-0003-07** and **T-FR-0003-10** VAL-done.
- **T-FR-0003-12** remains the FR-0003 closeout smoke/ARM ticket after **-03**, **-06**, **-08**, **-09**, and **-11**.

Full **Deps:** edges live in the per-feature `tickets.md` files; the global mermaid in `docs/design/tickets-initial.md` should be updated by union when ticket branches merge.

---

## Process note (queue vs graph)

The frontier is global, so FR-0002 and FR-0003 can appear together when their **Deps:** allow it. FR-0001 remains parked by registry policy even though **T-FR-0001-01** has `Deps: none`.

For FR-0003, prefer the feature-branch workflow: create each new ticket worktree under `.worktrees/FR-0003-hearth-pi-docker-cli/`, branch from `feat/FR-0003-hearth-pi-docker-cli`, open ticket PRs back into that feature branch, then finish the feature with a PR to `main`.

---

## Cross-cutting work (parallel to tickets)

- Refresh `CURRENT.md` on `feat/FR-0003-hearth-pi-docker-cli`; it currently describes the merged **T-FR-0003-02** ticket branch rather than the feature rollup.
- After PR #8 merges, union **TFR0003_13_*** `triadDone` into `docs/design/tickets-initial.md` and update the **T-FR-0003-13** row in `tasks/ticket-progress.md` on the feature branch.
- When FR-0003 feature-branch state is merged toward `main`, reconcile root `tasks/ticket-progress.md` and `docs/design/tickets-initial.md` so future frontier runs do not need this integration note.

---

## First concrete steps (primary next ticket)

1. Pull `.worktrees/FR-0003-hearth-pi-docker-cli/feature/` and confirm it includes PR #9.
2. Decide whether PR #8 (**T-FR-0003-13**) should be merged before or during the next implementation wave.
3. Start **T-FR-0003-04**, **T-FR-0003-05**, and **T-FR-0003-10** as separate child worktrees and ticket branches from `feat/FR-0003-hearth-pi-docker-cli`.
4. Refresh repo-root `CURRENT.md` on the feature branch so it lists the active parallel set and next actions instead of a completed ticket-only summary.

---

## Related files

- `tasks/ticket-progress.md`
- `tasks/feature-history/TICKET-SOURCES.md`
- `tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`
- `tasks/feature-history/FR-0003-hearth-pi-docker-cli/20-tickets-dag.md`
- `docs/design/tickets-initial.md`
- Prior snapshots: `tasks/handoffs/2026-05-10-parallel-frontier.md`, `tasks/handoffs/2026-05-10-parallel-frontier-b.md`, `tasks/handoffs/2026-05-11-parallel-frontier.md`
