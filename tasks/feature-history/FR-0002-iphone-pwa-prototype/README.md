# FR-0002 — iPhone PWA prototype

**Status:** `in-progress`
**Owner:** project lead (Ian)
**Allocated:** 2026-04-27
**Relationship:** parks FR-0001 implementation while we de-risk the iPhone-PWA story end-to-end. FR-0001 design stays authoritative for MVP; this FR may produce **design amendments** to FR-0001 if reality disagrees.

## Charter (one sentence)

Prove that a Caddy-fronted, locally-trusted, manifest-and-service-worker React shell on a Pi/Mac mini at home can be added to the iPhone Home Screen and receive a Web Push notification — end-to-end, on a real device — before we invest in the plugin registry, Tinder loader, Spark broker, or Kindling repo split.

## Why prototype before MVP

The five biggest "does this even feel native?" risks all live in this slice:

1. **HTTPS on a LAN-only host** — Caddy `tls internal` on `hearth.home.arpa` actually working on iOS once the local CA is trusted.
2. **iPhone CA trust UX** — installing the local-CA profile and enabling full trust without losing users at "VPN & Device Management."
3. **Standalone launch** — `display: standalone` + Apple meta tags + `viewport-fit=cover` actually producing a no-Safari-chrome experience that handles the notch and home-indicator.
4. **Service worker installs** — Vite-PWA-built SW registers on the iPhone PWA after Add to Home Screen, survives a relaunch.
5. **Web Push** — VAPID-signed push from a Python service on a home box reaches Apple's `*.push.apple.com` endpoint, the SW receives it, `showNotification` renders.

If any of these break, every later FR-0001 ticket is paying interest on a wrong assumption. Spending one FR to land them in a vertical slice is cheap.

## In scope

1. **Caddy with `tls internal`** serving `https://hearth.home.arpa/` from a Compose stack — no plugin generation, no registry, just a static config.
2. **Static Mantle shell**: a Vite + React + TypeScript app served from a single FastAPI route or directly from Caddy. Manifest, service worker, app icons, theme tokens, bottom-tab nav placeholder (the tabs lead nowhere — this is a prototype). Apple meta tags. Safe-area CSS.
3. **iPhone CA trust workflow**: a documented, executed `./develop ca-export` path. Capture screenshots/notes about each iOS step.
4. **Web Push round-trip**: VAPID keypair, `POST /api/push/subscribe` endpoint, "Send test notification" button on the prototype home view, `notify.send` server-side function (no Spark broker — direct call inside the FastAPI process), service-worker `push` event handler that calls `showNotification`.
5. **Real-device walkthrough**: a documented, filmed run-through on a real iPhone (Ian's). Time it. Note every friction point.

## Out of scope

- Plugin loader, Tinder schema, plugin registry, Spark broker. None of FR-0001's tickets `T-FR-0001-02..-08`.
- Auth and identity beyond a single hard-coded session cookie (or no auth at all on a LAN-only prototype host).
- ntfy fallback. We're proving Web Push works; ntfy stays in FR-0001.
- Backup, install.sh for Pi/Mac mini, systemd units. The prototype runs in `./develop up` only.
- Kindling repo split. The shell is built directly under `apps/hub/web/` with no `vendor/kindling/` submodule.
- `groceries` plugin. The prototype's only "screen" is the test-notification button and the Mantle bottom-tab placeholder.

## Acceptance for FR-0002 close

A two-minute video shows, on Ian's actual iPhone, in this order:

1. `./develop up` brought the stack up on a Mac mini / Pi.
2. Safari at `https://hearth.home.arpa/` returns the Mantle shell with a green "PWA-ready" tile, no certificate errors (after CA trust is installed).
3. Share → Add to Home Screen.
4. Tap the icon — full-screen launch, no Safari chrome, status bar tinted to `--hearth-bg`, bottom-tab placeholder visible.
5. Grant notification permission.
6. Tap "Send test notification" — within ~3 seconds an iOS push lands; tapping it returns to the PWA.
7. Force-quit and relaunch — service worker cache means the shell still renders without network.

A short markdown report at `40-prototype-report.md` (created when the FR closes) summarizes what worked, what didn't, and lists every **DESIGN-FLAW** discovered against FR-0001's `mantle-ui.md`, `deployment.md`, and `notifications.md`. Those flaws become amendments before FR-0001 implementation resumes.

## Layered design

| Doc | Purpose |
|-----|---------|
| [`10-design/charter.md`](10-design/charter.md) | This charter expanded — what we expect to learn, what would invalidate it |
| [`10-design/risks.md`](10-design/risks.md) | The five risks named above, each with a "would fail prototype if…" trigger |
| [`20-tickets-dag.md`](20-tickets-dag.md) | Mermaid DAG for `T-FR-0002-xx` |
| [`tickets.md`](tickets.md) | Canonical ticket sections (`### T-FR-0002-xx`, phases, deps) |
| [`serial-diary.md`](serial-diary.md) | Append-only diary |
| `40-prototype-report.md` | **Created at close.** Findings + amendments to FR-0001 docs |

Authoritative shared specs (`docs/design/architecture/overview.md`, `mantle-ui.md`, `deployment.md`, `notifications.md`) are **inputs** to this FR. The prototype either confirms them or generates amendments through the process in `docs/ai-context.md`.

## Open questions

| ID | Question | Default for prototype |
|----|----------|------------------------|
| P1 | Build the Mantle shell directly in `apps/hub/web/` or in a fresh `prototype/` folder we throw away? | Build in `apps/hub/web/` so the FR-0001 ticket `T-FR-0001-04` inherits the working shell. |
| P2 | Is the "hub" backend for the prototype a real FastAPI app or a 30-line stub? | **Real FastAPI app**, but with only the four endpoints needed (`/`, `/api/push/subscribe`, `/api/push/test`, `/api/health`). FR-0001's `T-FR-0001-02` will replace the stub with the registry-backed hub. |
| P3 | Where does the VAPID keypair live? | `var/hearth/secrets/vapid.{pub,priv}` (the same path FR-0001 uses) so the keypair survives the prototype → MVP transition. |
| P4 | Test on a Mac mini or Pi 4 first? | **Mac mini first** (faster iteration) → Pi 4 second (validate ARM and lower-end). |
| P5 | If the iPhone CA trust UX is too painful, fall back to a real cert? | The prototype must succeed with `tls internal` first; if the trust UX consistently fails users, we open `Q-FOLLOWUP-01` against FR-0001 to consider Tailscale-issued certs or Let's-Encrypt-via-DNS-01. |
