# CURRENT — `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-12-smoke-arm-ci`

**FR:** `FR-0003` — ticket **`T-FR-0003-12`** (smoke + ARM CI)  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-12-smoke-arm-ci/`

## Status

- **TEST / DEV / VAL:** complete on this branch.
- **Smoke:** `./scripts/ci/hearth-install-smoke.sh` — dry-run `./install`, materialized `heart/` tree, `hearth version` / `doctor` / `--plugin list`, optional `docker compose config` when Docker is on PATH.
- **CI:** `.github/workflows/hearth-install-smoke.yml` — matrix **`ubuntu-latest`** (amd64) + **`ubuntu-24.04-arm`** (arm64).

## Next

1. Merge this branch into **`feat/FR-0003-hearth-pi-docker-cli`** and push.  
2. Open or update the feature PR to **`main`** (`finish-feature` workflow).  
3. Real Pi hardware timing remains an operator follow-up (documented in `serial-diary.md` for this ticket).
