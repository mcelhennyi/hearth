# FR-0006 — Design-language unification

**Status:** `design` · **Owner:** human + AI · **Started:** 2026-05-21

Cross-repo design-language alignment across **hearth** (this repo), **kindling** (plugin template), and **grocery-list** (reference plugin). Closes 26 gaps from a four-quadrant audit covering `docs/design/dashboard.md`, `docs/design/mantle-ui.md`, the mockups under `docs/design/mockups/`, kindling's plugin-author surface, and grocery-list's UI implementation.

## Scope (this repo)

1. **Amend design docs** to resolve the FIX-tier audit items: `dashboard.md` (DG-U2/3/4/5, DF-U1/2, RW-U3/4), `mantle-ui.md` (DG-U6/7/8/9, DF-U3, theme persistence, bottom-bar divergence), `plugin-contract.md` (DG-T1).
2. **Implement Mantle shell gaps** — chrome-slot DOM zones, postMessage handlers for `hearth.{title,toast,haptic,theme,user,online,chrome.{mount,unmount}}`, plugin frame state UI (load/error/offline).
3. **Implement Settings modal** + dynamic theming context (closes `RW-U2`).
4. **Implement Dashboard grid** — block primitives, default-layout seeder, `GET/PUT /api/dashboard/layout`, app-shortcut rendering, P1 only (widgets/edit-mode tagged for future) (closes `RW-U1`).
5. **Ship `@kindling/mantle`** — shared component package (tokens, base components, postMessage hooks, TypeScript types) authored here, consumed by kindling + grocery-list.

## Partner FRs

| Repo | FR | Role |
|------|----|------|
| **kindling** | FR-0001 `plugin-ui-system` | Author `docs/design/plugin-ui-system.md`, replace bare template, add `templates/plugin-react/`, update consumer rule. Consumes `@kindling/mantle` from hearth FR-0006. |
| **grocery-list** | FR-0002 `mantle-ui` | React + Vite scaffold, consume `@kindling/mantle`, declare `[ui.chrome]` slots, sticky in-frame tabs, sidebar decision per DG-G2. Depends on hearth FR-0006 + kindling FR-0001. |

## Tags reserved

See [`tasks/TAG-REGISTRY.md`](../../TAG-REGISTRY.md):
- DG-U2..U11, DG-T1 (design gaps)
- DF-U1..U3 (design flaws)
- RW-U3, RW-U4 (rework required; existing RW-U1, RW-U2 are addressed in this FR too)

## Artifacts

- [`00-intake.md`](00-intake.md)
- `10-design-00-skeleton.md` *(to be authored)*
- `20-tickets-dag.md` *(to be authored)*
- `tickets.md` *(canonical ticket bodies, to be authored)*
- `serial-diary.md` *(append-only)*
- [`parallel/`](parallel/) *(per-stream diaries)*
- [`handoffs/`](handoffs/) *(continue/milestone/closeout)*
- `90-closeout.md` *(at closeout)*

## Source of analysis

Pre-design four-quadrant audit performed 2026-05-21 covering: dashboard docs + mocks + code; mantle docs + mocks + code; kindling design-language alignment; grocery-list UI vs mocks. See [`00-intake.md`](00-intake.md) §Audit summary.
