# FR-0006 closeout — Design-language unification

**Merged:** [**PR #46**](https://github.com/mcelhennyi/hearth/pull/46) → **`main`** @ `25e3381` on 2026-05-26. Feature branch head before merge: `121706e`.

## Executive summary

FR-0006 unifies the Hearth dashboard and Mantle shell with the design docs and mockups: system tiles/strips and layout APIs, postMessage bridge, Settings modal, chrome slots, plugin frame states, dashboard grid with empty state and edit mode, and the private **`@kindling/mantle`** package (components, hooks, vanilla bridge, overlays, CI package validation).

## Delivered surfaces

| Surface | Location |
|---------|----------|
| System tiles & strips API | `apps/hub/api` (`system` routes) |
| Dashboard layout API | `apps/hub/api` (`dashboard` routes) |
| Mantle shell bridge + chrome | `apps/hub/web/src/shell/` |
| Dashboard grid, empty state, edit mode | `apps/hub/web/src/dashboard/` |
| `@kindling/mantle` package | `packages/mantle/` |
| Mantle CI + package validation workflows | `.github/workflows/kindling-mantle-*.yml` |
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
| T-FR-0006-15 | @kindling/mantle package validation | **done** |

## Validation

- `./develop test` — **287** pytest passed, 3 skipped (2026-05-26 conflict-fix rerun)
- Hub web Vitest — **57** passed (14 files)
- `@kindling/mantle` `pnpm test` — **37** passed

## Deferred / follow-up

| Item | Tracking |
|------|----------|
| Public npm publish | Explicitly deferred; do not configure **`NPM_TOKEN`** or push a publish tag until publish policy changes. |
| Shell overlay rendering for `hearth.sheet` / `hearth.dialog` | v0 in-iframe fallback; follow-up shell ticket |
| Settings chrome route (`RW-U2`) | REWORK-REQUIRED in `App.tsx` — modal-only v0 |
| Partner repos: kindling FR-0001, grocery-list FR-0002 | Consume the local/private Mantle package path until publish policy changes. |
| Manual iPhone / Pi dashboard smoke | Operator VAL |

## Suggested next step

Keep **`@kindling/mantle`** private for now, then run partner FRs in kindling and grocery-list using a local/private package path.

## Options

| Option | When |
|--------|------|
| Keep Mantle private | Default — continue local/private package consumption |
| Staff FR-0004 auth | After merge if auth is next platform priority |
| Staff FR-0005 remote-build | Parallel design track on `main` |

## Audit

- **Feature branch:** `feat/FR-0006-design-language` @ `121706e` (retained on remote)
- **Merge:** [PR #46](https://github.com/mcelhennyi/hearth/pull/46) @ `25e3381`
- **Ticket PRs:** #31–#45 → feature branch
- **Handoff:** [`handoffs/2026-05-21-finish-feature.md`](handoffs/2026-05-21-finish-feature.md)
