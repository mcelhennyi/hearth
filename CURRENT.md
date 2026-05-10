# CURRENT — `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-02-install-layout`

**Ticket:** `T-FR-0003-02` — Install layout: `heart/`, VERSION.json, README  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-02-install-layout/`

## Delivered

- **`deploy/hearth-install/`**: `hearth_install` package (`ensure_heart_layout`, `VERSION.json` v1 parser), JSON Schema, templates, module README.
- **Tests:** `tests/test_heart_install_layout.py` (dirs, manifest parse, idempotence).
- **`./develop test`**: Compose profile `test` (`hearth-test` service) runs pytest in `python:3.12-slim-bookworm` (pip needs network on first cold run).
- **Docs:** `docs/design/deployment.md` links schema; feature README artifact index links `deploy/hearth-install/README.md`.

## Verify

```bash
./develop test
```
