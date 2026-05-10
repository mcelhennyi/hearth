# CURRENT — `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-10-kindling-plugin-contract`

**Ticket:** `T-FR-0003-10` — Kindling contract: `scripts/install` + `plugin` template  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-10-kindling-plugin-contract/`
**Branch role:** Ticket branch targeting `feat/FR-0003-hearth-pi-docker-cli`
**Last meaningful update:** 2026-05-10

## Phase

- **VAL done:** Hearth-side Kindling mirror implemented and validated through Docker Compose.

## Delivered

- `deploy/kindling-contract/`: `hearth_kindling_contract` renderer plus mirrored `templates/plugin-python/` containing executable `plugin`, executable `scripts/install`, Tinder metadata, and Python admin passthrough.
- `tests/test_kindling_plugin_contract.py`: contract coverage for template rendering, lifecycle flag handling, install hook delegation, passthrough, and slug validation.
- Docs/tracking: Kindling satellite contract mirror note, FR-0003 artifact index, serial diary, ticket progress row, and global DAG `triadDone`.

## Verify

```bash
./develop test tests/test_kindling_plugin_contract.py
./develop test
```

## Next

- Commit, push, and open PR to `feat/FR-0003-hearth-pi-docker-cli`.
