# FR-0006 — Tickets

**Feature:** FR-0006 `design-language` · **next_xx:** `16`

Authoritative ticket bodies for the design-language unification. Source-of-truth for `develop-frontier` / `identify-frontier`. DAG view: [`20-tickets-dag.md`](20-tickets-dag.md).

---

### T-FR-0006-01 — System tiles & strips API

**Type:** impl · **Deps:** none · **Order:** P0 · **Owner:** —

Implement hub-side endpoints supporting `system` block content on the dashboard (closes `DF-U1`, `DF-U2`).

**Surface**

- `GET /api/system/tiles` → `{tiles: SystemTile[]}` where `SystemTile = {id, title, body, action?: {nav: string}, hidden_by_user: bool, suppressed: bool}`. v0 tiles: `ca-trust`, `hub-healthy`, `pi-online`.
- `POST /api/system/tiles/<id>/hide` → 204.
- `POST /api/system/tiles/<id>/restore` → 204.
- `GET /api/system/strips` → `{strip: SystemStrip | null}` — single highest-priority active strip. v0 strips: `pwa-install` (iOS+not-installed), `mac-shell` (desktop browser).
- `POST /api/system/strips/<id>/dismiss` → 204; persists per-user dismissal.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Pytest fixtures for tile/strip computation; suppression rules; user-hide persistence (SQLite). |
| **DEV** | `app/system_tiles.py` + `app/system_strips.py`; routes wired in `app/routes/system.py`; alembic migration for `user_system_state` table. |
| **VAL** | All tests pass in Docker; OpenAPI schema regen; manual sanity hit via `httpx` script. |

---

### T-FR-0006-02 — Dashboard layout API

**Type:** impl · **Deps:** none · **Order:** P0 · **Owner:** —

Implement `GET/PUT /api/dashboard/layout` and the default-layout generator (closes part of `RW-U1`).

**Surface**

- `GET /api/dashboard/layout` → `DashboardLayout` (schema in [`docs/design/dashboard.md`](../../../docs/design/dashboard.md#layout-persistence)). Returns default layout when none persisted.
- `PUT /api/dashboard/layout` → 200 on save, **409** on detected collision (any pair of blocks with overlapping rectangles), **422** on schema invalid.

**Default-layout rules**

1. One `app-shortcut` per enabled `app` plugin (`1×1`), ordered by `[ui.nav].order` then `name`.
2. `system` tiles appended after shortcuts on the first row (wrap).
3. No `widget` blocks in default (P3 deferred).

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Pytest: default seed for 0/1/N plugins; PUT-then-GET round trip; collision rejection; schema validation. |
| **DEV** | `app/dashboard.py`, `app/schemas/dashboard.py`, `app/routes/dashboard.py`; alembic migration `dashboard_layouts` (user_id, json blob, version). |
| **VAL** | Tests pass in Docker; OpenAPI updated. |

---

### T-FR-0006-03 — Mantle postMessage bridge

**Type:** impl · **Deps:** none · **Order:** P0 · **Owner:** —

Implement the inbound listener + outbound pusher for the postMessage protocol in Mantle (closes `DG-U6`/`DG-U7`/`DG-U9` shell-side wiring).

**Surface**

- `apps/hub/web/src/shell/usePostMessageBridge.ts` — single owner of `window.addEventListener("message")` with origin guard (`event.origin === window.location.origin`).
- Handles inbound: `hearth.title`, `hearth.toast` (console log only — DG-U11 stub), `hearth.haptic` (iOS Web API; no-op elsewhere), `hearth.chrome.{mount,unmount}`.
- Pushes outbound: `hearth.theme`, `hearth.user`, `hearth.online`, `hearth.frame.state`, `hearth.chrome.{resize,invoke}`.
- Exposes a small typed event bus the rest of the shell subscribes to (no scattered listeners).

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Vitest + jsdom: message-origin guard rejects cross-origin; each inbound type dispatches; each outbound posts with correct shape. |
| **DEV** | Bridge module + integration in `App.tsx`; remove the placeholder comment block in `PluginFrame.tsx`. |
| **VAL** | Existing tests pass + new bridge tests; manual smoke vs. a stub plugin emitting `hearth.title`. |

---

### T-FR-0006-04 — User preferences API + Settings modal

**Type:** impl · **Deps:** T-FR-0006-01 (route conventions), T-FR-0006-03 · **Order:** P1 · **Owner:** —

Closes `DG-U8`, `RW-U2`.

**Surface**

- `GET /api/user/preferences` → `{theme: "light"|"dark"|"system"}` and future toggles.
- `PUT /api/user/preferences` — merge body; 200.
- `apps/hub/web/src/shell/SettingsModal.tsx` — floating modal (desktop) / bottom sheet (mobile); tabs: **Theme**, **Plugins**, **System tiles**, **Diagnostics**, **Sign out**.
- `apps/hub/web/src/theme/ThemeProvider.tsx` — boot from `localStorage` `hearth.theme.preference`, reconcile with server prefs after first paint, broadcast `hearth.theme` via bridge to all plugin iframes on change, update `theme-color` meta tag.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Pytest for preferences API; Vitest for ThemeProvider boot + reconcile flow; Vitest for SettingsModal a11y (focus trap, Escape close). |
| **DEV** | Both backend + frontend pieces; mobile sheet uses `<dialog>` with safe-area awareness. |
| **VAL** | Tests pass in Docker; manual: open Settings from both triggers; toggle theme persists across reload and across browsers. |

---

### T-FR-0006-05 — Plugin frame state UI

**Type:** impl · **Deps:** T-FR-0006-03 · **Order:** P1 · **Owner:** —

Closes `DG-U7`.

**Surface**

- `apps/hub/web/src/shell/PluginFrameStates.tsx` rendering: Mounted (transparent), Loading (spinner + plugin title from registry), Slow (after 5 s subtitle), Error (card + Reload + Open Settings), Offline (card + Try again).
- State machine in `usePluginFrameState.ts` driven by iframe `load`/`error`, fetch probe to plugin root, navigator.onLine.
- Shell pushes `hearth.frame.state` to the plugin (when it's reachable) so the plugin suppresses its own overlays.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Vitest: state transitions for each trigger; 5 s and 15 s timers (vi.useFakeTimers). |
| **DEV** | Component + state hook; CSS scrim respects safe-area. |
| **VAL** | Tests pass; manual: throttle network in DevTools and confirm Slow → Error escalation. |

---

### T-FR-0006-06 — Chrome slot DOM + rendering

**Type:** impl · **Deps:** T-FR-0006-03 · **Order:** P1 · **Owner:** —

Closes `DG-U6` shell side.

**Surface**

- DOM zones `.chrome-slot--top` and `.plugin-bottom-slots` in `App.tsx`; `.shell.has-chrome-slots` toggle when any slot mounted.
- `apps/hub/web/src/shell/ChromeSlot.tsx` rendering ChromeButton/ChromeMenu from registry state.
- Overflow `⋯` menu when item count exceeds visible cap (top=3, bottom=4).
- Per-plugin total cap enforcement (≤8); excess registrations bounce with `hearth.chrome.error`.
- Implicit `hearth.chrome.unmount` on plugin route change.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Vitest: mount/update/unmount; cap enforcement; overflow menu rendering; route-change auto-unmount. |
| **DEV** | Slot registry hook + components + CSS to mirror mock zone layout. |
| **VAL** | Tests + manual against a stub plugin mounting 5 top buttons → overflow correct. |

---

### T-FR-0006-07 — Dashboard grid + block primitives

**Type:** impl · **Deps:** T-FR-0006-02 · **Order:** P1 · **Owner:** —

Closes core of `RW-U1`.

**Surface**

- `apps/hub/web/src/dashboard/Grid.tsx` — CSS grid per [`docs/design/dashboard.md` § Primitive cell](../../../docs/design/dashboard.md#primitive-cell) and `DG-U5` metrics.
- `apps/hub/web/src/dashboard/blocks/AppShortcut.tsx` — icon + label + tap-to-navigate.
- `apps/hub/web/src/dashboard/blocks/System.tsx` — fetched from `/api/system/tiles`.
- `apps/hub/web/src/dashboard/blocks/Strip.tsx` — full-width banner above the grid.
- `apps/hub/web/src/dashboard/blocks/Widget.tsx` — placeholder (P3 deferred).
- DashboardView reads `/api/dashboard/layout`, renders blocks; offline fallback from IndexedDB cache.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Vitest snapshots for desktop/mobile grids; block click navigates; offline cache rehydrates. |
| **DEV** | Components + CSS; remove legacy plugin-list DashboardView. |
| **VAL** | Tests in Docker; manual sanity at both breakpoints. |

---

### T-FR-0006-08 — Empty state

**Type:** impl · **Deps:** T-FR-0006-07 · **Order:** P2 · **Owner:** —

Closes `DG-U4`.

**Surface**

- `apps/hub/web/src/dashboard/EmptyState.tsx` rendered when layout has zero blocks. Headline, body, Open Settings CTA opens the modal at Plugins tab.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Vitest: renders when blocks empty; CTA triggers Settings open. |
| **DEV** | Component + wiring. |
| **VAL** | Tests; manual: hub with no enabled plugins shows empty state. |

---

### T-FR-0006-09 — Edit mode

**Type:** impl · **Deps:** T-FR-0006-07, T-FR-0006-02 · **Order:** P2 · **Owner:** —

Closes `DG-U2`, `DG-U3`, `RW-U4`.

**Surface**

- Entry: 600 ms long-press anywhere on grid (mobile); **Edit** top-bar button (desktop).
- Visual: jiggle animation, `×` remove badge, drag handles on widgets. `prefers-reduced-motion` swaps jiggle for dashed outline.
- Drag/drop reposition; resize for widgets (v0 placeholder OK if widget hosting deferred).
- Collision detection: red outline + persistent banner; **Done** disabled while collisions exist.
- Exit: Done (PUT layout), Cancel/Escape (discard with confirm).
- Picker: **+** in top bar lists not-on-grid app shortcuts and hidden system tiles.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Vitest: enter via long-press timer + via button; collision detection; reduce-motion branch; PUT called on Done; PUT not called on Cancel. |
| **DEV** | Component family in `apps/hub/web/src/dashboard/edit/`; respects `--hearth-error`. |
| **VAL** | Tests; manual: rearrange + save + reload retains layout. |

---

### T-FR-0006-10 — `@kindling/mantle` package scaffold

**Type:** impl · **Deps:** none · **Order:** P0 · **Owner:** —

Sets up the package authored in this repo, published to npm.

**Surface**

- `packages/mantle/` with `package.json` (name `@kindling/mantle`, `"private": false`, `"sideEffects": ["**/*.css"]`).
- Build via `tsup` or Vite library mode → ESM + CJS + types.
- Exports map: `.` (components+hooks), `./tokens`, `./vanilla`, `./styles.css`.
- README + LICENSE.
- pnpm workspace inclusion.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Vitest: package builds; types pass `tsc --noEmit`; exports map resolves. |
| **DEV** | Package scaffold + token CSS file mirroring mantle-ui.md tokens. |
| **VAL** | `pnpm --filter @kindling/mantle build` succeeds in Docker. |

---

### T-FR-0006-11 — `@kindling/mantle` base components

**Type:** impl · **Deps:** T-FR-0006-10 · **Order:** P1 · **Owner:** —

**Surface**

`<Page>`, `<PageHeader>`, `<Card>`, `<Section>`, `<List>`, `<EmptyState>`, `<Button>`, `<IconButton>`, `<Input>`, `<TextArea>`, `<Select>`, `<Switch>`. All accessible (44pt iOS hit targets, focus rings, ARIA where relevant). `<Page>` consumes safe-area tokens.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Vitest + Testing Library: each component renders, axe-core finds no a11y violations, props produce expected variants. |
| **DEV** | Components + Tailwind-flavored styling using tokens. |
| **VAL** | Tests pass in Docker. |

---

### T-FR-0006-12 — `@kindling/mantle` hooks

**Type:** impl · **Deps:** T-FR-0006-10, T-FR-0006-03 (postMessage contract types) · **Order:** P1 · **Owner:** —

**Surface**

`useMantle`, `useTheme`, `useUser`, `useChromeSlot`, `useHaptics`, `useNotifications`, `useSpark` (stub returning `{available: false}` until a later FR wires hub-proxied Spark). Each hook delegates to the postMessage bridge via shared types.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Vitest: each hook subscribes/unsubscribes correctly; origin guard; useChromeSlot mount/update/unmount round-trip. |
| **DEV** | Hooks + shared `types.ts` (`ChromeButton`, `ChromeMenu`, `FrameState`, `ThemeTokens`). |
| **VAL** | Tests pass. |

---

### T-FR-0006-13 — `@kindling/mantle` overlays

**Type:** impl · **Deps:** T-FR-0006-10, T-FR-0006-12 · **Order:** P2 · **Owner:** —

`<Sheet>`, `<Toast>`, `<Dialog>` that visually escape the iframe via postMessage. `<Toast>` is a stub for `DG-U11` — it accepts and console-logs in v0; shell-side rendering deferred.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Vitest: `<Sheet>`/`<Dialog>` open/close emits postMessage; `<Toast>` no-throw. |
| **DEV** | Components + fallback in-iframe rendering when shell ignores (graceful). |
| **VAL** | Tests; manual smoke. |

---

### T-FR-0006-14 — `@kindling/mantle` vanilla bridge

**Type:** impl · **Deps:** T-FR-0006-10, T-FR-0006-03 · **Order:** P1 · **Owner:** —

`vanilla/theme.ts` (`mantle.theme.subscribe(cb)`) and `vanilla/chrome.ts` (`mantle.chrome.mount(...)`) for non-React plugins. Same origin guard rules.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Vitest with jsdom; verify theme listener updates `:root` vars; chrome.mount/unmount round-trips. |
| **DEV** | TypeScript modules; UMD/IIFE build for `<script>`-tag plugins. |
| **VAL** | Tests pass. |

---

### T-FR-0006-15 — `@kindling/mantle` package validation

**Type:** release · **Deps:** 10–14 · **Order:** P3 · **Owner:** —

**Surface**

- `pnpm changeset` (or simple manual versioning) configured.
- Package remains private in this repo for now; no public npm publish.
- GitHub Actions validates a package artifact dry-run when a tag `kindling-mantle-vX.Y.Z` is pushed.
- CHANGELOG.md seeded with v0.1.0 entry.
- README documents install + minimal example pointing at kindling's `plugin-ui-system.md`.

**Phases**

| Phase | Acceptance |
|-------|------------|
| **TEST** | Package artifact dry-run in CI green. |
| **DEV** | Workflow + docs + version. |
| **VAL** | Public npm publish explicitly deferred; kindling and grocery-list consume the local/private package path until publish policy changes. |
