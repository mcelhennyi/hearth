# Tickets — FR-0001 Hearth platform

**Feature id:** **`FR-0001`**
**Canonical ids:** **`T-FR-0001-xx`**
**DAG:** [`20-tickets-dag.md`](20-tickets-dag.md)
**Progress tracker:** [`tasks/ticket-progress.md`](../../ticket-progress.md)

Phases follow `docs/ai-context.md`: each ticket goes **TEST → DEV → VAL** in a child worktree under `.worktrees/FR-0001-hearth-platform/`. Each ticket spec below lists exit criteria for each phase. Tests should pin the verification surface (acceptance), not implementation details.

---

### T-FR-0001-01 — Repo scaffold and dev loop

**Title:** Repo scaffold and Compose dev loop
**Deps:** `none`

#### Purpose

Create the directory layout from `.cursor/rules/stack-conventions.mdc`, a working `./develop up` Compose stack with one Caddy container, one empty `hub` container, and a smoke test. After this ticket, `./develop up` boots locally and `https://hearth.home.arpa/` returns a placeholder page over local TLS.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Acceptance for "the dev loop is real" | A bash test (`tests/smoke/dev-loop.sh`) starts the stack, `curl -k https://hearth.home.arpa/` returns 200 with a `Hearth — placeholder` body, then tears down. |
| **DEV** | Build the scaffold | `apps/hub/api/` (FastAPI placeholder), `apps/hub/web/` (Vite placeholder), `deploy/compose/`, `deploy/caddy/`, `./develop` wrapper. Add `.dockerignore`, `pyproject.toml`, `package.json` (pnpm workspace). |
| **VAL** | Verify a fresh clone works | Cold clone + `./develop up` succeeds; smoke test passes in CI stub. |

#### Notes

- Pin Python 3.12, Node 20 LTS, Caddy 2.8.
- DNS `hearth.home.arpa` resolution: use local DNS (for example Pi-hole or router DNS), with an `/etc/hosts` fallback in `deploy/compose/README.md`.

---

### T-FR-0001-02 — Hub API skeleton and SQLite registry

**Title:** Hub API skeleton and SQLite registry
**Deps:** `T-FR-0001-01`

#### Purpose

A FastAPI app (`hub.app:app`) backed by SQLite at `var/hearth/hearth.db` exposes:

- `GET /api/health` — liveness.
- `GET /api/plugins` — registry rows.
- `POST /api/plugins/install`, `/.../enable`, `/.../disable`, `/.../uninstall` — stubs that mutate the registry but do not yet talk to a supervisor.
- `GET /api/settings`, `PUT /api/settings` — the small set we know we need (theme, hostname, notification channel).

DB migrations via `alembic`; first migration creates the registry, settings, and audit-log tables.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | API contract tests | `pytest tests/api/test_plugins.py` covers registry CRUD (install→enable→disable→uninstall) and asserts schema returned matches `docs/design/plugin-contract.md`. |
| **DEV** | Implement | FastAPI routes, SQLAlchemy models, Alembic migration, `tests/conftest.py` with a temp DB fixture. |
| **VAL** | All API tests green; OpenAPI doc renders at `/api/docs`; round-trip from web shell works against stub. | |

---

### T-FR-0001-03 — Tinder loader and manifest schema

**Title:** Tinder loader and manifest schema
**Deps:** `T-FR-0001-02`

#### Purpose

Implement the Tinder spec from `docs/design/plugin-contract.md`:

- `apps/hub/api/tinder/schema.py` — pydantic models for `tinder.toml`.
- `apps/hub/api/tinder/loader.py` — read+validate, surface diagnostics.
- Wire `POST /api/plugins/install` to the loader.
- Add a CLI sub-command `hub tinder validate <path>` for plugin authors.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Schema + loader tests | Fixture plugins under `tests/fixtures/plugins/`: one valid (`groceries-stub`), several invalid (bad slug, unknown backend kind, permission overflow). Each error case asserts a specific diagnostic. |
| **DEV** | Implement schema + loader | Round-trip the fixture into the registry. Capture validation errors as registry rows with `state=disabled`. |
| **VAL** | Loader handles every documented schema rule; spec doc and code in lockstep (escalate `DESIGN-FLAW` if mismatch found). | |

---

### T-FR-0001-04 — Mantle PWA shell and iframe embed

**Title:** Mantle PWA shell and iframe embed
**Deps:** `T-FR-0001-01`

#### Purpose

Build the React shell at `apps/hub/web/`:

- Vite + Vite-PWA for the manifest and service worker.
- `apple-touch-icon`, theme-color, `viewport-fit=cover`, safe-area CSS.
- Top bar (desktop) + bottom-tab nav (mobile) via a media-query-driven layout.
- Plugin frame as an `iframe` rendering `/<slug>/`; postMessage protocol from `mantle-ui.md`.
- Hooks: `useMantle`, `useUser`, `useTheme`, `useSpark` (calls into the plugin's own backend, not the broker), `useNotifications`.
- Dashboard at **`/`** fed by registry + layout API (see `dashboard.md`); **no hardcoded plugin tabs or routes** in `apps/hub/web/`.
- Plugin frame as `iframe` for each enabled app slug from `GET /api/plugins`.
- iOS install prompt on first visit.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Shell tests | Vitest + RTL: layout breakpoint; postMessage mock iframe; SW smoke; **assert no routes named `/groceries`, `/recipes`, or `/ideas` in shell source**; nav renders only Home (+ Settings) when registry mock is empty. Lighthouse PWA audit ≥ 90 in CI (Playwright + headless Chrome). |
| **DEV** | Implement | Components under `apps/hub/web/src/mantle/` (lifted to Kindling in T07). Remove FR-0002 prototype hardcoded tabs. Tailwind + shadcn/ui. |
| **VAL** | Manual: iPhone standalone; with **zero** plugins, bottom bar shows Home only; after installing `groceries` submodule, Groceries tab appears from registry. | |

#### Notes

- Theme tokens come from `mantle-ui.md`. Don't reinvent them.
- **Plugin agnosticism:** `apps/hub/web/src/App.tsx` (and all shell code) must not import or name specific plugins. See `docs/design/architecture/overview.md` §1b.
- Document any iOS quirks discovered (back-button, status bar) in `serial-diary.md`.

---

### T-FR-0001-05 — Caddy generation and local TLS

**Title:** Caddy generation and local TLS
**Deps:** `T-FR-0001-01`, `T-FR-0001-03`, `T-FR-0001-04`

#### Purpose

The hub regenerates a Caddyfile fragment from the registry on every install/enable/disable. `./develop ca-export` serves the local CA cert for iPhone trust.

- `apps/hub/api/proxy/caddy.py` — fragment renderer + `caddy reload` invocation.
- `deploy/caddy/Caddyfile.template` — base config that `import`s the fragment.
- `./develop ca-export` script wrapping `caddy file-server` for 10 minutes.

Out of scope here: nginx parity templates (post-MVP).

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Renderer + reload tests | Unit tests: registry fixture → expected fragment text (golden files). Integration: spin up real Caddy in Compose, install a stub plugin, `curl https://hearth.home.arpa/groceries-stub/health` returns the stub's response. |
| **DEV** | Implement renderer + helper + reload hook | Reload runs as a privileged side-car (separate Compose service) not in the hub itself. |
| **VAL** | iPhone PWA test on a real device: visit `https://hearth.home.arpa/`, install, see plugin tab. | |

---

### T-FR-0001-06 — Spark v1 broker and client libs

**Title:** Spark v1 broker and Python/TS client libraries
**Deps:** `T-FR-0001-02`

#### Purpose

Implement Spark v1 per `docs/design/spark-api.md`:

- Broker process (`apps/hub/api/spark/broker.py`) — Unix-socket listener at `var/hearth/run/spark.sock`, length-prefixed JSON frames.
- Python client (`apps/hub/api/spark/client.py`) used by the hub itself; later lifted to Kindling in T07.
- TS client stub (used from a plugin's *backend*, not the browser) lives under `apps/hub/web/src/spark/` for now and is lifted later.
- Permission enforcement against the registry's view of Tinder manifests.
- Audit log to `var/hearth/log/spark.jsonl`.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Broker tests | `pytest tests/spark/`: call/reply, publish/subscribe, permission denied (`from`'s manifest doesn't allow target.method), unknown method, timeout. Two-process integration test with two stub plugins. |
| **DEV** | Implement broker + client + permission check | Topic wildcards (`*`, `>`); error envelope per spec. |
| **VAL** | All tests green; audit log line count matches frame count in integration test. | |

---

### T-FR-0001-07 — Kindling repo and CLI

**Title:** Lift Mantle + Spark + Tinder schema into Kindling repo, add scaffolding CLI
**Deps:** `T-FR-0001-03`, `T-FR-0001-04`, `T-FR-0001-06`

#### Purpose

Create a new repository `kindling` (separate from this one), **initialized from `.skeleton`** with **`.skeleton/` retained as a submodule** inside Kindling, then migrate:

- `apps/hub/web/src/mantle/` → `kindling/mantle/` (published as `@kindling/mantle`).
- `apps/hub/api/spark/client.py` → `kindling/spark/python/`.
- `apps/hub/web/src/spark/` → `kindling/spark/typescript/`.
- `apps/hub/api/tinder/schema.py` (the schema only, not the loader) → `kindling/tinder/`.

Add the `kindling` CLI:

- `kindling new <slug>` — clone `templates/plugin-python/`, replace placeholders, `git init`, optional `git submodule add` into the consumer repo's `apps/<slug>/`.
- `kindling validate [path]` — runs Tinder schema check.
- `kindling install <slug>` — POSTs to a running hub's `/api/plugins/install`.

In Hearth: add `vendor/kindling/` as a submodule; switch `apps/hub/web/` and `apps/hub/api/` to consume from there. Drop the local copies.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Round-trip tests | `kindling new groceries-test` creates a plugin that passes `kindling validate` and successfully installs into the local hub via `kindling install`. |
| **DEV** | Move code, set up workspace, write CLI | The Hearth repo contains zero duplicate copies of code that lives in Kindling. |
| **VAL** | Hearth still boots and the dashboard still renders after the repo split. | |

#### Notes

- Set up Kindling using the same `.skeleton` submodule. Kindling's own FR-0001 (in its own registry) covers its initial scaffold.

---

### T-FR-0001-08 — groceries reference plugin

**Title:** First reference plugin (`groceries`) end-to-end
**Deps:** `T-FR-0001-07`

#### Repository

| Field | Value |
|-------|--------|
| **Git remote (canonical source)** | [`https://github.com/mcelhennyi/grocery-list`](https://github.com/mcelhennyi/grocery-list) |
| **Hearth submodule path** | `apps/groceries/` |
| **Tinder slug / routes** | `groceries` → `/groceries/` (repo name may differ from slug) |

Implementation is developed and pushed in the **`grocery-list`** repo (`kindling new groceries`, own `.skeleton/` + Kindling deps); Hearth consumes it **only** as a submodule at `apps/groceries/`—no plugin source copied into `apps/hub/`.

#### Purpose

A plugin generated via `kindling new groceries` (or equivalent scaffold), developed in **`grocery-list`**, and added to Hearth as `apps/groceries/`. Demonstrates the platform end-to-end per the **Plugin MVP** table below.

#### Plugin MVP (in scope for this ticket)

| Area | MVP behavior |
|------|----------------|
| **UI** | One Mantle-themed screen: shopping list — add an item, check off / remove. No custom theme tokens. |
| **Backend** | FastAPI; `[capabilities.list]` with methods `add`, `remove`, `items` and events `added`, `removed` (see `docs/design/plugin-contract.md`). |
| **Persistence** | SQLite at `var/hearth/plugins/groceries/db.sqlite` (plugin-owned under `var/hearth/plugins/<slug>/`). |
| **Spark — publish** | On add/remove, publish `groceries.list.added` / `groceries.list.removed` (or equivalent per manifest). |
| **Spark — subscribe** | Register handler for `pantry.changed`; **no-op** until a pantry plugin exists (proves subscribe path only). |
| **Spark — notify** | Permission to `spark_call` `hub.notify.send`; optional demo path when item count crosses a configured low-stock threshold (VAL with **T-FR-0001-09**). |
| **Tinder** | `kind = "app"`; valid `tinder.toml`; permissions `spark_publish` for `groceries.*`. |
| **Platform fit** | Install/enable via hub; appears on dashboard; iframe under Mantle at `/groceries/`. |

#### Out of scope (this plugin in FR-0001)

- Pantry inventory, store-aware sorting, multi-list / household sharing, recipes integration.
- `kind = "widget"` surfaces or dashboard widget blocks.
- Calling other plugins' HTTP routes (Spark only).
- Ember, cloud backup, multi-user auth inside the plugin.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Plugin tests | Plugin's own pytest covers `list.add`/`remove`/`items` via Spark. End-to-end Playwright test in Hearth: install via dashboard, add an item, see it on a second browser session. |
| **DEV** | Implement backend, UI, manifest | UI follows Mantle primitives; no custom theme code. |
| **VAL** | iPhone PWA verifies the mobile feel: bottom-tab nav switches in, item add works, Web Push fires when crossing the configured low-stock threshold. | |

---

### T-FR-0001-09 — Auth, VAPID, Web Push + ntfy

**Title:** Single-user local auth + Web Push + ntfy
**Deps:** `T-FR-0001-02`, `T-FR-0001-04`

#### Purpose

Implement the slice of identity + notifications that MVP needs:

- Single-user login: Argon2id password hash in `var/hearth/secrets/`, session cookie, FastAPI dep that injects user.
- VAPID keypair generated on install (`scripts/gen-vapid.py`), stored at `var/hearth/secrets/vapid.{pub,priv}`.
- `POST /api/push/subscribe`, `DELETE /api/push/subscribe/<endpoint>` — registers per-device.
- Spark capability `hub.notify.send` per `docs/design/notifications.md` — fans to Web Push and (if configured) ntfy.
- Quiet hours and rate-limit per spec.
- Mantle: login screen, first-run flow that asks for notification permission and prompts iOS install.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Auth + push tests | Auth tests: bad password, lockout after N attempts, session expiry. Push tests: VAPID signing matches a known-good vector; subscription pruning on `410 Gone`; ntfy POST shape. |
| **DEV** | Implement | Reuse `pywebpush` for VAPID; `httpx` for ntfy. |
| **VAL** | Manual on real iPhone: receive a notification when a stub plugin calls `hub.notify.send`; tapping it opens the right plugin route. | |

---

### T-FR-0001-10 — Pi/Mac mini install.sh + backup

**Title:** Bare-metal install script and backup/restore
**Deps:** `T-FR-0001-05`, `T-FR-0001-08`, `T-FR-0001-09`

#### Purpose

The closeout ticket. Take the Compose-only dev loop and produce a real Pi/Mac mini story:

- `deploy/install.sh` — idempotent installer per `docs/design/deployment.md`.
- `deploy/systemd/hearth-hub.service`, `hearth-plugin@.service`.
- macOS launchd equivalents.
- `hub backup --output <path>` and `hub restore <path>` CLI subcommands.
- Smoke test in CI: a Pi-emulating ARM container runs `install.sh` and confirms `https://hearth.home.arpa/api/health` answers.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Installer + backup tests | CI ARM smoke test green; backup tarball restored on a fresh container produces the same plugin list and groceries items. |
| **DEV** | Implement installer, units, backup/restore | Plugin backup `include`/`exclude` honored. |
| **VAL** | Wall-clock test on a real Pi 4 / Mac mini: clone, run installer, install groceries via dashboard, take a backup, restore on a fresh box. Time the run; record in `serial-diary.md`. | |

---

## Acceptance for FR-0001 closeout

All ten tickets `done` in `tasks/ticket-progress.md`, `serial-diary.md` consolidated into `DIARY.md`, then `/finish-feature` opens a PR to `main`. The five-bullet acceptance from `README.md` is verified on a real Pi/Mac mini and the run is filmed for the project's first-run video.
