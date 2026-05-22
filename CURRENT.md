# CURRENT — T-FR-0006-02 Dashboard layout API

**Branch:** `feat/FR-0006-design-language-T-FR-0006-02-dashboard-layout`  
**Worktree:** `.worktrees/FR-0006-design-language/T-FR-0006-02-dashboard-layout/`  
**Ticket:** T-FR-0006-02 · **FR-0006** design-language

## Phase status

| Phase | Status | Notes |
|-------|--------|-------|
| TEST | done | `tests/api/test_dashboard.py` — 10 tests (default 0/1/N plugins, round-trip, collision 409, validation 422). |
| DEV | done | `app/dashboard.py`, `schemas_dashboard.py`, `routes/dashboard.py`, `models_dashboard.py`, alembic `0002_dashboard_layouts`, router in `main.py`. |
| VAL | done | `./develop test tests/api/test_dashboard.py -q` — 10 passed in Docker. OpenAPI includes `/api/dashboard/layout`. |

## Test command

```bash
./develop test tests/api/test_dashboard.py -q
```

(`./develop api pytest …` uses hub `WORKDIR=/app`; use `/workspace/tests/api/…` or prefer `./develop test`.)

## Next step

Open PR to `feat/FR-0006-design-language`; merge after review. Unblocks **T-FR-0006-07** (dashboard grid).
