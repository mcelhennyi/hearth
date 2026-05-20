# Tickets — FR-0002 iPhone PWA prototype

**Feature id:** **`FR-0002`**
**Canonical ids:** **`T-FR-0002-xx`**
**DAG:** [`20-tickets-dag.md`](20-tickets-dag.md)
**Progress tracker:** [`tasks/ticket-progress.md`](../../ticket-progress.md)
**Charter:** [`README.md`](README.md), [`10-design/charter.md`](10-design/charter.md), [`10-design/risks.md`](10-design/risks.md)

These tickets are intentionally small — each is a vertical slice. Phases follow `docs/ai-context.md` (TEST → DEV → VAL). **Priority (2026-04-30):** **VAL** for each ticket is satisfied by proving the stack on a **Raspberry Pi** (FR-0002 closeout host) with a desktop browser and/or iPhone on the same LAN as documented in `SETUP.md` and `40-prototype-report.md`. **Mac mini** validation is a **later phase** — not required for ticket VAL `done`. **iPhone-specific checks** beyond TLS/push are a **side goal** under **Follow-up: iPhone** in the closeout report.

The **TEST/DEV/VAL exit criteria below are concise**; the next worker may flesh them out before starting work, recording any expansion in `serial-diary.md`. Reuse code that ends up working — these tickets are also the seeds for FR-0001 tickets `T-FR-0001-04`, `-05`, and `-09`.

---

### T-FR-0002-01 — Caddy + `tls internal` + static placeholder

**Title:** Caddy in Compose with local TLS, serving a static `https://hearth.home.arpa/` placeholder
**Deps:** `none`
**Reuse target:** `T-FR-0001-05` (Caddy generation and local TLS)

#### Purpose

Stand up a Compose stack with one Caddy container that serves a static placeholder page over `https://hearth.home.arpa/` using `tls internal`. Provide `./develop ca-export` for trusting the local CA on clients (including iPhone when you run the side goal). **No** plugin generation, **no** registry — just a hard-coded `Caddyfile`.

#### Phases (concise)

| Phase | Exit criteria |
|-------|----------------|
| **TEST** | A bash test brings the stack up, `curl -k https://hearth.home.arpa/` returns a known-good HTML body, `./develop ca-export` serves the local-CA cert at `:8080/ca.crt` for ≤ 10 minutes, then tears down. |
| **DEV** | `deploy/compose/docker-compose.yml`, `deploy/caddy/Caddyfile.dev`, `./develop` wrapper subcommands `up`, `down`, `ca-export`. mDNS or `/etc/hosts` documented in `deploy/compose/README.md`. |
| **VAL** | **Server-first:** On a real **Pi 4** (FR-0002 closeout host), run the Compose stack; from a desktop browser on the same LAN (or SSH port-forward if documented), open `https://hearth.home.arpa/` after trusting the exported local CA — **no TLS warning**. **Mac mini:** later phase (not required). Note host IP, OS, and client in `serial-diary.md` or the closeout report. **Side goal (non-blocking):** Safari on iPhone after CA trust — **Follow-up: iPhone** in `40-prototype-report.md`. |

---

### T-FR-0002-02 — Mantle PWA bones (manifest + SW + bottom-tab placeholder)

**Title:** Static React + Vite + Vite-PWA shell with manifest, service worker, theme tokens, and a bottom-tab placeholder
**Deps:** `none`
**Reuse target:** `T-FR-0001-04` (Mantle PWA shell and iframe embed)

#### Purpose

Build the Mantle shell at `apps/hub/web/`. The shell is **static** — no plugin frame yet. Manifest, service worker, app icons (use `docs/design/logo.svg`), Apple meta tags, safe-area CSS, theme tokens from `docs/design/mantle-ui.md`, bottom-tab nav placeholder (4 tabs that all render the same "PWA-ready" tile), top-bar variant for desktop. Caddy (from `T-FR-0002-01`) serves the built bundle.

#### Phases (concise)

| Phase | Exit criteria |
|-------|----------------|
| **TEST** | Vitest covers the bottom-tab/top-bar layout switch at the 768 px breakpoint and the SW registration. Lighthouse PWA audit ≥ 90 in CI (Playwright + headless Chrome). |
| **DEV** | `apps/hub/web/` Vite + TS scaffold, Tailwind, Vite-PWA config, `manifest.webmanifest`, `index.html` with Apple meta tags, four placeholder tab routes, theme tokens. |
| **VAL** | **Server-first:** With Caddy serving the built bundle on **Pi**, load `https://hearth.home.arpa/` from a desktop browser (same LAN); no TLS errors after CA trust; manifest loads; SW registers (verify in devtools); layout matches ticket intent at desktop and a mobile **viewport** width in devtools. **Mac mini:** later phase. **Side goal (non-blocking):** real iPhone — Add to Home Screen, standalone launch, safe-area tabs, force-quit + relaunch — **Follow-up: iPhone** in `40-prototype-report.md`. |

---

### T-FR-0002-03 — Web Push round-trip (VAPID + subscribe + send)

**Title:** End-to-end Web Push from a tiny FastAPI service to a subscribed PWA client (server-first; iPhone as follow-up)
**Deps:** `T-FR-0002-01`, `T-FR-0002-02`
**Reuse target:** `T-FR-0001-09` (Auth, VAPID, Web Push + ntfy)

#### Purpose

Add the smallest backend that can send a Web Push to a subscribed client. A FastAPI app (`apps/hub/api/`) exposes:

- `GET /api/health`
- `POST /api/push/subscribe` — accepts a `PushSubscription`, persists to a JSON file at `var/hearth/push-subscriptions.json` (no SQLite — keep it tiny).
- `POST /api/push/test` — signs a fixed payload with VAPID and POSTs to every stored subscription endpoint.

VAPID keypair generated by a `scripts/gen-vapid.py` and stored at `var/hearth/secrets/vapid.{pub,priv}` (the same path FR-0001 will reuse).

The Mantle shell adds a "Send test notification" button on the home tile; the SW handles the `push` event with `self.registration.showNotification`.

#### Phases (concise)

| Phase | Exit criteria |
|-------|----------------|
| **TEST** | Unit: VAPID signing matches a known-good vector; subscription pruning on `410 Gone`. Integration: spin up the stack, fake-subscribe with a captured iOS subscription, assert `pywebpush` returns a 2xx for the test endpoint. |
| **DEV** | `apps/hub/api/` FastAPI app, `pywebpush` integration, SW push handler in the Mantle shell. Static auth: a single hard-coded session cookie or no auth (LAN-only). Note the auth shortcut in `serial-diary.md` so it doesn't leak into FR-0001. |
| **VAL** | **Server-first:** From a desktop Chromium-class browser **or** iPhone PWA subscribed against the **deployed** hub on **Pi**, tap "Send test notification" — push arrives in ≤ 30 seconds. **Mac mini:** later phase. **Side goal (non-blocking):** remaining iPhone Home Screen / relaunch checks — **Follow-up: iPhone** in `40-prototype-report.md`. |

---

### T-FR-0002-04 — Server walkthrough + closeout report (iPhone follow-up optional)

**Title:** Run the acceptance demo on Pi 4 (server-first steps); write the closeout report; raise amendments against FR-0001 docs; Mac mini later phase
**Deps:** `T-FR-0002-01`, `T-FR-0002-02`, `T-FR-0002-03`
**No FR-0001 reuse target** — this ticket produces decisions, not code.

#### Purpose

Run the full FR-0002 **server-first** acceptance (see [`README.md`](README.md) → "Acceptance for FR-0002 close") on a **Pi 4** per repo-root **`SETUP.md`**. **Mac mini** is a **later phase** — defer to **Environment A** in `40-prototype-report.md`. Time the Pi run; capture screenshots / logs. **iPhone-only steps** beyond TLS/push are optional — log under **Follow-up: iPhone**. Fill in `40-prototype-report.md` and amend FR-0001 docs per `docs/ai-context.md` for any DESIGN-FLAW found.

#### Phases (concise)

| Phase | Exit criteria |
|-------|----------------|
| **TEST** | The five-step acceptance is itself the test. Each step is a checkbox in the report; each must produce evidence (screenshot, log line, video timestamp). |
| **DEV** | Run the demo. Iterate on bugs found in the prototype itself, **not** in FR-0001 docs (that's the next phase). |
| **VAL** | `40-prototype-report.md` is written and committed; every R1–R5 risk in [`10-design/risks.md`](10-design/risks.md) has a verdict (pass / fail / pass-with-caveat) and a linked amendment commit when applicable. The FR-0001 README's "parked" callout is updated with what FR-0002 learned. |

---

## FR-0002 closeout

When `T-FR-0002-04` VAL is `done`, run `/finish-feature` so the prototype branch lands as a PR to `main`. Update `REGISTRY.md` to set FR-0002 status `done` and FR-0001 status back to `design` (or `in-progress` if implementation is starting immediately).
