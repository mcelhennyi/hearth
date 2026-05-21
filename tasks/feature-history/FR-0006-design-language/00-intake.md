# FR-0006 — Intake

**Title:** Design-language unification across hearth, kindling, grocery-list
**Date opened:** 2026-05-21
**Driver:** Cross-repo design-language drift surfaced during pre-development audit. Dashboard is a plugin list (not a grid); Mantle shell has no chrome-slot wiring, no Settings, no postMessage handlers; kindling provides no design-language bridge to plugin authors; grocery-list ships vanilla HTML with hardcoded colors. The mocks under `docs/design/mockups/` are the visual source of truth; this FR brings code, docs, and the plugin template into alignment.

## Goals

1. Resolve the 19 FIX-tier audit gaps inline in `dashboard.md`, `mantle-ui.md`, `plugin-contract.md`, and `mockups/README.md`.
2. Ship a working Mantle dashboard grid (P1: app-shortcut blocks + default layout + persistence API).
3. Ship chrome-slot wiring (mantle `postMessage` handlers; DOM zones in shell; `hearth.title/online/theme/user` listeners; load/error/offline UI).
4. Ship the Settings modal (closes `RW-U2`) wired from desktop top bar and mobile bottom bar; dynamic theme persistence.
5. Author and publish `@kindling/mantle` (design tokens, base components, postMessage hooks) so kindling and grocery-list can adopt mantle-aligned UI without copying tokens.
6. Update the mockup README to label mocks as **reference implementation** for visual treatments not yet promoted to spec.

## Out of scope (this FR)

- Widget hosting (P3 — keep `DG-U10` open).
- Edit-mode drag/resize implementation (P2 — `R-U1` remains; this FR specifies UX **only**).
- Plugin module federation (post-MVP).
- Overlay toast/haptic implementation (`DG-U11` resolved in design only; implementation deferred until first plugin consumer).
- `system` and `strip` block-type **rendering** beyond the seeded set in default layout (specifications land in `dashboard.md` via DF-U1/U2).
- grocery-list smart-list, history, notifications, multi-list (separate grocery-list FRs).

## Success criteria

- All 19 FIX-tier audit items have inline design-doc amendments under amendment blocks per `docs/ai-context.md`.
- Mantle shell renders chrome-slot DOM zones and updates them from plugin `postMessage` events; verified with grocery-list mounting Filter/Add/Sort/Clear buttons.
- Dashboard `/` renders a grid of app-shortcut blocks for enabled plugins; layout persists via `PUT /api/dashboard/layout` and rehydrates on reload.
- Settings modal opens from desktop top bar + mobile bottom bar; theme toggle (light/dark/system) persists and propagates to plugin iframes via `hearth.theme`.
- `@kindling/mantle` published as a versioned package consumable from kindling `templates/plugin-react/` and grocery-list's new React shell.
- 238 existing tests still pass; new tests cover slot wiring, dashboard API, theme persistence, and the package's exported types.

## Audit summary (2026-05-21)

| Quadrant | Severity | Headline |
|----------|----------|----------|
| Hearth dashboard | Critical | Code is a plugin-list stub; ~9 design gaps in dashboard.md |
| Hearth mantle | Critical | Tokens + PWA wiring good; no chrome-slots, no Settings, no postMessage handlers |
| Kindling | High | No design-language bridge doc; template lacks tokens/meta; no `@kindling/mantle` |
| Grocery-list | High | Vanilla HTML, hardcoded colors, no Mantle integration (deliberate MVP, but now blocking) |

Full report: see chat transcript 2026-05-21 (four parallel subagent audits).

## Triage (user-approved 2026-05-21)

**FIX (amend doc inline, 19):** DG-U2, DG-U3, DG-U4, DG-U5, DG-U6, DG-U7, DG-U8, DG-U9, DF-U1, DF-U2, DF-U3, RW-U3, RW-U4, theme persistence, bottom-bar divergence, dashboard.md ↔ mantle-ui.md launcher cross-ref, DG-T1, DG-K1 (kindling), DG-G1 + DG-G2 + sticky-tabs (in plugin-contract.md).
**TAG (ship with marker; resolve in design stage):** DG-U10 (widget overflow), DG-U11 (overlay primitives), DF-K1 (template tokens), RW-K1 (plugin-react template), DF-K2 (kindling-consumer rule), RW-G1 (grocery vanilla→React).
**DECIDED:** Ship `@kindling/mantle` package now (#21) inside hearth FR-0006.

## Raw request

> design language update. Analyze the dashboard and mantle docs and mocks. Review the current implementation of these elements in code. Fully implement those design docs to bring the UI up to spec. Ensure that during analysis you mark the design docs with any tags necessary. Notify me of any gaps or ambiguities that I can fix prior to development. Include kindle updates and grocery app updates as well to make a fully complete update for the current state of the application. Apply those updates to their respective repos. Ensure that the skeleton in each repo is updated as well to ensure the docs are properly updated during this process.
