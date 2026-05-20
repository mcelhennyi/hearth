# Current branch state

**Branch:** `feat/FR-0001-hearth-platform-T-FR-0001-07-kindling-repo`
**Status:** T-FR-0001-07 complete (TEST/DEV/VAL done); 198 tests passing

## What was done (this ticket)

- Created `kindling/` local directory (scope-right: separate repo/submodule deferred)
- Migrated tinder schema → `kindling/tinder/schema.py`
- Migrated Spark Python client → `kindling/spark/python/client.py`
- Migrated Spark TS client → `kindling/spark/typescript/client.ts`
- Migrated Mantle components → `kindling/mantle/`
- Implemented `kindling_cli` Python package (`kindling new`, `kindling validate`, `kindling install`)
- Added `kindling` script entry point to `pyproject.toml`
- 17 new tests in `tests/test_kindling_cli.py`; 198 total pass via Docker

## Next step

Merge T-FR-0001-07 PR into `feat/FR-0001-hearth-platform`; then eligible next:
- **T-FR-0001-05** (Caddy generation + local TLS)
- **T-FR-0001-08** (groceries reference plugin) — now unblocked by T07
