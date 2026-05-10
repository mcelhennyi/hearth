# CURRENT — `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-04-cli-core`

**Ticket:** `T-FR-0003-04` — `hearth` CLI core: argparse, paths, doctor, compose passthrough
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-04-cli-core/`
**Phase:** PR

## Plan

1. Add CLI contract tests for install-root resolution, `VERSION.json` loading, `doctor`, `compose --`, `version`, and help output.
2. Implement a small Python CLI package plus `bin/hearth` shim in a single home.
3. Validate through `./develop test` where Docker is available, with documented host-local exceptions if needed.

## Current Status

- Worktree created from `feat/FR-0003-hearth-pi-docker-cli`.
- TEST done: `tests/test_hearth_cli.py` covers install-root resolution, `VERSION.json`, graceful `doctor`, `compose --`, and global help.
- DEV done: `deploy/hearth-cli/hearth_cli/cli.py` implements `version`, `doctor`, `compose --`, install-root resolution, and `bin/hearth`.
- VAL done: `./develop test` passes; fixture smoke ran `bin/hearth --install-root <tmp> version`, `doctor`, and `compose -- ps`.
- Docker wrapper note: sandboxed access to the Colima socket was denied, so `./develop test tests/test_hearth_cli.py` was rerun with unrestricted Docker access and reached pytest.
