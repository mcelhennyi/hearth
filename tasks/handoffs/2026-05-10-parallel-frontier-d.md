# Next-step handoff — parallel frontier (2026-05-10, refresh d)

**Audience:** Next agent or maintainer picking up global ticket work.
**Authority:** `tasks/feature-history/**/tickets.md`, `tasks/ticket-progress.md`, `docs/design/tickets-initial.md`, `docs/ai-context.md`.

**Integration note:** Root `main` does **not** yet contain the latest FR-0003 feature branch or FR-0002 Mantle ticket branch. This handoff therefore separates:

- **Strict `main` snapshot:** what `tasks/ticket-progress.md` and `docs/design/tickets-initial.md` say in the root checkout.
- **Practical next frontier after PR #13:** what becomes eligible from `feat/FR-0003-hearth-pi-docker-cli`, where T-FR-0003-04, -05, -10, and -13 are already VAL-done and pushed.

---

## Snapshot: queue beacon (`tasks/ticket-progress.md`)

| Field | Value (as of this handoff) |
|------|----------------------------|
| **Active ticket** | Root checkout still advertises `/develop-frontier` wave 4, but FR-0003 wave 4 has been integrated into `feat/FR-0003-hearth-pi-docker-cli` and opened as PR #13 to `main`. |
| **Active phase** | `handoff` / integration-ready. |
| **Branch / worktree** | FR-0003 feature: `.worktrees/FR-0003-hearth-pi-docker-cli/feature/` -> `feat/FR-0003-hearth-pi-docker-cli`; PR #13 targets `main`. FR-0002 feature: `.worktrees/FR-0002-iphone-pwa-prototype/feature/`. |
| **Session status** | `handoff` |
| **Next agent should** | If continuing FR-0003 before PR #13 merges, branch from `feat/FR-0003-hearth-pi-docker-cli`. If working from root `main`, first merge/review PR #13 or re-run this command after it lands. |

**Triad-complete (strict root `main` summary):** `T-FR-0000-01`, `T-FR-0003-01`.

**Triad-complete on FR-0003 feature branch / PR #13:** `T-FR-0000-01`, `T-FR-0003-01`, `T-FR-0003-02`, `T-FR-0003-04`, `T-FR-0003-05`, `T-FR-0003-10`, `T-FR-0003-13`.

**Still incomplete:** FR-0002 `T-FR-0002-01` remains VAL-blocked on real Mac mini/Pi hardware; FR-0002 `T-FR-0002-02` has PR #7 open into the FR-0002 feature branch. FR-0003 next implementation tickets after PR #13 are `T-FR-0003-03`, `T-FR-0003-06`, `T-FR-0003-07`, and `T-FR-0003-09`.

---

## Snapshot: what the dependency graph allows in parallel

**Eligibility rule:** Every ticket in **Deps:** has **VAL** = `done` in the branch used as the source of truth. For FR-0003 below, that source is **PR #13 / `feat/FR-0003-hearth-pi-docker-cli`**, not root `main`.

With **T-FR-0003-02**, **T-FR-0003-04**, **T-FR-0003-05**, and **T-FR-0003-10** VAL-done on the FR-0003 feature branch, these tickets are eligible and mutually non-blocking:

| Ticket | Title | FR | Deps | Practical action |
|--------|-------|----|------|------------------|
| [T-FR-0003-03](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-03--install-bootstrap-docker--layout--first-compose-up) | `./install` bootstrap: Docker + layout + first `compose up` | FR-0003 | `T-FR-0003-02`, `T-FR-0003-05` | Start from `feat/FR-0003-hearth-pi-docker-cli` after PR #13 state. |
| [T-FR-0003-06](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-06--hearth---update) | `hearth --update` | FR-0003 | `T-FR-0003-04`, `T-FR-0003-05` | Start from `feat/FR-0003-hearth-pi-docker-cli` after PR #13 state. |
| [T-FR-0003-07](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-07--hearth---plugin---add-and-list) | `hearth --plugin --add` and `list` | FR-0003 | `T-FR-0003-04`, `T-FR-0003-05` | Start from `feat/FR-0003-hearth-pi-docker-cli` after PR #13 state. |
| [T-FR-0003-09](../feature-history/FR-0003-hearth-pi-docker-cli/tickets.md#t-fr-0003-09--hearth-stack-control-startstoprestartstatuslogs) | `hearth` stack control: start/stop/restart/status/logs | FR-0003 | `T-FR-0003-04`, `T-FR-0003-05` | Start from `feat/FR-0003-hearth-pi-docker-cli` after PR #13 state. |
| [T-FR-0002-01](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md#t-fr-0002-01--caddy--tls-internal--static-placeholder) | Caddy + tls internal + static placeholder | FR-0002 | `none` | VAL-only; requires real Mac mini/Pi target and trusted desktop-browser flow. |
| [T-FR-0002-02](../feature-history/FR-0002-iphone-pwa-prototype/tickets.md#t-fr-0002-02--mantle-pwa-bones-manifest--sw--bottom-tab-placeholder) | Mantle PWA bones | FR-0002 | `none` | PR #7 is open into the FR-0002 feature branch; review/merge rather than duplicate. |

So **up to four new FR-0003 streams** are dependency-valid after PR #13 state: `T-FR-0003-03`, `T-FR-0003-06`, `T-FR-0003-07`, and `T-FR-0003-09`. FR-0002 work is integration/hardware-gated rather than a clean new code stream.

**Examples of what stays blocked until more VAL-done rows exist:**

- **T-FR-0002-03** needs **T-FR-0002-01** and **T-FR-0002-02** VAL-done.
- **T-FR-0002-04** needs **T-FR-0002-01**, **T-FR-0002-02**, and **T-FR-0002-03** VAL-done.
- **T-FR-0003-08** needs **T-FR-0003-07** VAL-done.
- **T-FR-0003-11** needs **T-FR-0003-07** and **T-FR-0003-10** VAL-done.
- **T-FR-0003-12** remains the FR-0003 closeout smoke/ARM ticket after **-03**, **-06**, **-08**, **-09**, and **-11**.

Full **Deps:** edges live in the per-feature `tickets.md` files; the global mermaid in `docs/design/tickets-initial.md` must be unioned when PR #13 or later ticket branches merge.

---

## Process note (queue vs graph)

The frontier is global, but active implementation should respect feature-branch reality:

- **If working from `main`:** PR #13 is the next integration gate for FR-0003. Do not start `T-FR-0003-03/-06/-07/-09` from stale `main`.
- **If working from the FR-0003 feature branch:** the next wave is dependency-valid now, because the feature branch already contains the needed predecessor tickets.
- **FR-0001** remains parked by registry policy even though `T-FR-0001-01` has `Deps: none`.

---

## Cross-cutting work (parallel to tickets)

- Merge/review **PR #13** (`feat/FR-0003-hearth-pi-docker-cli` -> `main`) or continue FR-0003 from that feature branch.
- Review/merge **PR #7** for `T-FR-0002-02`; do not duplicate Mantle PWA bones work.
- Complete **T-FR-0002-01** VAL only when a real Mac mini/Pi target and trusted desktop-browser workflow are available.
- Keep repo-root `CURRENT.md` branch-local: retain it on `feat/*`; remove it when a feature branch lands on `main`.

---

## First concrete steps

1. For FR-0003 continuation: run `/develop-frontier 0003` from or against `feat/FR-0003-hearth-pi-docker-cli`, targeting **T-FR-0003-03**, **T-FR-0003-06**, **T-FR-0003-07**, and **T-FR-0003-09**.
2. For `main` hygiene: review and merge **PR #13** first, then re-run `/identify-frontier` from clean `main`.
3. For FR-0002: review **PR #7** and schedule the **T-FR-0002-01** hardware VAL.
4. Do not remove remote `feat/*` ticket branches automatically; they remain the audit trail.

---

## Related files

- `tasks/ticket-progress.md`
- `tasks/feature-history/TICKET-SOURCES.md`
- `tasks/feature-history/FR-0002-iphone-pwa-prototype/tickets.md`
- `tasks/feature-history/FR-0003-hearth-pi-docker-cli/tickets.md`
- `docs/design/tickets-initial.md`
- Prior snapshots: `tasks/handoffs/2026-05-10-parallel-frontier.md`, `tasks/handoffs/2026-05-10-parallel-frontier-b.md`, `tasks/handoffs/2026-05-10-parallel-frontier-c.md`
