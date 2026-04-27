# Roadmap

This is a **direction-of-travel** doc, not a contract. Items here are not authoritative product specs until they get an `FR-NNNN` and move into `docs/design/...` or `tasks/feature-history/FR-NNNN-*/10-design/`.

## Phase 1 — MVP (FR-0001, in design)

- Hub app (gateway, plugin registry, dashboard, settings).
- Tinder plugin manifest + on-disk discovery (submodules and drop-in).
- Caddy generation from registry, with `tls internal` for local HTTPS.
- Mantle shared **PWA** shell (manifest + service worker + bottom-tab nav, iframe embeds for MVP).
- iPhone "Add to Home Screen" + local CA trust workflow.
- Web Push notifications (with ntfy fallback) — Spark capability `hub.notify.send`.
- Spark v1 (local Unix-socket RPC + pub/sub).
- Kindling templates repo + scaffolding CLI.
- Compose dev loop + Pi/Mac mini install script.
- One reference plugin (`groceries`).

Acceptance: see `tasks/feature-history/FR-0001-hearth-platform/README.md`.

## Phase 2 — Ember relay + remote access (separate FR — not yet allocated)

- Ember relay server (cloud-hosted or self-hosted) that brokers e2e-encrypted access to a home Hearth box from anywhere.
- Native [`remote-access`](plugin-ideas/remote-access.md) plugin that owns relay provider setup, device pairing UX, status, and diagnostics once the relay surface exists.
- Device-bound identity (per-device keypair, hub signs new devices on first pairing).
- Encrypted continuous backup adapters: Google Drive, S3-compatible, iCloud Drive (best-effort), potentially through a native [`system-backup`](plugin-ideas/system-backup.md) plugin.
- `spark.call_remote` for cross-host plugin calls.
- Hub UI: device pairing, relay status, restore-from-backup.

Sketch: [`satellite-repos/ember.md`](satellite-repos/ember.md).

## Phase 3 — Lifestyle features (multiple FRs, individually scoped)

These were named in the original product brief and are explicitly **not** part of FR-0001. Each becomes its own FR when the platform can host it.

- **Cross-app notifications + reminders** — uses Spark events and a small `notifier` plugin.
- **Unified dashboard** — aggregates Spark events into "today" tiles. The hub already shows enabled plugins; this is richer aggregation.
- **AI recommendations** — recipes-from-pantry, idea catcher → developer agent handoff. Builds on Spark capability surface; agentic developer is the existing `../project_02` (Colony) reachable via a Spark adapter.
- **Usage analytics (private)** — per-user histograms of plugin usage; never leaves the box without explicit export.
- **Plugin store / community plugins** — Tinder manifests are the unit of distribution; a store is a curated index plus signature verification.
- **Native plugin idea backlog** — early plugin concepts start in [`native-plugin-ideas.md`](native-plugin-ideas.md) before they receive an `FR-NNNN`.
- **Workflows / automation** — Zapier-style cross-plugin recipes, expressed as a small DSL on top of Spark.
- **Native wrappers** — Tauri or Electron shell that points at `https://<id>.ember.example/`; same UI, OS-integrated.

## Phase 4 — Research / speculative

- **Ember mining / token incentives.** The original brief floats Ember acting as a node in a new "home-server" cryptocurrency where value derives from contributing CPU, storage, and (consensual) data sharing. Tracked here as a research item; **not** a design commitment. Any move on this needs a feasibility study, legal review, and a separate FR with explicit user-consent UX.
- **Local LLM inference on Pi 5 / Mac mini** as a Spark capability `ai.complete`; depends on hardware and quantized models worth running.
- **Federated Hearth boxes** (e.g. household with two Pis) via Ember; requires conflict-resolution semantics on shared plugin data.

## Triage rules

- An idea graduates from this doc to a real FR when:
  1. The acceptance for FR-0001 is met (or near).
  2. The idea has a single-paragraph charter and a non-empty out-of-scope list.
  3. A stakeholder owns it.
- Until then, ideas may be referenced from `serial-diary.md` notes, but **must not** be cited as if they were committed scope.
