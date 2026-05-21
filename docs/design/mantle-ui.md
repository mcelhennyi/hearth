# Mantle — shared PWA shell

**Authority:** This document defines the shared React shell every Hearth UI lives inside — **behavior, chrome zones, and contracts** (logical). **Layout and visual design language** (proportions, spacing, color as rendered, responsive chrome) are authoritative in **[`mockups/`](mockups/README.md)** (static HTML/CSS). The **home dashboard** grid (block types, persistence, widget model) is in [`dashboard.md`](dashboard.md).

The primary client is an **iPhone PWA** added to the Home Screen. Mantle is therefore a Progressive Web App by default: it ships a manifest, a service worker, an offline-aware app shell, and a layout that adapts between bottom-tab nav (mobile/standalone) and top-bar nav (desktop browser).

## Goals

1. **One look — and a native feel on iPhone.** Tabs at the bottom, big tap targets, safe-area-aware, no Safari chrome once installed.
2. **One auth flow.** Plugins do not implement login screens — the shell handles it.
3. **One app chrome.** The top and bottom bars use the **same structure** on the dashboard and inside every **app** plugin so Hearth feels like a single app; plugins **extend** bars via declared slots, they do not replace them.
4. **No fork-and-skin.** A theme change in Hearth propagates to every plugin without each plugin redeploying.
5. **Registry-driven chrome.** The shell **never** hardcodes plugin slugs, labels, or routes. Tab bar and dashboard shortcuts come from **`GET /api/plugins`** (enabled **`app`** plugins only). With zero plugins installed, the user sees **Home** and **Settings** only—see [`architecture/overview.md`](architecture/overview.md#1b-plugin-agnosticism-hub-boundary).

## PWA wiring

| Surface | What it is | Where it lives |
|---------|-----------|-----------------|
| `manifest.webmanifest` | App identity (name, icons, `start_url:"/"`, `display:"standalone"`, `theme_color`, `scope:"/"`, `id:"hearth"`) | `apps/hub/web/public/manifest.webmanifest` |
| App icons | 180×180 (Apple touch icon), 192/512 PNG, maskable variants | `apps/hub/web/public/icons/` |
| Service worker | Vite-PWA generated; caches the shell, falls back to a cached "offline" page; **does not** cache plugin iframes (those are handled by their own SW if they ship one) | `apps/hub/web/src/sw.ts` |
| `<head>` meta | `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style=black-translucent`, `viewport-fit=cover`, `theme-color` matching token `--hearth-bg` | `apps/hub/web/index.html` |

The manifest's `display: standalone` plus the Apple meta tag is what lets "Add to Home Screen" launch Hearth without any browser UI.

iPhone Safari requires **HTTPS** for service workers and Web Push. Hearth's reverse proxy (Caddy) issues a local CA cert for `hearth.home.arpa`; the cert must be trusted on the iPhone via a profile install. See [`deployment.md`](deployment.md) for the one-time trust steps.

## Shell modes

| Mode | Route | Main content |
|------|-------|----------------|
| **Dashboard** | `/` | User-editable **grid** of blocks ([`dashboard.md`](dashboard.md)) — per-plugin **app icons** and/or **widgets**, system tiles |
| **App** | `/<slug>/…` | Plugin UI in the **plugin frame** (iframe for MVP) |

Chrome (top + bottom bars) stays **mounted** across mode changes so navigation does not flash or reset safe-area layout.

## Layout and visual mocks

Do **not** use ASCII layout diagrams in this doc for spatial reference. Open the linked HTML mocks in a browser — see **[`mockups/README.md`](mockups/README.md)** for the full index.

| Viewport | Shell mode | Canonical mock |
|----------|------------|----------------|
| iPhone | Dashboard `/` | [`mockups/dashboard-iphone.html`](mockups/dashboard-iphone.html) |
| Desktop (≥768px) | Dashboard `/` | [`mockups/dashboard-desktop.html`](mockups/dashboard-desktop.html) |
| iPhone | App `/<slug>/` (shell only) | [`mockups/mantle-iphone-bare.html`](mockups/mantle-iphone-bare.html) |
| Desktop | App `/<slug>/` (shell only) | [`mockups/mantle-desktop-bare.html`](mockups/mantle-desktop-bare.html) |
| iPhone | App + example plugin UI | [`mockups/mantle-iphone-groceries.html`](mockups/mantle-iphone-groceries.html) (reference plugin) |
| Desktop | App + example plugin UI | [`mockups/mantle-desktop-groceries.html`](mockups/mantle-desktop-groceries.html) (reference plugin) |

Shared Mantle mock stylesheet: [`mockups/mantle-mock.css`](mockups/mantle-mock.css).

### Chrome regions (logical)

| Region | Dashboard | App `/<slug>/` |
|--------|-----------|----------------|
| **Top bar** | Flame (inactive), title “Hearth”, user; **Settings** text control on desktop (opens modal — see desktop dashboard mock) | Leading **Home** control, plugin title (`hearth.title`), optional **`[ui.chrome].top`** slots, user |
| **Main frame** | Dashboard grid ([`dashboard.md`](dashboard.md)) — no iframe | Plugin **iframe** (MVP) |
| **Bottom bar** | Fixed to viewport bottom (not a floating dock). **Home** pinned left; **app launcher** scrolls horizontally in the center; **Settings** pinned right | Same fixed bar. **Home** pinned left; **center is plugin bottom chrome slots only** — **no other app tabs**; **Settings** pinned right |

Breakpoint: **768px** — below = mobile/PWA chrome; at/above = desktop chrome (top bar includes text Settings on dashboard; bottom bar uses horizontal app pills on desktop per mocks).

### Bottom bar — nav policy

| Zone | Dashboard (`/`) | App (`/<slug>/`) |
|------|-----------------|------------------|
| **Left (pinned)** | **Home** — active | **Home** — returns to `/` |
| **Center** | **App launcher** — one control per enabled **`app`** plugin with `ui.nav.show_in_tab_bar` (default true), ordered by `[ui.nav].order`; horizontally scrollable when overflow | **Plugin bottom slots** only — content from `[ui.chrome].bottom` via `hearth.chrome.mount` |
| **Right (pinned)** | **Settings** | **Settings** |

#### Desktop vs mobile bottom-bar styling (normative)

| Aspect | Mobile (<768 px) | Desktop (≥768 px) |
|--------|------------------|-------------------|
| Home left control | **Tab button** (`.nav-tab`) with icon + label; active state highlights `--hearth-accent` | **Plain link** (`.shell-home-link`) with text "Home"; underline-on-hover |
| Launcher items | **Icon tabs** with truncated label below | **Pill chips** (icon + label inline) |
| Settings right control | **Icon-only** button (gear) | **Icon + text** "Settings" button |
| Plugin bottom slots (app mode) | Right-aligned flex group of icon buttons | Same buttons + visible text labels |

| Item | Behavior |
|------|----------|
| **Settings (desktop)** | **Top bar** and **bottom bar** both expose Settings; either opens the same **floating modal** over the shell (see [`mockups/dashboard-desktop.html`](mockups/dashboard-desktop.html)). |
| **Settings (mobile)** | **Icon-only** control in the pinned right zone (see [`mockups/dashboard-iphone.html`](mockups/dashboard-iphone.html)). |
| **REFINEMENT R-U2** | When many app plugins are enabled, v0 uses a **scrollable** center strip with edge fade (mocks), not a separate overflow sheet. |

Long-press on a launcher tab is reserved for plugin actions in a future iteration.

## Chrome contract

The shell owns a **fixed skeleton** on every screen. Plugins supply **slot content** only; they cannot remove Home, user menu, or settings access.

### Top bar zones (left → right)

| Zone | Owner | Dashboard | App (`/<slug>/`) |
|------|-------|-----------|------------------|
| **Leading** | Shell | Hearth flame (inactive) | **Home** chevron or flame — tap returns to `/` |
| **Title** | Shell | “Hearth” or user-defined dashboard title | Plugin title via `hearth.title` postMessage |
| **Center / trailing slots** | Plugin (optional) | Empty | Content from `[ui.chrome].top.slots` |
| **User** | Shell | Account / sign-out | Same |

### Bottom bar zones (left → right)

| Zone | Owner | Dashboard | App |
|------|-------|-----------|-----|
| **Launcher / slots** | Shell (dashboard) / Plugin (app) | Home active + scrollable **app launcher** | Home inactive; center = **`[ui.chrome].bottom` only** (no cross-app tabs) |
| **Top chrome slots** | Plugin (optional) | Empty | `[ui.chrome].top` — e.g. actions, add |
| **Settings** | Shell | Visible (icon or text per viewport) | Visible |

Visual rules: same height, background (`--hearth-surface`), border, and typography in both modes so switching dashboard ↔ app feels like one operating system, not a browser with a random header per site.

### Declaring chrome slots (app plugins) (`DG-U6` closed 2026-05-21)

In `tinder.toml`:

```toml
[ui.chrome]
top    = { slots = ["actions"] }
bottom = { slots = ["primary"] }
```

At runtime the plugin iframe registers slot content via postMessage:

| Direction | Message | Purpose |
|-----------|---------|---------|
| plugin → shell | `{type:"hearth.chrome.mount", slot, surface, payload}` | Register slot UI |
| plugin → shell | `{type:"hearth.chrome.unmount", slot, surface}` | Remove slot UI |
| shell → plugin | `{type:"hearth.chrome.resize", slot, rect}` | Optional layout hint |

**Payload shape (v0).** Plugins may register two shapes only; arbitrary React subtrees are deferred behind module-federation (post-MVP).

```ts
type ChromeButton = {
  kind: "button";
  id: string;                   // stable id within slot+surface; used for unmount
  label: string;                // accessible name (also used in overflow menu)
  icon?: string;                // lucide icon name (preferred) or data: URL <= 4 KB
  variant?: "default" | "accent";  // accent = primary action color
  busy?: boolean;               // shows a small spinner overlay
  disabled?: boolean;
};

type ChromeMenu = {
  kind: "menu";
  id: string;
  label: string;
  icon?: string;
  items: Array<{ id: string; label: string; icon?: string; disabled?: boolean }>;
};
```

The plugin sends `payload: ChromeButton | ChromeMenu`. When the user activates a slot item the shell echoes back `{type:"hearth.chrome.invoke", slot, surface, id, itemId?}` so the plugin can act.

**Indexing and ordering.** Within a slot, items render in **first-mount-first** order. A plugin may mount the same `id` again with new fields to update it (same id is a replace, not a duplicate). Unmount uses `(slot, surface, id)` triple.

**Max visible per slot.**

| Slot | Visible cap | Overflow |
|------|-------------|----------|
| `top` | **3** items per plugin | Items 4+ collapse into a single `⋯` menu using the items' `label`s. |
| `bottom` | **4** items per plugin | Items 5+ collapse into a single `⋯` menu. |

Items always reflow before the shell's pinned Home / user / Settings controls. **No** plugin may push more than 8 items to a single slot in total; excess registrations are rejected (shell sends `{type:"hearth.chrome.error", slot, surface, reason:"limit"}`).

**Lifecycle.** All slot registrations are cleared automatically when the plugin iframe unloads or the user navigates away from `/<slug>/` (the shell sends `hearth.chrome.unmount` implicitly for every mounted id on route change).

**Widget** plugins do not use chrome slots (they render only inside dashboard blocks).

### What plugins must not do

- Render a **second** top or bottom bar inside the iframe that duplicates shell zones (violates “one app” feel).
- Hide or overlay shell chrome.
- Replace Home or settings.

In-frame navigation (tabs, sidebars, toolbars **below** the title area) remains the plugin’s choice — see Plugin chrome rules.

## Embed strategy (MVP)

**iframe per app plugin.** The dashboard at `/` is **shell-native** (no iframe). **`app`** plugins render at `/<slug>/` inside an iframe in the main frame.

| Pro | Contra |
|-----|--------|
| Hard isolation — a crashing plugin cannot brick the shell. | Each plugin ships its own JS bundle. |
| Plugins ship any tech they want for the UI (Vue, Svelte, plain HTML). | Cross-frame nav requires a small `postMessage` protocol. |
| Auth header injection is uniform via the proxy. | iOS quirks: deep-link state and back-button behavior need explicit handling (the shell intercepts back). |

**Module Federation** (one bundle, zero-cost nav) is the upgrade path post-MVP. The PWA shell is designed so the swap is internal — plugin authors do not change their UI code.

### Plugin frame states (`DG-U7` closed 2026-05-21)

The plugin frame is never empty. It always renders one of five states:

| State | Trigger | Shell UI |
|-------|---------|----------|
| **Mounted** | iframe `load` event fired and the plugin has sent at least one of `hearth.title` or `hearth.ready` within **5 s** | Plugin renders normally; loading scrim removed. |
| **Loading** | Frame just navigated; no `load` event yet, or no plugin ack within 5 s | Centered shell spinner (`--hearth-accent`) over the plugin background; shell renders plugin title from registry while waiting. |
| **Slow** | After **5 s** still no `load` | Spinner persists; subtle subtitle "Still loading {plugin}…". After **15 s** offers a **Reload** action. |
| **Error** | iframe fires `error`, or the proxy returns 4xx/5xx, or the frame violates sandbox | Centered "{plugin} failed to load" card with **Reload** and **Open Settings** actions; cause shown in collapsible details (HTTP status, last log line). |
| **Offline** | Browser `navigator.onLine === false` when entering the plugin route, or the SW returned a cached fallback | Centered "You're offline" card with the last-cached plugin title; **Try again** button. |

State transitions are reported to the plugin (when reachable) via `{type:"hearth.online", online}`; the shell also pushes `{type:"hearth.frame.state", state}` so the plugin can self-suppress overlays when the shell is showing one.

### Settings modal (`DG-U8` closed 2026-05-21)

Settings is a **floating modal** over the shell, not a separate route. Both the desktop top-bar text button and the desktop+mobile bottom-bar Settings icon open the same modal.

| Aspect | Specification |
|--------|---------------|
| Trigger | Top-bar **Settings** (text, desktop dashboard only) **or** bottom-bar Settings (icon, all viewports, both modes). |
| Container | Modal centered on desktop (max-width **640px**, max-height **80vh`); full-screen sheet on mobile (slides up from bottom; close handle at top). |
| Surface | `--hearth-surface`; backdrop `color-mix(in srgb, var(--hearth-bg) 70%, transparent)`. |
| Close | Escape, backdrop tap, system back gesture (mobile), explicit Done button. |
| Tabs (v0) | **Theme**, **Plugins**, **System tiles**, **Diagnostics**, **Sign out**. |
| Theme tab | Light / Dark / **System** radio group. Selection persists via `localStorage` key `hearth.theme.preference` and is mirrored to a server-side user preference (`PUT /api/user/preferences`). On change the shell updates the `theme-color` meta tag and broadcasts `hearth.theme` to every mounted plugin iframe. |
| Plugins tab | List of enabled/disabled `app` and `widget` plugins; toggles call `POST /api/plugins/<slug>/{enable,disable}`. |
| System tiles tab | Show / hide the dashboard's `system` block tiles (see [`dashboard.md`](dashboard.md#system-block--content-and-configuration-df-u1-closed-2026-05-21)). |
| Diagnostics tab | Hub health, CA trust status, hub uptime; links to the FR-0003 `hearth doctor` output where available. |
| Sign out | Calls `POST /api/auth/logout` and reloads the shell. |

**Reduced-motion:** The desktop modal fades in (160 ms) instead of scaling; the mobile sheet snaps without spring animation.

### Theme persistence

The user's theme preference (`hearth.theme.preference` in `localStorage`) is the **source of truth at boot**; it is reconciled with the server preference (`GET /api/user/preferences`) after first paint to avoid theme flash. When `preference = "system"`, the shell tracks `prefers-color-scheme` live and re-broadcasts `hearth.theme` on change.

### Desktop nav surface — no floating dock (`DF-U3` closed 2026-05-21)

The desktop shell **does not** render a macOS-style floating dock. The bottom bar fixed to the viewport is the only navigation surface in both modes. Any `.dock-layer` content visible in earlier mock revisions is **non-normative** and to be removed from `mockups/mantle-desktop-*.html`. See [`mockups/README.md`](mockups/README.md).

### postMessage protocol (shell ↔ plugin iframe)

| Direction | Message | Purpose |
|-----------|---------|---------|
| shell → plugin | `{type:"hearth.theme", tokens}` | push theme on change |
| shell → plugin | `{type:"hearth.user", user}` | push user info |
| shell → plugin | `{type:"hearth.online", online}` | network state |
| plugin → shell | `{type:"hearth.title", title}` | **`DG-U9` closed:** updates **both** the browser tab title (`document.title = "{title} — Hearth"`) **and** the shell top-bar title in App mode. Dashboard ignores plugin-set titles. |
| plugin → shell | `{type:"hearth.toast", level, message}` | **`DG-U11`** — show a global toast (placement, duration, styles deferred to first overlay implementation; until then the shell silently accepts and console-logs) |
| plugin → shell | `{type:"hearth.nav", path}` | request shell-level nav |
| plugin → shell | `{type:"hearth.haptic", style}` | **`DG-U11`** — request a tap-haptic (iOS PWA only; supported styles `selection` / `impact` / `notification`; non-iOS callers no-op) |
| plugin → shell | `{type:"hearth.notify", payload}` | request a push (delegated to hub; see `notifications.md`) |
| plugin → shell | `{type:"hearth.chrome.mount", …}` / `hearth.chrome.unmount` | slot UI in top/bottom bars (see Chrome contract) |

A Mantle hook `useMantle()` (TS) exposes this; plugins authored from Kindling already wire it up.

## Theme tokens

CSS custom properties defined at `:root` by Mantle. Plugins MUST consume these and MUST NOT hardcode brand colors.

| Token | Default | Purpose |
|-------|---------|---------|
| `--hearth-bg`             | `#0f1115` (dark) / `#fafafa` (light) | Plugin frame background |
| `--hearth-surface`        | `#161a22` / `#ffffff` | Cards, modals |
| `--hearth-fg`             | `#e6e6e6` / `#111111` | Body text |
| `--hearth-muted`          | `#9aa3b2` / `#6b7280` | Secondary text |
| `--hearth-accent`         | `#ff6a3d` (ember orange) | Primary actions, the flame |
| `--hearth-accent-fg`      | `#0f1115` | Text on accent |
| `--hearth-radius-sm/md/lg`| `4px / 8px / 16px` | Radii |
| `--hearth-font-sans`      | `-apple-system, Inter, system-ui, sans-serif` | Default UI font |
| `--hearth-safe-top/bottom`| `env(safe-area-inset-*)` | iOS notch / home-indicator |

A user setting toggles light/dark/system; the chosen palette is pushed to plugins via the `hearth.theme` message and to the `theme-color` meta tag for the standalone status bar.

## Component primitives (shipped from Kindling)

Plugins import these from `@kindling/mantle`:

- `<Page>` `<PageHeader>` — layout primitives that pin to the shell's plugin frame and handle scroll + safe areas.
- `<Card>` `<Section>` `<List>` `<EmptyState>`.
- `<Button>` `<IconButton>` `<Input>` `<TextArea>` `<Select>` `<Switch>` — accessible form primitives, 44pt iOS hit targets.
- `<Sheet>` `<Toast>` `<Dialog>` — overlays that escape the iframe via the postMessage protocol so they aren't clipped to plugin bounds.
- **Widget primitives** (dashboard only, post-MVP hosting): `<WidgetMetric>`, `<WidgetList>`, `<WidgetButton>` — render hub snapshot JSON; not used inside app iframes.
- `useMantle()`, `useUser()`, `useTheme()`, `useSpark()`, `useHaptics()`, `useNotifications()`, `useChromeSlot()` — hooks for the shell contract.

Underneath: Tailwind for layout, shadcn/ui as the primitive base, lucide-react for icons.

## Logo placement

- Top bar (desktop) and bottom-left of the title bar (mobile) use the **Hearth flame** SVG at 24×24.
- The accent color is the flame color. Plugins may render a tinted version of the flame as a "powered by Hearth" badge.

## Accessibility

- WCAG AA color contrast for the default light + dark palettes (CI check via `axe-core`).
- All interactive primitives have keyboard equivalents and focus rings.
- iOS VoiceOver: tab bar items are exposed as a `tablist` with proper roles.
- Plugins inherit `lang="en"` from the shell document; override only when localized.

## Plugin chrome rules

**App** plugins **must not** duplicate the shell’s top/bottom bar (see Chrome contract). Within the plugin frame, anything goes — sidebars, in-content tabs, command palettes, etc.

**Widget** plugins have no iframe and no chrome slots; they only appear as dashboard blocks.

## Offline behavior

- Shell HTML, CSS, JS, and icons are precached by the service worker.
- The dashboard renders a cached **layout + widget snapshots** when offline ([`dashboard.md`](dashboard.md)).
- Plugin iframes that don't ship their own SW show a cached "offline" placeholder — they can opt in to their own SW via a Tinder field (not in MVP).
- Spark calls fail loudly when offline; UIs should show "waiting to reconnect" rather than spinning forever.

## Install prompt

On the dashboard, when the user agent matches iOS Safari (and the app isn't already installed), Mantle shows a one-time tip pointing at Share → Add to Home Screen with a small animation. Dismissed permanently after first install or explicit dismiss.

## Related docs

- [`mockups/README.md`](mockups/README.md) — HTML/CSS visual mocks index (canonical layout reference).
- [`dashboard.md`](dashboard.md) — home grid, block types, layout persistence.
- [`plugin-contract.md`](plugin-contract.md) — `[ui.chrome]`, `[ui.nav]`, plugin kinds.
