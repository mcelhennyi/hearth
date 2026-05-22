# Changelog

All notable changes to `@kindling/mantle` are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-05-21

Initial public release from the [hearth](https://github.com/mcelhennyi/hearth) monorepo (`packages/mantle`). Implements FR-0006 design-language tickets T-FR-0006-10 through T-FR-0006-14.

### Added

- **Tokens** — `@kindling/mantle/tokens` and `@kindling/mantle/styles.css` (`--hearth-*` CSS custom properties).
- **Component styles** — `@kindling/mantle/components.css`.
- **React components** — `Page`, `PageHeader`, `Card`, `Section`, `List`, `EmptyState`, `Button`, `IconButton`, `Input`, `TextArea`, `Select`, `Switch`, `Sheet`, `Dialog`, `Toast`.
- **React hooks** — `useMantle`, `useTheme`, `useUser`, `useChromeSlot`, `useHaptics`, `useNotifications`, `useSpark` (stub until hub-proxied Spark ships).
- **Overlays** — `Sheet`, `Dialog`, and `Toast` (v0 posts to shell via postMessage; shell-side toast rendering deferred).
- **Vanilla bridge** — `@kindling/mantle/vanilla` (`mantle.theme.subscribe`, `mantle.chrome.mount`) plus IIFE build at `@kindling/mantle/vanilla/mantle.iife`.
- **Types** — `@kindling/mantle/types` for postMessage envelopes and chrome payloads.

[0.1.0]: https://github.com/mcelhennyi/hearth/releases/tag/kindling-mantle-v0.1.0
