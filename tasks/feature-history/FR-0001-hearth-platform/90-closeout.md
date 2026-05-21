# FR-0001 closeout — Hearth platform MVP

**Merged:** 2026-05-21 — [**PR #30**](https://github.com/mcelhennyi/hearth/pull/30) → **`main`** @ `0811ed2`

**Feature-complete gate:** met 2026-05-20; post-merge closeout 2026-05-21.

## Executive summary

FR-0001 delivers the self-hosted Hearth hub: FastAPI registry, Mantle PWA shell, Caddy proxy generation, Spark v1, Kindling scaffolding, groceries reference plugin, bare-metal `install.sh`, and Pi Docker operator path (FR-0003 on `main`). Post-closeout commits on the feature branch wire **Docker-profile groceries end-to-end** (plugin Dockerfile, generated `Caddyfile.plugins`, PWA service-worker allowlist so plugin iframes reach Caddy).

## Delivered surfaces

| Surface | Location |
|---------|----------|
| Hub API + registry | `apps/hub/api/` |
| Mantle PWA shell | `apps/hub/web/` |
| Caddy fragments (bare-metal) | `apps/hub/api` caddy generator |
| Docker profile Caddy + compose | `deploy/caddy/`, `deploy/hearth-install/hearth_install/plugin_compose.py` |
| Spark broker + clients | `spark/` |
| Kindling (in-repo) | `kindling/` |
| Groceries plugin | `apps/groceries/` → `mcelhennyi/grocery-list` |
| Bare-metal install | `deploy/install.sh`, `deploy/systemd/`, `deploy/launchd/` |
| Pi `./install` + `hearth` CLI | `deploy/hearth-install/`, `SETUP.md` |

## Tickets

| Ticket | Summary | TEST / DEV / VAL |
|--------|---------|------------------|
| T-FR-0001-01 | Repo scaffold and Compose dev loop | done / done / done |
| T-FR-0001-02 | Hub API skeleton and SQLite registry | done / done / done |
| T-FR-0001-03 | Tinder loader and manifest schema | done / done / done |
| T-FR-0001-04 | Mantle PWA shell and iframe embed | done / done / done |
| T-FR-0001-05 | Caddy generation and local TLS | done / done / done |
| T-FR-0001-06 | Spark v1 broker and client libs | done / done / done |
| T-FR-0001-07 | Kindling repo and CLI | done / done / done |
| T-FR-0001-08 | groceries reference plugin | done / done / done |
| T-FR-0001-09 | Auth, VAPID, Web Push + ntfy | done / done / done |
| T-FR-0001-10 | Pi/Mac mini install.sh + backup | done / done / done |

## Validation

- `./develop test` on `feat/FR-0001-hearth-platform` @ finish-feature refresh — **238 passed**, 3 skipped (`HEARTH_INTEGRATION=1` gated).
- Pi Docker (operator): `hearth --plugin --add`, `Caddyfile.plugins`, groceries container + `curl https://hearth.home.arpa/groceries/` — validated in session; requires `hearth pwa build` + SW cache clear on iPhone after merge.

## Deferred / follow-up

| Item | Tracking |
|------|----------|
| Manual iPhone VAL (cert trust, PWA, push, groceries tab) | `serial-diary.md`; not blocking gate |
| Hub registry sync with `plugins.yaml` (Docker profile) | DESIGN-GAP DG-D4 in `docs/design/deployment.md` |
| `hearth --plugin --add` → hub `POST /api/plugins/install` | Operator uses file registry today |
| FR-0004 centralized auth | unblocked — resume when staffed |

## Suggested next step

On **Pi**: `git pull` on `main`, `hearth pwa build`, `hearth restart caddy`, clear PWA cache; confirm Groceries tab. Then staff **FR-0004** (`in-progress` in `REGISTRY.md`) or **FR-0005** design tickets.

## Options

| Option | When |
|--------|------|
| Pi groceries + iPhone VAL | Operator smoke on merged `main` |
| Resume FR-0004 | Centralized auth — gate cleared |
| Start FR-0005 | Remote-build / `hearth pwa publish` |

## Audit

- **Merge commit:** `0811ed27304dc76b9e4a98bf8ed8b568dcdf7196`
- **Feature branch:** `feat/FR-0001-hearth-platform` (retained on remote — audit trail)
- **Handoffs:** [`handoffs/2026-05-21-finish-feature.md`](handoffs/2026-05-21-finish-feature.md), [`handoffs/2026-05-21-merged-to-main.md`](handoffs/2026-05-21-merged-to-main.md)
- **Repo-root `CURRENT.md`:** removed on `main` at post-merge closeout (feature-branch artifact)
