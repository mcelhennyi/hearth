# Dashboard — home grid and plugin surfaces

**Authority:** This document defines the Hearth **home dashboard** at `/` — **behavior, block types, layout model, and persistence** (logical). **Grid appearance** (tile sizes, spacing, widget chrome on screen) is authoritative in **[`mockups/dashboard-iphone.html`](mockups/dashboard-iphone.html)** and **[`mockups/dashboard-desktop.html`](mockups/dashboard-desktop.html)** — see **[`mockups/README.md`](mockups/README.md)**. Shell chrome is specified in [`mantle-ui.md`](mantle-ui.md). Manifest fields live in [`plugin-contract.md`](plugin-contract.md).

The primary client is an **iPhone PWA**; the dashboard grid is designed to feel like the iOS Home Screen: fixed columns, tappable blocks of multiple primitive sizes, and an edit mode to rearrange.

## Goals

1. **One home surface** — `/` is a user-composed grid, not a static plugin list.
2. **Per-plugin home contributions** — an enabled plugin may surface on the dashboard as an **app icon** (tap opens its full UI at `/<slug>/`), as one or more **widgets** (compact data/actions in a grid block), or **both**. The user chooses which blocks appear via layout (edit mode); nothing forces every contribution to be on the grid at once.
3. **App plugins first** — registry, proxy, Mantle iframe embed, and grid **shortcuts** ship before widget hosting is enabled end-to-end.
4. **Consistent chrome** — top and bottom bars stay visually and structurally the same in the dashboard and inside apps; plugins may **extend** bars, not replace them.

## What plugins can put on the home grid

| Contribution | Block type | Tap behavior | Who declares it |
|--------------|------------|--------------|-----------------|
| **App icon** | `app-shortcut` (`1×1` by default) | Opens `/<slug>/` in the plugin frame | Every enabled **`app`** plugin (icon/label from `[ui.nav]` / `plugin.icon`) |
| **Widget** | `widget` (span per surface) | In-block actions; optional “Open app” navigates to `/<slug>/` | **`app`** plugins with `[widget.surfaces.*]`, or **`widget`**-only plugins |

An **`app`** plugin with a full UI may ship **zero, one, or many** widget surfaces in addition to its icon — e.g. Groceries with a `1×1` shortcut plus a `2×1` “items low on stock” tile. A **`widget`**-only plugin contributes widgets **without** a full SPA or app icon (see [`plugin-contract.md`](plugin-contract.md#plugin-kind-app-vs-widget)).

## Plugin kinds (summary)

| Kind | User experience | Backend | UI delivery | MVP |
|------|-----------------|---------|-------------|-----|
| **`app`** | Full UI at `/<slug>/…`; optional **app icon** and/or **widget** blocks on `/` | Plugin process + proxied UI | `entrypoint.ui` (`static`, `iframe-spa`, later `module-federation`) | **Supported** (icon/shortcut); widgets **deferred** |
| **`widget`** | Widget block(s) only — no full app view | Plugin process; **no** `entrypoint.ui` | Hub-fetched **widget snapshot** + Mantle **widget primitives** (no iframe) | **Declared in Tinder; hosting deferred** |

Details and manifest keys: [`plugin-contract.md` → Plugin kind](plugin-contract.md#plugin-kind-app-vs-widget).

## Visual mocks

| Viewport | File | Notes |
|----------|------|-------|
| iPhone (4 columns) | [`mockups/dashboard-iphone.html`](mockups/dashboard-iphone.html) | App shortcuts, widgets, system tiles, PWA install strip; bottom bar per [`mantle-ui.md`](mantle-ui.md) |
| Desktop (8 columns) | [`mockups/dashboard-desktop.html`](mockups/dashboard-desktop.html) | Wider grid; **fixed bottom bar** (aligned with Mantle app mocks, not a floating dock); settings modal |

Example **app** chrome with a filled plugin iframe: [`mockups/mantle-iphone-groceries.html`](mockups/mantle-iphone-groceries.html), [`mockups/mantle-desktop-groceries.html`](mockups/mantle-desktop-groceries.html). Bare shell at `/<slug>/`: [`mockups/mantle-iphone-bare.html`](mockups/mantle-iphone-bare.html), [`mockups/mantle-desktop-bare.html`](mockups/mantle-desktop-bare.html).

## Dashboard grid

### Primitive cell

The grid is measured in **primitive cells** — the smallest square unit on the home screen (analogous to one iOS app icon cell).

| Property | Mobile (portrait) | Desktop (≥768px) |
|----------|-------------------|------------------|
| Column count | **4** fixed | **8** fixed (wider canvas; same primitive size) |
| Row height | Equal to column width (square cells) | Same |
| Gap | Token `--hearth-grid-gap` (default 8px) | Same |
| Safe area | Respect `--hearth-safe-top/bottom`; grid scrolls vertically | Same |

### Block spans

A **block** occupies a rectangle of primitive cells. Allowed spans:

| Field | Range | Notes |
|-------|-------|-------|
| `w` (width) | 1–4 on mobile, 1–8 on desktop | Must fit in column count |
| `h` (height) | 1–4 | Tall widgets (calendar, list preview) |

Examples on mobile (4 columns): `1×1` shortcut, `2×1` wide widget, `2×2` medium widget, `4×2` full-width strip.

Blocks **do not overlap**. The layout engine packs blocks in row-major order with user-defined positions stored explicitly (see persistence); on conflict, edit mode highlights the collision.

### Widget block chrome (visual)

Widget tiles are **fixed to their grid rectangle** (square primitive cells × `w` × `h`); content **must not clip** outside the rounded block. Mocks encode two layout tiers by block height (`data-span-h` on widget blocks):

| Block height `h` | Layout | Typical content |
|------------------|--------|-----------------|
| **`h = 1`** | **Compact** — title and primary action on one header row; metric and subtitle share the remaining row (subtitle may wrap up to two lines with ellipsis) | Metric snapshots (e.g. Pantry `2×1`) |
| **`h ≥ 2`** | **Tall** — title, growing body (list/metric with line clamp), footer row with meta + action | Event lists (e.g. Scheduler Today `2×2`) |

Mantle widget primitives must respect the same bounds when rendering hub snapshots. Reference: [`mockups/dashboard-iphone.html`](mockups/dashboard-iphone.html), [`mockups/dashboard-desktop.html`](mockups/dashboard-desktop.html).

### Block types

| `type` | Purpose | MVP |
|--------|---------|-----|
| `app-shortcut` | Icon + label; tap opens `/<slug>/` in the plugin frame | **Yes** — default block for each enabled **app** plugin |
| `widget` | Hosts a widget plugin surface (`surface` id) | **Schema only** — renders placeholder until widget hosting ships |
| `system` | Hub-owned tiles (CA install, health, issues) | **Optional** — may be fixed blocks or a separate “Setup” sheet |

### Default layout (before user customization)

When no saved layout exists, the hub generates:

1. One `app-shortcut` block per enabled **app** plugin (`1×1`), ordered by `[ui.nav].order` then name — the default **app icon** for each app.
2. **No** automatic `widget` blocks in MVP (even when the manifest declares `[widget.surfaces.*]`); the user adds widgets from the edit-mode picker once hosting ships. Auto-placement from `span_default` is a deferred product detail.
3. Optional fixed **system** blocks at the end of the first row (e.g. “Add this device”) — product decision per [`deployment.md`](deployment.md).

### Edit mode

- Enter: long-press on empty grid area, or an “Edit” control on the dashboard (exact control is implementation detail).
- Behaviors: drag to reposition, drag handles to resize within allowed spans, remove block, add block from a picker (enabled apps + available widget surfaces).
- Exit: Done — persists layout via API (below).
- **App plugins** that are enabled but not placed on the grid still appear in the shell **plugin nav** (see [`mantle-ui.md`](mantle-ui.md)); the grid is not the only launch path.

### Layout persistence

Stored per user (MVP: single local user) in the hub DB.

| Endpoint | Method | Body |
|----------|--------|------|
| `/api/dashboard/layout` | `GET` | — |
| `/api/dashboard/layout` | `PUT` | `DashboardLayout` JSON |

```json
{
  "version": 1,
  "columns": 4,
  "blocks": [
    {
      "id": "b-groceries",
      "type": "app-shortcut",
      "plugin": "groceries",
      "x": 0,
      "y": 0,
      "w": 1,
      "h": 1
    },
    {
      "id": "b-pantry-widget",
      "type": "widget",
      "plugin": "pantry",
      "surface": "item-count",
      "x": 2,
      "y": 0,
      "w": 2,
      "h": 1
    }
  ]
}
```

- `id` — stable UUID for user edits; hub may mint on first save.
- `x`, `y` — origin in primitive cells (0-based, top-left).
- Widget blocks reference `plugin` + `surface` (manifest-defined).

Offline: Mantle caches the last `GET` response in IndexedDB; dashboard renders cached layout with stale badges until online.

## Widget plugins (backend contract, hosting deferred)

Widget plugins exist so lifestyle data can surface on the home grid **without** shipping a full web app.

### Responsibilities

| Layer | Responsibility |
|-------|----------------|
| **Plugin process** | Spark capabilities, optional HTTP on loopback; implements **widget surfaces** (data + actions). |
| **Hub** | Discovers surfaces from Tinder, polls or subscribes for snapshots, enforces permissions, serves `GET /api/dashboard/widgets/<slug>/<surface>`. |
| **Mantle** | Renders snapshot JSON with shared **widget primitives** (`<WidgetMetric>`, `<WidgetList>`, `<WidgetButton>`, …) — no iframe. |

### Snapshot model (target)

Hub returns a versioned JSON document per surface:

```json
{
  "surface": "item-count",
  "title": "Pantry",
  "updated_at": "2026-05-19T12:00:00Z",
  "body": {
    "kind": "metric",
    "value": "12",
    "subtitle": "items",
    "action": { "label": "Open", "nav": "/groceries/" }
  }
}
```

Plugins produce this via Spark method `widget.snapshot` (**DESIGN-GAP DG-S1** — exact method name and capability surface TBD in [`spark-api.md`](spark-api.md) when widget work is scheduled) or hub-side adapter calling existing capability methods.

### MVP policy

- Tinder **`plugin.kind = "widget"`** validates at install time.
- **`POST /api/plugins/<slug>/enable`** for `kind=widget` returns **501** with a clear message until widget hosting is implemented.
- Dashboard **widget** blocks may appear in saved layouts but render a **placeholder** (“Widget support coming soon”) in MVP.

## Navigation model (dashboard vs app)

| Route | Shell mode | Chrome (see mocks) |
|-------|------------|-------------------|
| `/` | **Dashboard** — grid, no iframe | [`dashboard-iphone.html`](mockups/dashboard-iphone.html) / [`dashboard-desktop.html`](mockups/dashboard-desktop.html) — **Home** active; scrollable **app launcher** in bottom bar center |
| `/<slug>/…` | **App** — plugin iframe fills frame | [`mantle-*-bare.html`](mockups/README.md) or filled example — **Home** + **plugin bottom slots** + **Settings**; **no other app tabs** in bottom bar |

Switching from dashboard → app: user taps `app-shortcut` or an app launcher control; shell navigates to `/<slug>/` and keeps bars mounted (no full-page flash).

Returning: **Home** in the bottom bar (or leading control in the top bar on app routes) always returns to `/`.

## Phasing

| Phase | Deliverable |
|-------|-------------|
| **P1 — FR-0001** | **App** plugins only; default auto grid of `app-shortcut` blocks; layout API optional (read-only default OK for first ship). |
| **P2** | User **edit mode** + `PUT /api/dashboard/layout` (**REFINEMENT R-U1** — interaction detail deferred; v0 may ship read-only `GET` only). |
| **P3** | **Widget** hosting: snapshot API, Mantle widget primitives, enable `kind=widget`. |
| **P4** | Spark-driven live tile refresh on dashboard (see [`roadmap.md`](roadmap.md) “Unified dashboard”). |

## Related docs

- [`mockups/README.md`](mockups/README.md) — HTML/CSS visual source of truth index.
- [`mantle-ui.md`](mantle-ui.md) — chrome zones, plugin slot extensions, nav policy.
- [`plugin-contract.md`](plugin-contract.md) — `plugin.kind`, `[widget.*]`, `[ui.chrome]`.
- [`architecture/overview.md`](architecture/overview.md) — hub aggregates dashboard data; Spark fan-out for tile refresh (P4).
