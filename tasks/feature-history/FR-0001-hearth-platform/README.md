# FR-0001 — Hearth platform (MVP)

**Status:** `parked` (design authoritative; implementation paused pending [FR-0002](../FR-0002-iphone-pwa-prototype/) prototype findings)
**Owner:** project lead (Ian)
**Allocated:** 2026-04-27

> **Parked 2026-04-27.** Before investing in the registry, Tinder loader, Spark broker, and Kindling split, we are de-risking the iPhone-PWA story end-to-end via [FR-0002](../FR-0002-iphone-pwa-prototype/README.md). The design in `docs/design/` and in this folder remains the source of truth for the MVP target; FR-0002 may produce **amendments** (per `docs/ai-context.md`) to `mantle-ui.md`, `deployment.md`, or `notifications.md` if a real-device test refutes an assumption. **Tickets `T-FR-0001-01..10` are unchanged but eligible only after FR-0002 closes.**

## Charter (one sentence)

Stand up Hearth — a self-hosted hub for vibe-coded daily-life productivity apps — so a Raspberry Pi or Mac mini at home can run a growing constellation of plugins behind one URL, one UI shell, and one inter-app API.

## In scope (MVP)

1. **Hub app** (Python/FastAPI + React) at `/`: dashboard, plugin registry, settings.
2. **Tinder** plugin manifest format + on-disk discovery (`/etc/hearth/plugins.d/*.toml` or git submodules under `apps/`).
3. **nginx reverse proxy** generated from the registry: `/` → hub, `/<slug>/...` → plugin.
4. **Mantle** — the shared React shell + design-system package (theme, top nav, plugin chrome, auth widget). Lives in **Kindling** repo, consumed by hub and plugins.
5. **Spark** v1 — synchronous JSON-RPC over Unix domain sockets between plugin processes; plugin capability surface declared in Tinder.
6. **Kindling** template repo — scaffolds a new plugin (FastAPI backend + React frontend wired into Mantle and Spark), CLI tool `kindling new <slug>`.
7. **Deploy story** — Docker Compose for dev; systemd units + an `install.sh` for Pi/Mac mini bare metal.
8. **One demo plugin** — `groceries` (chosen because it exercises persistence, Spark capability `produce: groceries.list`, and a basic UI). Lives in its own repo, added as submodule `apps/groceries/`.

## Out of scope (this FR)

- **Ember** relay / e2e remote access / cloud-storage backup providers — separate later FR (sketch in `docs/design/satellite-repos/ember.md`).
- **Identity beyond a single local user.** Single-user assumption with a `.htpasswd`-style local auth; multi-user/device pairing waits for Ember.
- **Notifications, AI recommendations, gamification, plugin store, automation/workflows.** Listed in `docs/design/roadmap.md` as Phase 3+; do not pull into MVP.
- **C++ background services.** Reserved for later when a real workload needs them.

## Acceptance for FR-0001 close

- A fresh Pi/Mac mini can `git clone … && ./install.sh` and reach a working dashboard at `http://hearth.local/`.
- Installing the `groceries` plugin (drop-in submodule + `kindling install`) makes it appear in the dashboard nav and reachable at `/groceries/`.
- A second hypothetical plugin can call `spark.call("groceries", "list.add", {…})` and succeed (validated via a tiny `dev-tools/spark-cli` script).
- Mantle theme tokens visibly drive both hub and plugin UIs (no per-plugin restyling).

## Layered design

| Doc | Topic |
|------|-------|
| [`10-design/charter.md`](10-design/charter.md) | This charter, expanded with stakeholder context and non-goals reasoning |
| [`10-design/system-architecture.md`](10-design/system-architecture.md) | Components, data flow, sequence diagrams, deployment topology |
| [`10-design/plugin-contract.md`](10-design/plugin-contract.md) | Tinder manifest schema, lifecycle, capability surface |
| [`10-design/spark-api.md`](10-design/spark-api.md) | Spark v1 RPC + event bus, capability discovery, error envelope |
| [`10-design/mantle-ui.md`](10-design/mantle-ui.md) | Shell layout, theme tokens, plugin iframe vs in-app embed decision |
| [`10-design/deployment.md`](10-design/deployment.md) | Docker Compose dev loop, systemd install, nginx generation, backup |
| [`10-design/kindling-templates.md`](10-design/kindling-templates.md) | Kindling repo layout + scaffolding CLI + version policy |
| [`20-tickets-dag.md`](20-tickets-dag.md) | Mermaid DAG for `T-FR-0001-xx` |
| [`tickets.md`](tickets.md) | Canonical ticket sections (`### T-FR-0001-xx`, phases, deps) |
| [`serial-diary.md`](serial-diary.md) | Append-only design/development diary |

The shared design surface — Spark, Tinder, Mantle, deployment, roadmap — also lives at the repo-wide path `docs/design/` so multiple FRs can reference it without going through this folder.

## Open questions

| ID | Question | Status |
|----|----------|--------|
| Q1 | Plugin embed: iframe per plugin (full isolation) vs ESM module-federation (one shell, shared cache)? Default in design: **iframe for MVP**, federation later. | resolved-for-MVP |
| Q2 | Spark transport: Unix sockets vs HTTP-on-loopback. Default: **Unix sockets** (no port management); HTTP only for cross-host (Phase 2). | resolved-for-MVP |
| Q3 | Plugin distribution: git submodule vs OCI image vs tarball. Default for MVP: **git submodule under `apps/<slug>/`** — easy to vendor and inspect. | resolved-for-MVP |
| Q4 | Auth in MVP: local `.htpasswd` vs no-auth on LAN. Default: **basic auth required by default**, bypass only with `HEARTH_TRUST_LAN=1`. | open |
| Q5 | Naming for the dashboard/landing page route — `/` (hub at root) vs `/dashboard/`. Default: **`/`** with hub claiming the empty slug. | resolved-for-MVP |
