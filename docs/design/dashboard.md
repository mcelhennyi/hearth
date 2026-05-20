# Dashboard — home grid and plugin surfaces

**Authority:** This document defines the Hearth **home dashboard** at `/`, how **app** and **widget** plugins participate, and how layout is stored. Shell chrome (top/bottom bars) is specified in [`mantle-ui.md`](mantle-ui.md). Manifest fields live in [`plugin-contract.md`](plugin-contract.md).

The primary client is an **iPhone PWA**; the dashboard grid is designed to feel like the iOS Home Screen: fixed columns, tappable blocks of multiple primitive sizes, and an edit mode to rearrange.

## Goals

1. **One home surface** — `/` is a user-composed grid, not a static plugin list.
2. **Two plugin surfaces** — **app** plugins (full UI at `/<slug>/`) and **widget** plugins (compact data/actions rendered **inside** the grid by Hearth).
3. **App plugins first** — registry, proxy, Mantle iframe embed, and grid **shortcuts** ship before widget hosting is enabled end-to-end.
4. **Consistent chrome** — top and bottom bars stay visually and structurally the same in the dashboard and inside apps; plugins may **extend** bars, not replace them.

## Plugin kinds (summary)

| Kind | User experience | Backend | UI delivery | MVP |
|------|-----------------|---------|-------------|-----|
| **`app`** | Opens a full plugin experience in the shell frame (`/<slug>/…`) | Normal plugin process + proxied UI | `entrypoint.ui` (`static`, `iframe-spa`, later `module-federation`) | **Supported** |
| **`widget`** | Renders inside a dashboard block (counts, lists, one-tap actions) | Plugin process; **no** full SPA required | Hub-fetched **widget snapshot** + Mantle **widget primitives** (no iframe) | **Declared in Tinder; hosting deferred** |

Details and manifest keys: [`plugin-contract.md` → Plugin kind](plugin-contract.md#plugin-kind-app-vs-widget).

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

### Block types

| `type` | Purpose | MVP |
|--------|---------|-----|
| `app-shortcut` | Icon + label; tap opens `/<slug>/` in the plugin frame | **Yes** — default block for each enabled **app** plugin |
| `widget` | Hosts a widget plugin surface (`surface` id) | **Schema only** — renders placeholder until widget hosting ships |
| `system` | Hub-owned tiles (CA install, health, issues) | **Optional** — may be fixed blocks or a separate “Setup” sheet |

### Default layout (before user customization)

When no saved layout exists, the hub generates:

1. One `app-shortcut` block per enabled **app** plugin (`1×1`), ordered by `[ui.nav].order` then name.
2. Optional fixed **system** blocks at the end of the first row (e.g. “Add this device”) — product decision per [`deployment.md`](deployment.md).

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

| Route | Shell mode | Top / bottom bar |
|-------|------------|------------------|
| `/` | **Dashboard** — grid, no iframe | Full chrome; bottom bar includes **Home** (active) + app shortcuts per nav policy |
| `/<slug>/…` | **App** — plugin iframe fills frame | **Same** chrome skeleton; plugin may extend slots (below) |

Switching from dashboard → app: user taps `app-shortcut` or nav tab; shell navigates to `/<slug>/` and keeps bars mounted (no full-page flash).

Returning: **Home** control in the bottom bar (or back chevron in the top bar on desktop) always returns to `/`.

## Phasing

| Phase | Deliverable |
|-------|-------------|
| **P1 — FR-0001** | **App** plugins only; default auto grid of `app-shortcut` blocks; layout API optional (read-only default OK for first ship). |
| **P2** | User **edit mode** + `PUT /api/dashboard/layout` (**REFINEMENT R-U1** — interaction detail deferred; v0 may ship read-only `GET` only). |
| **P3** | **Widget** hosting: snapshot API, Mantle widget primitives, enable `kind=widget`. |
| **P4** | Spark-driven live tile refresh on dashboard (see [`roadmap.md`](roadmap.md) “Unified dashboard”). |

## Related docs

- [`mantle-ui.md`](mantle-ui.md) — chrome zones, plugin slot extensions, nav policy.
- [`plugin-contract.md`](plugin-contract.md) — `plugin.kind`, `[widget.*]`, `[ui.chrome]`.
- [`architecture/overview.md`](architecture/overview.md) — hub aggregates dashboard data; Spark fan-out for tile refresh (P4).
