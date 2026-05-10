# CURRENT — `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-05-plugin-registry-compose`

**Ticket:** `T-FR-0003-05` — Plugin registry file + Compose fragment generation  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-05-plugin-registry-compose/`  
**Phase:** complete

## Delivered So Far

- Added golden tests for `heart/state/plugins.yaml` to `heart/compose/overrides/generated.plugins.yml`.
- Implemented a stdlib-only schema-v1 registry reader and Compose override generator in `deploy/hearth-install/`.
- `ensure_heart_layout()` now creates an idempotent default plugin registry.
- Containerized tests passed: `./develop test tests/test_plugin_compose_generation.py tests/test_heart_install_layout.py`.
- Full validation passed: `./develop test`, `docker compose config --quiet`, and a two-fake-plugin `docker compose up -d` smoke.
- Updated `tasks/ticket-progress.md`, `serial-diary.md`, and `docs/design/tickets-initial.md` for `T-FR-0003-05`.

## Next

1. Commit and push this ticket branch.
2. Open a PR into `feat/FR-0003-hearth-pi-docker-cli`.
