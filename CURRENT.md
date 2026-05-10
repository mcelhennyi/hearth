# CURRENT — `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-03-install-bootstrap`

**Ticket:** `T-FR-0003-03` — `./install` bootstrap (Docker + layout + first `compose up`)  
**FR:** `FR-0003`  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-03-install-bootstrap/`  
**Phase:** VAL complete — ready for PR into `feat/FR-0003-hearth-pi-docker-cli`

## Done this branch

- Repo-root `./install` wrapper + `hearth_install.bootstrap` (dry-run, layout, shim, compose template, plugin overrides, `docker compose up -d`).
- Tests + serial diary entry; `deploy/hearth-install/README.md` updated.

## Validation

- `./develop test` — full suite PASS.
- Host-local: `docker compose config` on generated project — PASS (documented in serial diary).

## Next

- Push branch; open PR **base** `feat/FR-0003-hearth-pi-docker-cli`.
- Feature owner merges ticket branch into feature integration worktree and reruns `./develop test`.
