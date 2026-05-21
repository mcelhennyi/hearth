# FR-0006 — Design skeleton (L0)

Public surfaces only. Behavior is in the **authoritative docs** referenced from each row; this file is the implementation-readiness checklist.

## API surfaces (hub)

| Endpoint | Method | Body / response | Closes |
|----------|--------|------------------|--------|
| `/api/dashboard/layout` | `GET` | `DashboardLayout` JSON (see [`docs/design/dashboard.md` § Layout persistence](../../../docs/design/dashboard.md#layout-persistence)). 200 always; returns the default layout if none persisted. | `RW-U1` |
| `/api/dashboard/layout` | `PUT` | `DashboardLayout` body; 200 on save, 409 if collisions detected server-side. | `RW-U1` |
| `/api/system/tiles` | `GET` | `{tiles: SystemTile[]}` — id, title, body, action target, suppressed flag. | `DF-U1` |
| `/api/system/tiles/<id>/hide` | `POST` | Body `{}`; 204. Records user-hide for this tile. | `DF-U1` |
| `/api/system/tiles/<id>/restore` | `POST` | Body `{}`; 204. Used by Settings → System tiles. | `DF-U1` |
| `/api/system/strips` | `GET` | `{strip: SystemStrip \| null}` — single active strip for current platform. | `DF-U2` |
| `/api/system/strips/<id>/dismiss` | `POST` | Body `{}`; 204. | `DF-U2` |
| `/api/user/preferences` | `GET` | `{theme: "light" \| "dark" \| "system", …}`. | `DG-U8` |
| `/api/user/preferences` | `PUT` | Body `{theme?: ...}`; merged on server. | `DG-U8` |

## Mantle shell — postMessage surface (consumer-side)

Closes `DG-U6`, `DG-U7`, `DG-U9`. Full contract: [`docs/design/mantle-ui.md` § postMessage protocol](../../../docs/design/mantle-ui.md#postmessage-protocol-shell--plugin-iframe).

Shell-side listeners to add (none exist today):

- `hearth.title` → set `document.title`, top-bar title in App mode.
- `hearth.theme` → never received from plugins; shell pushes only.
- `hearth.chrome.mount` / `hearth.chrome.unmount` / `hearth.chrome.invoke` echo.
- `hearth.haptic` → iOS Web APIs (no-op elsewhere).
- `hearth.toast` → console-log v0 (DG-U11 deferred).
- `hearth.online` → shell pushes on connectivity change.

Shell pushes to plugins:

- `hearth.theme` (on Settings change and on `prefers-color-scheme` change when preference = system).
- `hearth.user` (on session start and on Settings → Sign out).
- `hearth.online` (on `online`/`offline` browser events).
- `hearth.frame.state` (Mounted/Loading/Slow/Error/Offline).
- `hearth.chrome.resize` (optional layout hint).
- `hearth.chrome.invoke` (when user activates a slot item).

## `@kindling/mantle` package (authored in this repo, published from here)

Closes the #21 user decision (ship now).

Package surface:

```
@kindling/mantle
├── tokens/           # CSS file + JS exports for --hearth-* values
├── components/
│   ├── Page.tsx      # safe-area-aware page wrapper
│   ├── PageHeader.tsx
│   ├── Card.tsx, Section.tsx, List.tsx, EmptyState.tsx
│   ├── Button.tsx, IconButton.tsx
│   ├── Input.tsx, TextArea.tsx, Select.tsx, Switch.tsx
│   ├── Sheet.tsx     # routes via postMessage
│   ├── Toast.tsx     # routes via postMessage (DG-U11 stub OK)
│   └── Dialog.tsx
├── hooks/
│   ├── useMantle.ts  # umbrella: postMessage origin guard + dispatcher
│   ├── useUser.ts
│   ├── useTheme.ts   # current tokens + light/dark/system
│   ├── useSpark.ts   # hub-proxied Spark calls (later FR; v0 stub)
│   ├── useHaptics.ts
│   ├── useNotifications.ts
│   └── useChromeSlot.ts  # mount/unmount/update slot items
├── vanilla/
│   ├── theme.ts      # imperative theme listener for non-React plugins
│   └── chrome.ts     # imperative chrome.mount/unmount/invoke
└── types.ts          # ChromeButton, ChromeMenu, FrameState, etc.
```

Publish target: scoped npm package `@kindling/mantle`. v0 lives in `packages/mantle/` of the hearth repo and is published as part of this FR.

## Frontend (Mantle shell) surfaces to add

- `apps/hub/web/src/dashboard/Grid.tsx` — block grid renderer (closes `RW-U1`).
- `apps/hub/web/src/dashboard/blocks/{AppShortcut,Widget,System,Strip}.tsx`.
- `apps/hub/web/src/dashboard/EditMode.tsx` — jiggle/×/handles (closes `DG-U2`+`DG-U3`+`RW-U4`).
- `apps/hub/web/src/dashboard/EmptyState.tsx` (closes `DG-U4`).
- `apps/hub/web/src/shell/ChromeSlot.tsx` + `apps/hub/web/src/shell/usePostMessageBridge.ts` (closes `DG-U6`).
- `apps/hub/web/src/shell/PluginFrameStates.tsx` (closes `DG-U7`).
- `apps/hub/web/src/shell/SettingsModal.tsx` + tabs (closes `DG-U8`, `RW-U2`).
- `apps/hub/web/src/theme/ThemeProvider.tsx` + `localStorage` + server reconcile (closes `DG-U8` theme persistence).

## Out of scope (this skeleton)

- Widget hosting implementation (P3).
- Edit-mode picker UX beyond entry/visual treatment.
- Module federation embed swap.
- Overlay primitive implementation (toast UI, haptic library) — DG-U11 stays open.
