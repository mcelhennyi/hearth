# UI design mocks (HTML / CSS)

**Visual source of truth** for Hearth shell and dashboard **layout, spacing, typography, color, and chrome proportions**. Open these files in a browser; do not infer layout from ASCII diagrams in markdown.

**Logical source of truth** (behavior, routes, APIs, zones, acceptance rules) remains in:

- [`../mantle-ui.md`](../mantle-ui.md) — Mantle shell, chrome contract, tokens (names/values table)
- [`../dashboard.md`](../dashboard.md) — home grid, block types, layout persistence

When markdown and a mock disagree on **appearance**, **amend the mock or the design doc** per [`../../ai-context.md`](../../ai-context.md); when they disagree on **behavior**, fix the spec or the implementation — not the other way around.

## Shared assets

| File | Role |
|------|------|
| [`mantle-mock.css`](mantle-mock.css) | Shared tokens and chrome/plugin-frame styles for Mantle app mocks |

Dashboard mocks embed their own CSS (same token names as [`mantle-ui.md`](../mantle-ui.md)).

## Mock index

| Mock | Viewport | Mode | What it shows |
|------|----------|------|----------------|
| [`dashboard-iphone.html`](dashboard-iphone.html) | iPhone PWA | **Dashboard** `/` | 4-column home grid; fixed bottom bar — **Home** and **Settings** pinned, scrollable **app launcher** center |
| [`dashboard-desktop.html`](dashboard-desktop.html) | Desktop ≥768px | **Dashboard** `/` | 8-column home grid; fixed bottom bar (not floating dock); **Settings** → floating modal |
| [`mantle-iphone-bare.html`](mantle-iphone-bare.html) | iPhone PWA | **App** `/<slug>/` | Shell only — empty plugin iframe; generic title **Plugin** |
| [`mantle-desktop-bare.html`](mantle-desktop-bare.html) | Desktop | **App** `/<slug>/` | Shell only — empty plugin iframe; generic title **Plugin** |
| [`mantle-iphone-groceries.html`](mantle-iphone-groceries.html) | iPhone PWA | **App** (example) | Filled plugin UI + top/bottom **chrome slots**; center bottom bar has **no other app tabs** |
| [`mantle-desktop-groceries.html`](mantle-desktop-groceries.html) | Desktop | **App** (example) | Same; wide plugin layout with sidebar (mock-only) |

The **groceries** HTML files illustrate a **reference plugin** only (`FR-0001`); they are not part of the bare shell contract.

## Bottom bar (canonical behavior)

| Context | Left (pinned) | Center | Right (pinned) |
|---------|---------------|--------|----------------|
| **Dashboard** | Home (active on `/`) | Scrollable **app launcher** (registry-driven tabs) | Settings |
| **App** `/<slug>/` | Home (back to `/`) | **Plugin** `[ui.chrome].bottom` slots only | Settings |

Desktop dashboard and app mocks use the same **fixed, full-width bottom bar** (see `dashboard-desktop.html`, `mantle-desktop-*.html`). iPhone mocks use the same zones with compact tabs (see `dashboard-iphone.html`, `mantle-iphone-*.html`).

## Dashboard widget layout

Widget blocks use **`data-span-h`** (block height in primitive rows) to pick a layout tier: **`h = 1`** compact (title + action header, metric + subtitle body); **`h ≥ 2`** tall (stacked body with line clamp, footer for meta + action). All copy must stay inside the tile — see [`../dashboard.md`](../dashboard.md) → Widget block chrome.

## Maintenance

- Add or rename mocks here when UI design changes; update links in [`mantle-ui.md`](../mantle-ui.md) and [`dashboard.md`](../dashboard.md) in the same change.
- Prefer editing **CSS** for token tweaks shared across Mantle mocks; keep dashboard HTML self-contained unless extracting shared CSS later.
- When adding widget examples, set **`data-span-h`** to match the block’s `grid-row` span and verify in-browser that nothing clips.
