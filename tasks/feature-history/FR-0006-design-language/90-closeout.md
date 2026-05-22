# FR-0006 closeout — Design-language unification

**PR pending:** [**PR #46**](https://github.com/mcelhennyi/hearth/pull/46) → **`main`** @ `6812b38`. Refresh merge line after merge.

## Executive summary

FR-0006 unifies the Hearth dashboard and Mantle shell with the design docs and mockups: system tiles/strips and layout APIs, postMessage bridge, Settings modal, chrome slots, plugin frame states, dashboard grid with empty state and edit mode, and the publishable **`@kindling/mantle`** package (components, hooks, vanilla bridge, overlays, npm CI/publish workflows).

## Delivered surfaces

| Surface | Location |
|---------|----------|
| System tiles & strips API | `apps/hub/api` (`system` routes) |
| Dashboard layout API | `apps/hub/api` (`dashboard` routes) |
| Mantle shell bridge + chrome | `apps/hub/web/src/shell/` |
| Dashboard grid, empty state, edit mode | `apps/hub/web/src/dashboard/` |
| `@kindling/mantle` package | `packages/mantle/` |
| Mantle CI + publish workflows | `.github/workflows/kindling-mantle-*.yml` |
| Design docs + mocks | `docs/design/dashboard.md`, `mantle-ui.md`, `docs/design/mockups/` |

## Tickets

| Ticket | Summary | Status |
|--------|---------|--------|
| T-FR-0006-01 | System tiles & strips API | TEST / DEV / VAL **done** |
| T-FR-0006-02 | Dashboard layout API | **done** |
| T-FR-0006-03 | Mantle postMessage bridge | **done** |
| T-FR-0006-04 | User preferences + Settings modal | **done** |
| T-FR-0006-05 | Plugin frame state UI | **done** |
| T-FR-0006-06 | Chrome slot DOM + rendering | **done** |
| T-FR-0006-07 | Dashboard grid + block primitives | **done** |
| T-FR-0006-08 | Empty state | **done** |
| T-FR-0006-09 | Edit mode | **done** |
| T-FR-0006-10 | @kindling/mantle package scaffold | **done** |
| T-FR-0006-11 | @kindling/mantle base components | **done** |
| T-FR-0006-12 | @kindling/mantle hooks | **done** |
| T-FR-0006-13 | @kindling/mantle overlays | **done** |
| T-FR-0006-14 | @kindling/mantle vanilla bridge | **done** |
| T-FR-0006-15 | @kindling/mantle publish | **done** |

## Validation

- `./develop test` — **269** pytest passed, 3 skipped
- Hub web Vitest — **57** passed (14 files)
- `@kindling/mantle` `pnpm test` — **37** passed (includes `npm publish --dry-run`)

## Deferred / follow-up

| Item | Tracking |
|------|----------|
| First npm publish | Operator: GitHub secret **`NPM_TOKEN`**, tag **`kindling-mantle-v0.1.0`** |
| Shell overlay rendering for `hearth.sheet` / `hearth.dialog` | v0 in-iframe fallback; follow-up shell ticket |
| Settings chrome route (`RW-U2`) | REWORK-REQUIRED in `App.tsx` — modal-only v0 |
| Partner repos: kindling FR-0001, grocery-list FR-0002 | Consume `@kindling/mantle@0.1.0` after publish |
| Manual iPhone / Pi dashboard smoke | Operator VAL |

## Suggested next step

Merge the feature PR to **`main`**, configure **`NPM_TOKEN`**, push tag **`kindling-mantle-v0.1.0`**, then run partner FRs in kindling and grocery-list.

## Options

| Option | When |
|--------|------|
| Merge PR | Default — integrates FR-0006 on `main` |
| Staff FR-0004 auth | After merge if auth is next platform priority |
| Staff FR-0005 remote-build | Parallel design track on `main` |

## Audit

- **Feature branch:** `feat/FR-0006-design-language` @ `110dd0a` (retained on remote)
- **Ticket PRs:** #31–#45 → feature branch
- **Handoff:** [`handoffs/2026-05-21-finish-feature.md`](handoffs/2026-05-21-finish-feature.md)
