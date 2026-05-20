# Current branch state

**Branch:** `feat/FR-0001-hearth-platform/T-FR-0001-08-groceries-plugin`
**Status:** T08 DEV complete; VAL deferred to manual (iPhone PWA); PR to feat branch pending

## What was done (T-FR-0001-08)

- Scaffolded `grocery-list` repo with FastAPI backend, SQLite persistence, Spark publish, vanilla JS UI
- `tinder.toml` with kind=app, capabilities.list, spark permissions
- Pushed grocery-list to `git@github.com:mcelhennyi/grocery-list.git`
- Added as git submodule at `apps/groceries/`
- 4 unit-level install tests in `tests/integration/test_groceries_install.py`
- `tests/integration/conftest.py` with TestClient fixture
- `integration` mark registered in `pyproject.toml`
- 210 tests pass via Docker

## Next step

- Merge T08 branch into `feat/FR-0001-hearth-platform`
- Run `/identify-frontier` → T-FR-0001-10 (Pi/Mac mini install + backup) becomes eligible
- Manual VAL for T08: iPhone PWA walkthrough (install groceries, add item, check mobile feel)
