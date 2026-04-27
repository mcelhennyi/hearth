# FR-0001 charter

## Problem we're solving

A single user (the project lead, expanding to family) wants to run small lifestyle apps — groceries, scheduler, recipes, idea catcher — on hardware they own (Pi or Mac mini), reach them from an iPhone PWA, and let those apps cooperate without each becoming its own service with its own login, design language, and deploy process.

Off-the-shelf platforms either (a) demand a SaaS subscription per app, or (b) are too generic (Home Assistant) and force the user to think about the platform, not the app. Hearth is intentionally narrow: **a hub for vibe-coded lifestyle apps**, with one chrome, one auth, one inter-app protocol, and one deploy story.

## Stakeholders

| Role | Person | What they care about |
|------|--------|----------------------|
| Lead / first user | Ian | Day-to-day usefulness; iPhone-first feel; quick path to add a new app on a Sunday afternoon. |
| Future household users | Family | Shared lists/calendar without thinking about networking. (Ember + multi-user; Phase 2.) |
| External developer agents | `../project_02` (Colony) | Stable plugin contract so generated apps slot in without manual rewiring. |

## MVP rationale (why these things, not others)

- **Hub + plugins** rather than monolith: writing a new lifestyle app should be a weekend project, not a quarter. The platform does the boring parts (auth, theme, nav, RPC, install) so vibe-coding can stay vibe-y.
- **Caddy + local TLS, iPhone PWA primary**: this is the single biggest "does it feel like an app on my phone?" decision. Without it, "added to Home Screen" still feels like a bookmark.
- **Spark over Unix sockets, not REST hops**: discovery + permissions + audit in one layer; later swappable for cross-host without changing plugin code.
- **One reference plugin (`groceries`)**: forces the platform contracts to be honest. A platform with no plugin is theory.
- **Skeleton submodule + Kindling submodule**: every plugin (and Hearth itself) gets the same process discipline and the same UI primitives — without copy-paste.

## Non-goals (and why they are out)

- **Ember relay / remote access / cloud backup.** Big surface, big crypto choices, big legal questions (especially the speculative mining angle in Phase 4). Belongs in a separate FR with its own design loop.
- **Multi-user with roles.** Useful, but every plugin then has to think about access checks. Single-user assumption keeps the contract simple; revisit when Ember pairs multiple devices for **the same** user first.
- **Notifications/AI/gamification/store/automation features** the original brief named. These are great Phase-3 features that *use* the platform; the platform isn't real until plugins can install, communicate, and render under one chrome.
- **C++ background services.** We will need them for some workloads (media, ML); none of the MVP plugins do.
- **A plugin marketplace.** Not until there are plugins worth marketing.

## Success looks like

A first-run video, two minutes long: clone a deploy repo on a Mac mini, run `./install.sh`, scan a QR on the dashboard from the iPhone, install the local CA cert (one-time), Add to Home Screen, see four tabs at the bottom (Dashboard, Groceries, Recipes-stub, Settings), add an item to groceries, get a Web Push when an inventory threshold trips. No part of that flow says "open Terminal, edit `nginx.conf`, …".

## What we're explicitly comfortable being wrong about

- **iframe-per-plugin** vs module federation: iframes win MVP because isolation is worth more than animation polish. We will likely revisit.
- **Spark over Unix sockets** vs HTTP-on-loopback: sockets avoid port management, but lose a few off-the-shelf debugging tools. Worth it for now.
- **Caddy** vs **nginx**: Caddy's `tls internal` is a feature we want; nginx is parity-supported but not the primary path. Production deployers can choose.
- **Single SQLite for the hub**: fine until it isn't. Migration to Postgres is a known later cost; not paying it now.
