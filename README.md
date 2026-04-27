# Hearth

**Your home's productivity hub — vibe-coded, encrypted, yours.**

Hearth is a self-hosted personal productivity platform that runs on a Raspberry Pi or Mac mini. It hosts a constellation of small "vibe-coded" lifestyle apps (groceries, scheduler, recipes, idea catcher, …) behind a single Caddy reverse proxy, a shared UI shell, and a discoverable app-to-app API. Each app is its own project that opts into the platform via a manifest; Hearth gives them a home, a chrome, an identity, and a way to talk.

The **primary client is an iPhone PWA** added to the Home Screen — Mantle ships a manifest, a service worker, bottom-tab navigation, and Web Push so the result feels native. Desktop browsers and Android work too (the layout is responsive). Phase-2 **Ember** brings e2e-encrypted access from anywhere; until then, Hearth lives on your LAN with a locally-trusted TLS cert.

## The constellation

| Name | Role | State |
|------|------|-------|
| **Hearth** | Hub: gateway, plugin loader, registry, dashboard, settings | This repo |
| **Mantle** | Shared React shell + design system (theme, nav chrome, auth widget) | Lives in **Kindling** |
| **Spark** | App-to-app API: discovery, capability surface, RPC, event bus | Spec in [`docs/design/spark-api.md`](docs/design/spark-api.md); client lib lives in **Kindling** |
| **Tinder** | Plugin manifest format (declares routes, capabilities, deps, permissions) | Spec in [`docs/design/plugin-contract.md`](docs/design/plugin-contract.md) |
| **Kindling** | Shared template repo: scaffold for new plugin apps, Mantle component library, Spark client lib, dev tooling | Separate repo, **planned** as `git@github.com:mcelhennyi/kindling.git`; see [`docs/design/satellite-repos/kindling.md`](docs/design/satellite-repos/kindling.md) |
| **Ember** | Phase-2 relay server: e2e-encrypted access from anywhere, identity, optional cloud-storage backup providers | Sketch in [`docs/design/satellite-repos/ember.md`](docs/design/satellite-repos/ember.md); not in MVP |

## Logo (working concept)

A geometric flame inside an arch (the hearth opening). Kept abstract enough to scale to a 16px favicon and recolor for plugin badges.

![Hearth logo](docs/design/logo.svg)

Source SVG lives at [`docs/design/logo.svg`](docs/design/logo.svg). Copy it to `apps/hub/web/public/logo.svg` once the hub app is scaffolded (ticket **`T-FR-0001-02`**).

## Documentation

- **System architecture:** [`docs/design/architecture/overview.md`](docs/design/architecture/overview.md)
- **Plugin contract (Tinder):** [`docs/design/plugin-contract.md`](docs/design/plugin-contract.md)
- **App-to-app API (Spark):** [`docs/design/spark-api.md`](docs/design/spark-api.md)
- **Shared UI (Mantle):** [`docs/design/mantle-ui.md`](docs/design/mantle-ui.md)
- **Deployment topology:** [`docs/design/deployment.md`](docs/design/deployment.md)
- **Notifications (Web Push + ntfy):** [`docs/design/notifications.md`](docs/design/notifications.md)
- **Native plugin ideas:** [`docs/design/native-plugin-ideas.md`](docs/design/native-plugin-ideas.md)
- **Roadmap (Phase 2 / Phase 3 / research):** [`docs/design/roadmap.md`](docs/design/roadmap.md)
- **Satellite repos (Kindling, Ember):** [`docs/design/satellite-repos/`](docs/design/satellite-repos/)
- **AI workflow notes:** [`docs/ai-context.md`](docs/ai-context.md)
- **Active feature:** [`tasks/feature-history/FR-0001-hearth-platform/`](tasks/feature-history/FR-0001-hearth-platform/)

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Hub gateway / plugin loader | **Python 3.12 + FastAPI** | Async, strong typing, fits the small-but-real-server target on Pi |
| Plugin backends | **Python (default)**, **C++** for hot paths (later) | Same justification; C++ reserved for media/ML-style background services |
| UIs (hub + plugins) | **React 18 + TypeScript + Vite** | Standard, fast HMR, large ecosystem; shipped via Mantle |
| Component library / shell | **Mantle** (Tailwind + shadcn/ui) | One look across all plugins; shipped from Kindling |
| Reverse proxy | **Caddy 2.x** (default) — auto local TLS via `tls internal`; nginx supported as alternative | Routes `/<plugin-slug>/...` → plugin process; HTTPS is required for the iPhone PWA + Web Push |
| PWA shell | **Vite-PWA** (manifest + service worker), bottom-tab nav on mobile | "Add to Home Screen" → standalone full-screen, offline-aware |
| Notifications | **Web Push** (iOS 16.4+, requires PWA installed) with **ntfy** as a hobbyist fallback | Spec in [`docs/design/notifications.md`](docs/design/notifications.md) |
| Persistence (hub) | **SQLite** (single file under `var/hearth/`) | Plugin registry, settings, user prefs; trivial to back up |
| Persistence (plugins) | Plugin's choice (SQLite default) | Plugins own their data; surfaced via Spark capabilities |
| Process supervision | **systemd** (Pi/Mac mini) or **Docker Compose** (dev) | Match the deploy target |

Detail: [`.cursor/rules/stack-conventions.mdc`](.cursor/rules/stack-conventions.mdc).

## Traceability prefix

Inline tags use **`@HRT-<AREA>-<NUMBER>`**. Areas: `HUB`, `MNTL`, `SPRK`, `TNDR`, `KDLG`, `EMBR`, `IDM`, `OPS`, `DOC`. See [`docs/design/documentation-style.md`](docs/design/documentation-style.md).

## Development

The repo is in **design** phase — no buildable scaffold yet. The first ticket that produces runnable code is **`T-FR-0001-02`** (Hub app skeleton + dev-loop Compose); see [`tasks/feature-history/FR-0001-hearth-platform/tickets.md`](tasks/feature-history/FR-0001-hearth-platform/tickets.md).

When the scaffold lands, prefer:

```bash
./develop help
```

Development commands (build, test, lint, dev servers) run inside Docker Compose by default; host-local execution is documented in ticket diaries as exceptions.

## Project skeleton

This repository was initialized from the [process skeleton](.skeleton/INIT.MD). Template sources live in `.skeleton/` (git submodule). Run `./sync-skeleton` when you intentionally want upstream process/tooling updates.

## License

Private / unpublished. Update before the first public push.
