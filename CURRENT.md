# CURRENT — `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-06-update`

**Ticket:** `T-FR-0003-06` — `hearth --update`  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-06-update/`  
**Branch:** `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-06-update`  
**Phase:** VAL complete — push + PR to `feat/FR-0003-hearth-pi-docker-cli`.

## Done

- `hearth --update` / `--dry-run`, git + compose + plugin refresh + optional `heart/bin/hearth-migrate`, tests in `tests/test_hearth_update.py`.
- Path resolution split: `hearth_cli/install_context.py` (fixes circular imports with `update_cmd`).

## Validation

- `./develop test` — 26 passed.
- Host VAL: `hearth --update --dry-run` run twice on a temp git-backed `heart/` install; outputs identical (no-op).

## Next

- Open PR to `feat/FR-0003-hearth-pi-docker-cli`.
