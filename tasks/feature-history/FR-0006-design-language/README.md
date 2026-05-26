# FR-0006 — Design-language unification

**Status:** `done` (merged to **`main`** via [PR #46](https://github.com/mcelhennyi/hearth/pull/46) @ `25e3381`) · **Owner:** human + AI · **Started:** 2026-05-21

Cross-repo design-language alignment across **hearth**, **kindling**, and **grocery-list**. Closeout: [`90-closeout.md`](90-closeout.md) · Finish handoff: [`handoffs/2026-05-21-finish-feature.md`](handoffs/2026-05-21-finish-feature.md).

## Scope (this repo)

1. Design doc amendments (`dashboard.md`, `mantle-ui.md`, `plugin-contract.md`).
2. Mantle shell — chrome slots, postMessage, frame states, Settings modal.
3. Dashboard grid — layout API, blocks, empty state, edit mode.
4. **`@kindling/mantle`** — components, hooks, vanilla bridge, overlays, private package artifact validation.

## Partner FRs

| Repo | FR | Role |
|------|----|------|
| **kindling** | FR-0001 | plugin-ui-system + template; consumes `@kindling/mantle` |
| **grocery-list** | FR-0002 | mantle-ui consumption |

## Artifacts

- [`00-intake.md`](00-intake.md)
- [`10-design-00-skeleton.md`](10-design-00-skeleton.md)
- [`20-tickets-dag.md`](20-tickets-dag.md)
- [`tickets.md`](tickets.md)
- [`90-closeout.md`](90-closeout.md)
- [`serial-diary.md`](serial-diary.md)
- [`handoffs/`](handoffs/)
