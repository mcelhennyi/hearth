# Mantle — shared PWA shell

**Authority:** This document defines the shared React shell every Hearth UI lives inside, and the design tokens / primitives plugins consume from the **Kindling** templates package.

The primary client is an **iPhone PWA** added to the Home Screen. Mantle is therefore a Progressive Web App by default: it ships a manifest, a service worker, an offline-aware app shell, and a layout that adapts between bottom-tab nav (mobile/standalone) and top-bar nav (desktop browser).

## Goals

1. **One look — and a native feel on iPhone.** Tabs at the bottom, big tap targets, safe-area-aware, no Safari chrome once installed.
2. **One auth flow.** Plugins do not implement login screens — the shell handles it.
3. **One nav.** Switching plugins from the tab bar is instant and does not bounce the user out of standalone mode.
4. **No fork-and-skin.** A theme change in Hearth propagates to every plugin without each plugin redeploying.

## PWA wiring

| Surface | What it is | Where it lives |
|---------|-----------|-----------------|
| `manifest.webmanifest` | App identity (name, icons, `start_url:"/"`, `display:"standalone"`, `theme_color`, `scope:"/"`, `id:"hearth"`) | `apps/hub/web/public/manifest.webmanifest` |
| App icons | 180×180 (Apple touch icon), 192/512 PNG, maskable variants | `apps/hub/web/public/icons/` |
| Service worker | Vite-PWA generated; caches the shell, falls back to a cached "offline" page; **does not** cache plugin iframes (those are handled by their own SW if they ship one) | `apps/hub/web/src/sw.ts` |
| `<head>` meta | `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style=black-translucent`, `viewport-fit=cover`, `theme-color` matching token `--hearth-bg` | `apps/hub/web/index.html` |

The manifest's `display: standalone` plus the Apple meta tag is what lets "Add to Home Screen" launch Hearth without any browser UI.

iPhone Safari requires **HTTPS** for service workers and Web Push. Hearth's reverse proxy (Caddy) issues a local CA cert for `hearth.local`; the cert must be trusted on the iPhone via a profile install. See [`deployment.md`](deployment.md) for the one-time trust steps.

## Layout

### Desktop / wide (`min-width: 768px`)

```
+---------------------------------------------------------------+
|  Mantle Top Bar  [logo]  Dashboard  Groceries  Recipes  +     |
|                                                Settings  User |
+---------------------------------------------------------------+
|  Plugin Frame                                                 |
|  +---------------------------------------------------------+  |
|  |   <plugin's own UI>                                     |  |
|  +---------------------------------------------------------+  |
+---------------------------------------------------------------+
|  Mantle Status Strip   notifications • spark events • health  |
+---------------------------------------------------------------+
```

### Mobile / installed PWA (`max-width: 767px`)

```
+--------------------------------------+
|  Hearth   Groceries           [user] |   <- compact title bar (safe-area top)
+--------------------------------------+
|                                      |
|   <plugin's own UI>                  |
|                                      |
|                                      |
+--------------------------------------+
|  [🏠]  [🛒]  [🍳]  [💡]  [⚙️]        |   <- bottom-tab nav (safe-area bottom)
+--------------------------------------+
```

The tab bar is the **canonical mobile nav**: one icon per enabled plugin (ordered by `tinder.toml` `[ui.nav].order`), with overflow into a "More" sheet beyond the first 4. Long-press on a tab is reserved for plugin actions in a future iteration.

## Embed strategy (MVP)

**iframe per plugin.** The shell serves `/` and renders `/<slug>/` inside an iframe inside the Plugin Frame.

| Pro | Contra |
|-----|--------|
| Hard isolation — a crashing plugin cannot brick the shell. | Each plugin ships its own JS bundle. |
| Plugins ship any tech they want for the UI (Vue, Svelte, plain HTML). | Cross-frame nav requires a small `postMessage` protocol. |
| Auth header injection is uniform via the proxy. | iOS quirks: deep-link state and back-button behavior need explicit handling (the shell intercepts back). |

**Module Federation** (one bundle, zero-cost nav) is the upgrade path post-MVP. The PWA shell is designed so the swap is internal — plugin authors do not change their UI code.

### postMessage protocol (shell ↔ plugin iframe)

| Direction | Message | Purpose |
|-----------|---------|---------|
| shell → plugin | `{type:"hearth.theme", tokens}` | push theme on change |
| shell → plugin | `{type:"hearth.user", user}` | push user info |
| shell → plugin | `{type:"hearth.online", online}` | network state |
| plugin → shell | `{type:"hearth.title", title}` | suggested page title for the tab |
| plugin → shell | `{type:"hearth.toast", level, message}` | show a global toast |
| plugin → shell | `{type:"hearth.nav", path}` | request shell-level nav |
| plugin → shell | `{type:"hearth.haptic", style}` | request a tap-haptic (iOS PWA only) |
| plugin → shell | `{type:"hearth.notify", payload}` | request a push (delegated to hub; see `notifications.md`) |

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
- `useMantle()`, `useUser()`, `useTheme()`, `useSpark()`, `useHaptics()`, `useNotifications()` — hooks for the shell contract.

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

A plugin **must not** render a top-level navigation bar of its own (the shell owns the chrome). Within the plugin frame, anything goes — sidebars, tabs, command palettes, whatever the plugin needs.

## Offline behavior

- Shell HTML, CSS, JS, and icons are precached by the service worker.
- The dashboard route renders a cached snapshot of the last seen plugin list when offline.
- Plugin iframes that don't ship their own SW show a cached "offline" placeholder — they can opt in to their own SW via a Tinder field (not in MVP).
- Spark calls fail loudly when offline; UIs should show "waiting to reconnect" rather than spinning forever.

## Install prompt

On the dashboard, when the user agent matches iOS Safari (and the app isn't already installed), Mantle shows a one-time tip pointing at Share → Add to Home Screen with a small animation. Dismissed permanently after first install or explicit dismiss.
