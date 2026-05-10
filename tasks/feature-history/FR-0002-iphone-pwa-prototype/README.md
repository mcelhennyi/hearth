# FR-0002 — iPhone PWA prototype

**Status:** `in-progress`
**Owner:** project lead (Ian)
**Allocated:** 2026-04-27
**Relationship:** parks FR-0001 implementation while we de-risk the **home-server PWA** story (TLS + shell + push on Pi/Mac mini first; iPhone as follow-up). FR-0001 design stays authoritative for MVP; this FR may produce **design amendments** to FR-0001 if reality disagrees.

## Charter (one sentence)

Prove that a Caddy-fronted, locally-trusted, manifest-and-service-worker React shell **runs correctly on a Pi/Mac mini at home** (TLS, static shell, Web Push to a subscribed browser) **before** we invest in the plugin registry, Tinder loader, Spark broker, or Kindling repo split. **iPhone** Home Screen + on-device push is a **follow-up side goal** to confirm the same stack on iOS; it does not gate FR-0002 close once server-first acceptance below is satisfied.

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
5. **Server walkthrough**: a documented run on Mac mini and Pi (screenshots/logs). Time major steps. Note every friction point.
6. **Side goal — iPhone walkthrough** (non-blocking for FR-0002 close): when available, filmed run-through on a real iPhone; file under **Follow-up: iPhone** in `40-prototype-report.md`.

## Out of scope

- Plugin loader, Tinder schema, plugin registry, Spark broker. None of FR-0001's tickets `T-FR-0001-02..-08`.
- Auth and identity beyond a single hard-coded session cookie (or no auth at all on a LAN-only prototype host).
- ntfy fallback. We're proving Web Push works; ntfy stays in FR-0001.
- Backup, install.sh for Pi/Mac mini, systemd units. The prototype runs in `./develop up` only.
- Kindling repo split. The shell is built directly under `apps/hub/web/` with no `vendor/kindling/` submodule.
- `groceries` plugin. The prototype's only "screen" is the test-notification button and the Mantle bottom-tab placeholder.

## Acceptance for FR-0002 close (server-first)

Evidence (video or screenshot set + logs) shows **on Mac mini and on Pi** (both unless one is waived with a written caveat in the report), in order:

1. `./develop up` (or documented production-equivalent) brings the stack up on the target host.
2. A **desktop browser** on the same LAN opens `https://hearth.home.arpa/` — Mantle shell with a green "PWA-ready" tile, **no certificate errors** after the local CA is trusted on that client.
3. DevTools (or equivalent) confirms **service worker** registration against the deployed origin.
4. **Web Push:** subscribe from that browser; "Send test notification" delivers within ~30 seconds in three of three tries; notification click focuses the app.

A short markdown report at `40-prototype-report.md` (created when the FR closes) summarizes what worked, what didn't, lists every **DESIGN-FLAW** discovered against FR-0001's `mantle-ui.md`, `deployment.md`, and `notifications.md`, and includes a section **Follow-up: iPhone** (empty OK at close) for Add to Home Screen, standalone chrome, and on-device push when someone runs that side goal later.

## Side goal — iPhone (product confidence, non-blocking)

When you have a phone and LAN, extend the same checklist: Safari CA trust, Add to Home Screen, standalone launch, push to iOS, force-quit + relaunch. Record results in **Follow-up: iPhone** in `40-prototype-report.md` — does not reopen FR-0002 if server-first acceptance already merged unless a **DESIGN-FLAW** appears.

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
