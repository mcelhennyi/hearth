# T-FR-0006-02 — Dashboard layout API (parallel diary)

**Branch:** `feat/FR-0006-design-language-T-FR-0006-02-dashboard-layout`
**Worktree:** `.worktrees/FR-0006-design-language/T-FR-0006-02-dashboard-layout/`
**Authority:** `docs/design/dashboard.md` § Layout persistence, § Default layout.

## 2026-05-21 — TEST → DEV → VAL complete

**Surface delivered**

- `GET /api/dashboard/layout` — returns persisted layout when present, else a
  default synthesized from enabled `app` plugins + system tiles. `updated_at`
  is `null` for defaults, set when persisted.
- `PUT /api/dashboard/layout` — 200 on save, 409 on any pair of overlapping
  block rectangles, 422 on schema-invalid bodies (Pydantic).

**Files added**

- `apps/hub/api/app/dashboard.py` — default layout generator + collision
  validator (half-open rectangle intersection).
- `apps/hub/api/app/schemas_dashboard.py` — `LayoutBlock` (validated input
  shape), `DashboardLayoutBody` (PUT body), `DashboardLayoutResponse`
  (passes blocks through as stored dicts so PUT-then-GET round-trips byte
  exactly — see note below).
- `apps/hub/api/app/models_dashboard.py` — single `dashboard_layouts` row
  per `user_id` (MVP: `"local"`), JSON `blocks` blob, `version`, `columns`,
  `updated_at`.
- `apps/hub/api/alembic/versions/0002_dashboard_layouts.py` — table migration.
- `apps/hub/api/app/routes/dashboard.py` — wired in `app/main.py`.
- `tests/api/test_dashboard.py` — 10 cases (0/1/N defaults, wrap, ordering,
  PUT round-trip, 409, 422 ×3, adjacent-not-collision).

**Naming note**

Spec lists `app/schemas/dashboard.py` and `app/models/dashboard_layout.py`
(subdirs). Existing `app/` uses **flat** `schemas.py` / `models.py` files,
so this ticket uses flat `schemas_dashboard.py` / `models_dashboard.py` to
mirror the repo pattern. The route lives under `app/routes/dashboard.py`
exactly as spec'd.

**T-FR-0006-01 coordination**

`/api/system/tiles` is owned by T-FR-0006-01 and not yet merged into
`feat/FR-0006-design-language` as of this work. Implemented
`get_system_tiles_for_user(user_id) -> list[dict]` as a stub returning `[]`
in `app/dashboard.py`. When T-01 lands, swap the stub for a call into
`app/system_tiles.py`. **No T-01 files were modified.**

**Block JSON shape**

`blocks[]` only carries `app-shortcut`, `widget`, and `system` blocks.
`strip` blocks are intentionally rejected by `LayoutBlock` (422) because
they are surfaced separately by `GET /api/system/strips` per
`dashboard.md` § "`strip` block — content and configuration".

**Round-trip serialization**

`DashboardLayoutResponse.blocks` is typed `list[dict[str, Any]]` rather than
`list[LayoutBlock]`. Persisting validated dicts with `exclude_none=True` and
returning them as-is avoids re-introducing `surface: None` on
`app-shortcut` blocks — clients see exactly what they sent.

**Default layout ordering**

Plugins are ordered by `name`. `[ui.nav].order` from the Tinder manifest is
not present on the `Plugin` SQLA model in v0; once that field lands the
ordering helper in `app/dashboard.py::list_enabled_app_plugins` updates to
the documented composite key.

**VAL**

- `./develop test tests/api/test_dashboard.py` — 10 passed.
- `./develop test tests/api` — 76 passed (no regressions).
