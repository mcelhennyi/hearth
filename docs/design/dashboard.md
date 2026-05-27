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
| Gap (`--hearth-grid-gap`) | **8px** | **10px** |
| Outer padding (around the grid; `--hearth-grid-pad`) | **12px** horizontal, `--hearth-safe-top`/`--hearth-safe-bottom` vertical | **16px** all sides |
| Block radius (`--hearth-radius-md`) | **8px** | **8px** |
| Block hairline border | `1px solid color-mix(in srgb, var(--hearth-fg) 8%, transparent)` | Same |
| Safe area | Respect `--hearth-safe-top/bottom`; grid scrolls vertically with `-webkit-overflow-scrolling: touch` | Same |
| Bottom scroll inset | `calc(--hearth-safe-bottom + bottom-bar height)` so the last row clears the fixed bar | Same |

> **DG-U5 closed (2026-05-21):** these metrics are normative and override the mock CSS if they drift. The mock CSS at `mockups/mantle-mock.css` is updated in lockstep.

### Block spans

A **block** occupies a rectangle of primitive cells. Allowed spans:

| Field | Range | Notes |
|-------|-------|-------|
| `w` (width) | 1–4 on mobile, 1–8 on desktop | Must fit in column count |
| `h` (height) | 1–4 | Tall widgets (calendar, list preview) |

Examples on mobile (4 columns): `1×1` shortcut, `2×1` wide widget, `2×2` medium widget, `4×2` full-width strip.

Blocks **do not overlap**. The layout engine packs blocks in row-major order with user-defined positions stored explicitly (see persistence); on conflict, edit mode highlights the collision.

### Widget block chrome (visual)

Widget tiles are **fixed to their grid rectangle** (square primitive cells × `w` × `h`); content **must not clip** outside the rounded block. **`DG-U10`** — exact overflow rules per tier (clamp character counts, internal scroll allowed?) remain deferred until widget hosting (P3) ships; until then, snapshots **must** fit without scroll, with text truncated via `-webkit-line-clamp`. Mocks encode two layout tiers by block height (`data-span-h` on widget blocks):

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
| `system` | Hub-owned status tiles (CA trust, hub healthy, Pi online) sourced from `GET /api/system/tiles` | **Yes (v0)** — fixed `1×1` blocks seeded in the default layout; user-removable in edit mode, restorable from Settings → System tiles (see **`DF-U1`** resolution below) |
| `strip` | Full-width (span `w=columns`, `h=1`) banner for hub-owned promotional or onboarding notices (e.g. "Install Hearth as a PWA") | **Yes (v0)** — at most one strip per dashboard; dismissible; sourced from `GET /api/system/strips` (see **`DF-U2`** resolution below) |

### `system` block — content and configuration (`DF-U1` closed 2026-05-21)

Hub-owned `system` tiles render via the same primitive as plugin shortcuts, but their content is fetched from `GET /api/system/tiles`. v0 tiles:

| Tile id | Title | Body | Action |
|---------|-------|------|--------|
| `ca-trust` | Trust local CA | "Install the Hearth root certificate to remove the iOS warning." | Opens Settings → Trust CA |
| `hub-healthy` | Hub healthy | Compact status badge sourced from `GET /api/health` | Tap → `/settings#diagnostics` |
| `pi-online` | Hub online | Reachability and last-seen for the deployed hub (Pi or Mac) | Tap → `/settings#diagnostics` |

- Tiles are **opt-out** per user (removable in edit mode). Settings → *System tiles* re-adds dismissed tiles.
- Tiles appearing in the default layout are placed **after** `app-shortcut` blocks of the first row, then wrap normally.
- A tile may self-suppress when its precondition is satisfied (e.g. `ca-trust` hides once trust is confirmed).

### `strip` block — content and configuration (`DF-U2` closed 2026-05-21)

`strip` blocks are full-width onboarding banners owned by the hub. They span `w = columns` (4 on mobile, 8 on desktop) at `h = 1`. Sourced from `GET /api/system/strips`:

| Strip id | When shown | Action |
|----------|------------|--------|
| `pwa-install` | iOS Safari and not yet installed | Opens iOS install hint sheet |
| `mac-shell` | Desktop browser, no install hint | Hides itself when dismissed |

Strips render **above** the grid (between top bar and the first row) and are dismissible. At most one strip is visible at a time (hub returns the highest-priority active strip).

### Default layout (before user customization)

When no saved layout exists, the hub generates:

1. One `app-shortcut` block per enabled **app** plugin (`1×1`), ordered by `[ui.nav].order` then name — the default **app icon** for each app.
2. **No** automatic `widget` blocks in MVP (even when the manifest declares `[widget.surfaces.*]`); the user adds widgets from the edit-mode picker once hosting ships. Auto-placement from `span_default` is a deferred product detail.
3. **`system`** blocks from `GET /api/system/tiles` appended after app shortcuts on the first row (wrap as needed); each tile self-suppresses when its precondition is satisfied.
4. **`strip`** block (at most one) rendered **above** the grid when `GET /api/system/strips` returns an active strip for the current platform.

### Empty state (`DG-U4` closed 2026-05-21)

When no enabled **app** plugins exist **and** the hub returns zero `system` tiles, the grid renders a centered empty state:

- Hearth flame icon at 64×64 (`--hearth-accent`).
- Headline: "Your dashboard is empty."
- Body: "Enable plugins in Settings to populate your home grid."
- Primary button: **Open Settings** → opens Settings modal at the *Plugins* tab.

The empty state never co-exists with a populated grid; the moment the first enabled plugin or system tile arrives, the default layout takes over.

### Edit mode (`DG-U2` + `DG-U3` + `RW-U4` closed 2026-05-21)

#### Entry

| Viewport | Entry trigger |
|----------|---------------|
| **Mobile** | **Long-press 600 ms** on any block, on empty grid area, or on the grid background. Long-press uses the system haptic (`hearth.haptic` `style:"impact"`). |
| **Desktop** | **Edit** text button in the top bar (right of "Hearth" title; visible only on dashboard). Long-press is also accepted. |

#### Visual treatment (required, normative; promotes mock visuals to spec)

While edit mode is active:

- All blocks animate with a subtle **jiggle** (≈ ±0.8° rotation, 0.4 s period, randomised phase) so the surface feels mutable.
- Each block shows a circular **× remove badge** at its top-left corner (`top: -6px; left: 50% - 12px`, 24×24, `--hearth-accent` background, `--hearth-accent-fg` foreground).
- **Drag handles** appear at the bottom-right of resizable blocks (`widget` only in v0; shortcuts are fixed `1×1`).
- The strip block in edit mode shows a single full-width × badge (right-aligned).

Prefers-reduced-motion: jiggle is replaced with a 2 px dashed outline around each block.

#### Behaviors

| Gesture | Effect |
|---------|--------|
| Tap × badge | Remove the block (system tiles flip to "hidden by user" — restored from Settings). |
| Drag block | Reposition. Targets snap to the grid; original position holds a faint outline until the drag ends. |
| Drag handle (widget) | Resize within allowed span (`w` 1–4 mobile / 1–8 desktop; `h` 1–4). |
| **+** button in top bar | Open picker (enabled apps not on grid, available widget surfaces, hidden system tiles). |

#### Collisions (`DG-U3`)

- When a drag-end position overlaps another block, both blocks render with a **2 px solid `--hearth-error` outline** (token added below) and the drop is rejected — the dragged block snaps back to its prior position. No partial overlap is ever persisted.
- A persistent banner ("Two blocks are overlapping; resolve before saving.") appears in the top bar, and **Done** is disabled while any pair of blocks reports a collision after move/resize.
- New token: `--hearth-error` (default `#e53935` light / `#ff6b6b` dark).

#### Exit

- **Done** button (top bar) — persists via `PUT /api/dashboard/layout`; returns to view mode.
- **Cancel** button or Escape — discards changes; returns to view mode.
- Native back gesture / Browser back — treated as Cancel (with confirm if changes pending).

#### Notes

- **App plugins** enabled but not placed on the grid still appear in the shell **plugin nav** (see [`mantle-ui.md`](mantle-ui.md)); the grid is not the only launch path.
- Mocks at `mockups/dashboard-iphone.html` and `mockups/dashboard-desktop.html` are now the **reference implementation** for visual details specified above; if the mocks drift from this section, this section wins. See [`mockups/README.md`](mockups/README.md).

### Layout persistence

Stored per authenticated Hearth user in the hub DB.

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

### Bottom-bar app launcher — ownership (`RW-U3` closed 2026-05-21)

The bottom-bar **app launcher** that sits between Home and Settings on the dashboard is owned by **Mantle**, not by this doc. Its sourcing (`GET /api/plugins` filtered to enabled `app` plugins with `show_in_tab_bar = true`), ordering (`[ui.nav].order` then name), overflow (scrollable horizontal strip with edge fade per `R-U2`), and visual styling are specified in [`mantle-ui.md` → Bottom bar — nav policy](mantle-ui.md#bottom-bar--nav-policy). Dashboard tiles and the launcher render the **same** enabled-plugin set; the user's saved layout decides which apps appear as **grid shortcuts**, but every enabled `app` plugin with `show_in_tab_bar = true` always appears in the **launcher** regardless of layout.

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
