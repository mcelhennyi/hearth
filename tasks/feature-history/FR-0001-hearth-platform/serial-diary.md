# FR-0001 — serial diary

Append-only. Newest entries at the top of each session block.

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
