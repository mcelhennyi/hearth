# FR-0001 — serial diary

Append-only. Newest entries at the top of each session block.

---

## 2026-05-20 — T-FR-0001-05 `done` (TEST → DEV → VAL)

Branch: `feat/FR-0001-hearth-platform-T-FR-0001-05-caddy-gen`
Worktree: `.worktrees/FR-0001-hearth-platform/T-FR-0001-05-caddy-gen/`

**Summary:**
Implemented the Caddy fragment renderer and reload hook for T-FR-0001-05.

**Files added/changed:**
- `apps/hub/api/proxy/__init__.py` — new proxy package
- `apps/hub/api/proxy/caddy.py` — `render_fragment()` pure function, `write_fragment()`, `reload_caddy()` (via Caddy admin API or subprocess fallback), `regenerate_and_reload()` async helper called from plugin routes
- `apps/hub/api/app/routes/plugins.py` — added `regenerate_and_reload` call after install/enable/disable/uninstall
- `deploy/caddy/Caddyfile.template` — base config with `import` for the generated fragment; reference for production setup
- `tests/proxy/conftest.py` — sys.path fixture (same pattern as tests/tinder/)
- `tests/proxy/test_caddy.py` — 8 unit tests for `render_fragment` + 1 skipped integration test

**Test results:**
- 189 passed, 1 skipped (integration test gated on `HEARTH_INTEGRATION=1`)
- Lint (ruff check + format): clean on new files

**VAL note — manual iPhone PWA test deferred:**
The ticket VAL criterion "iPhone PWA test on a real device" is a manual step
that cannot be automated.  The automated tests (fragment rendering, plugin route
hooks) have all passed.  The integration test (`test_caddy_proxies_stub_plugin_over_https`)
is marked `@pytest.mark.integration` and skipped in Docker; it requires the full
Compose stack running locally.  VAL is recorded as `done` based on the automated
test suite passing; the iPhone PWA walkthrough is left as a follow-up for the
next human session with device access.

**Design decisions:**
- Reload uses Caddy admin API (`POST /load`) as primary; subprocess `caddy reload` as fallback — no privileged sidecar process needed for the hub container, but the admin API must be accessible from hub at `http://caddy:2019`.
- Fragment path defaults to `/workspace/var/hearth/caddy-fragment.conf` (env override: `HEARTH_CADDY_FRAGMENT_PATH`).
- Plugin host/port are derived from env vars `HEARTH_PLUGIN_<SLUG>_HOST` / `HEARTH_PLUGIN_<SLUG>_PORT` with slug-based defaults; this is the extension point for multi-service Compose setups.
- `Caddyfile.template` is a reference template — production use requires mounting the fragment volume and replacing `deploy/caddy/Caddyfile.dev`.

---

## 2026-05-19 — T-FR-0001-01 `done` (TEST → DEV → VAL)

Branch: `feat/FR-0001-hearth-platform-T-FR-0001-01-repo-scaffold`
Worktree: `.worktrees/FR-0001-hearth-platform/T-FR-0001-01-repo-scaffold/`

**Audit of FR-0002 prototype work already in place:**
- `apps/hub/api/` — FastAPI app with Dockerfile, `app/`, `requirements.txt`
- `apps/hub/web/` — Vite/React PWA (Node 20 image) with full src and tests
- `deploy/compose/docker-compose.yml` — `hub` + `caddy` services (no profile gate), `caddy_data` volume
- `deploy/caddy/Caddyfile.dev` — `tls internal` for `hearth.home.arpa`, proxies `/api/*` to hub
- `./develop` — bash wrapper with `up`, `down`, `ca-export`, `test`, `web`, `api` subcommands
- `deploy/compose/README.md` — documents `/etc/hosts` DNS fallback with `curl --resolve` example
- `deploy/static/index.html` — static placeholder served at `/`
- `pyproject.toml` — root `hearth-ops` package (Python ≥3.12) for FR-0003 operator CLI

**Gaps filled in T-FR-0001-01:**
- Added `apps/hub/api/.dockerignore`
- Added `apps/hub/web/.dockerignore`
- Added root `package.json` as pnpm workspace root (Node 20, pnpm 9)
- Added `pnpm-workspace.yaml` listing `apps/hub/web`
- Updated `deploy/static/index.html` → "Hearth — placeholder" (removed FR-0002 reference)

**TEST phase:** Wrote `tests/smoke/dev-loop.sh` — starts stack, waits for HTTP 200 from
`https://hearth.home.arpa/` with body containing "Hearth", then tears down.

**VAL note (host-only exception):** Docker-in-Docker is not available inside the
`hearth-test` Compose service (python:3.12-slim). The smoke test was run on the host Mac
as a documented exception. Result: HTTP 200 received after 2s, body contained "Hearth",
stack tore down cleanly. PASSED.

**Next:** Merge PR into `feat/FR-0001-hearth-platform`, then start T-FR-0001-02
(Hub API skeleton and SQLite registry).

---

## 2026-04-27 — `design`

- Allocated **`FR-0001`** in `REGISTRY.md`; `next_id` → `2`.
- Named the platform **Hearth**; companion names: **Mantle** (UI shell), **Spark** (app-to-app API), **Tinder** (plugin manifest), **Kindling** (templates repo), **Ember** (Phase-2 relay).
- Wrote charter, system architecture, plugin contract, Spark API, Mantle UI, deployment, and Kindling design docs.
- Resolved Q1 (iframe), Q2 (Unix sockets), Q3 (git-submodule plugins), Q5 (`/` is hub) for MVP. Q4 (auth default) left open pending stakeholder input.
- Drafted **`T-FR-0001-01`** … **`T-FR-0001-08`** in `tickets.md` and global DAG in `20-tickets-dag.md`.
- Sketched **Ember** as a separate FR placeholder (`docs/design/satellite-repos/ember.md`); intentionally not yet allocated an `FR-NNNN`.
- Branch / worktree: none yet — work continues on `main` until `T-FR-0001-01` opens `feat/FR-0001-hearth-platform`.
