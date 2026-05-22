# T-FR-0006-01 — System tiles & strips API — diary

Stream: parallel; branch `feat/FR-0006-design-language-T-FR-0006-01-system-tiles`;
worktree `.worktrees/FR-0006-design-language/T-FR-0006-01-system-tiles/`.

## 2026-05-21 — TEST → DEV plan

- Convert `app/schemas.py` → `app/schemas/__init__.py` package (re-exports
  everything) and add `app/schemas/system.py`. Existing
  `from app.schemas import X` callers stay valid. T-FR-0006-02 needs the same
  package shape (`app/schemas/dashboard.py`).
- New SQLAlchemy table `user_system_state` (PK = `(scope, item_id)` where
  `scope` ∈ {`tile`, `strip`}, `item_id` is the tile/strip id, plus
  `hidden`/`dismissed_at`). v0 is single-user so we omit `user_id` (consistent
  with the rest of the hub API).
- v0 catalogue is hard-coded in `app/system_tiles.py` /
  `app/system_strips.py`. Suppression and "platform" detection are
  deferred-to-client per `docs/design/dashboard.md` (tiles can self-suppress;
  strip selection accepts a `platform` query hint to avoid serving iOS-only
  banners to desktop). Server returns `suppressed=False` by default and lets
  the client decide; this matches the design language ("a tile may
  self-suppress when its precondition is satisfied") without inventing a
  preconditions engine here.
- Alembic migration `0002_user_system_state.py`.
- Tests under `tests/api/test_system.py` reuse the in-memory `client`
  fixture from `tests/api/conftest.py`.

## 2026-05-21 — VAL

Run `./develop test tests/api/test_system.py` and full `./develop test` to
ensure no regression.

## 2026-05-21 — VAL done

- `./develop test tests/api/test_system.py -q` → **16 passed** (hearth-test profile).
- `./develop test tests/api/ -q` → **82 passed** (all API tests).
- `./develop test -q` → full suite green (254 passed, 3 skipped per initial commit).
- OpenAPI: `app.openapi()` lists `/api/system/tiles`, strips, hide/restore/dismiss.
- [PR #31](https://github.com/mcelhennyi/hearth/pull/31) open → `feat/FR-0006-design-language`.
- TEST/DEV/VAL all `done`; `docs/design/tickets-initial.md` triadDone for TFR0006_01.
