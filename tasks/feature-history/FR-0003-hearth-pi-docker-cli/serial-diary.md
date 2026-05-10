---

## 2026-05-10 — T-FR-0003-08 TEST→DEV→VAL (`hearth --plugin enter`)

**Branch:** `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-08-plugin-enter`  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-08-plugin-enter/`

### TEST

- Added `hearth_install.plugin_session` (`HEARTH_PLUGIN_ENTER_STACK` JSON array + `HEARTH_PLUGIN_ENTER_FROM`) and `tests/test_plugin_enter_session.py` for push/pop nesting, `exit_plugin_enter_session`, and malformed-stack errors.

### DEV

- `hearth --plugin enter [--slug SLUG]` — interactive **bash/zsh** via `exec $SHELL -i` after `chdir` to `heart/plugins/<slug>`; non-TTY prints `cd` + `export` fallback. Numbered picker when TTY and `--slug` omitted.
- Kindling template `plugin` implements real `./plugin --exit` when `hearth_install` is importable (reuses `plugin_session`).
- Documented operator UX under `deploy/hearth-install/README.md`.

### VAL

- `docker compose -f deploy/compose/docker-compose.yml --profile test run --rm hearth-test` — **PASS** (59 tests).
- **Host-local / manual:** full **enter → `./plugin status` → `--exit`** REPL smoke is intentionally not automated (requires interactive TTY + real shell); deterministic coverage is the pytest suite above.

---

## 2026-05-10 — T-FR-0003-03 TEST→DEV→VAL (`./install` bootstrap)

**Branch:** `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-03-install-bootstrap`  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-03-install-bootstrap/`

### TEST

- Added `tests/test_install_bootstrap.py`: `--dry-run` leaves install root untouched; `--skip-compose-up` materializes layout + shim; mocked `docker compose up`; empty plugin registry emits valid `services: {}` for Compose `include`.

### DEV

- Repo-root `./install` thin bash wrapper → `python -m hearth_install.bootstrap`.
- `hearth_install.bootstrap`: layout (`ensure_heart_layout`), packaged `docker-compose.install.yml` → `heart/compose/docker-compose.yml` (hub-smoke placeholder + `include` of generated plugins), plugin compose generation, `heart/bin/hearth` symlink to repo `bin/hearth`, optional `docker compose up -d`.
- Docker Engine install is intentionally **not** scripted (host mutation); missing daemon prints Pi-oriented hints + Docker docs link.
- `plugin_compose._render_compose`: empty enabled plugins → `services: {}` for valid YAML merge.

### VAL

- `./develop test` — PASS (full suite in Compose `hearth-test`).
- Host-local (documented exception): `docker compose config` against a temp install produced by `--skip-compose-up` — PASS on developer macOS (validates `include` + hub-smoke placeholder).

---

## 2026-05-10 — T-FR-0003-06 TEST→DEV→VAL (`hearth --update`)

**Branch:** `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-06-update`  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-06-update/`

### TEST

- Added `tests/test_hearth_update.py` with mocked `git`/`docker compose` subprocesses, dry-run idempotence, deploy ref change + `VERSION.json` rewrite, and CLI mutual-exclusion checks.

### DEV

- Implemented `hearth_cli/update_cmd.py`: deploy `git pull --ff-only`, plugin dir refresh from `plugins.yaml`, `generate_plugin_compose`, optional executable `heart/bin/hearth-migrate`, `docker compose up -d --pull always`.
- Split `ResolvedInstall` / `resolve_install` into `hearth_cli/install_context.py` to avoid circular imports.
- Documented behavior under **Updates** in `docs/design/deployment.md`.

### VAL

- `./develop test` — **PASS** (26 tests).
- Host-local: `bin/hearth --install-root <temp git+heart> --update --dry-run` run twice; output identical (**no-op**). Full non-dry-run update not exercised here (requires real Compose stack + network pull).

---

## 2026-05-10 — T-FR-0003-07 TEST→DEV→VAL (hearth --plugin --add / list)

**Branch:** `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-07-plugin-add-list`  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-07-plugin-add-list/`

### TEST

- Added `tests/test_hearth_plugin_commands.py` for classify errors, local tree add/list, shallow git clone fixtures, CLI wiring, registry serialization round-trip, and `scripts/install` execution via local stub.

### DEV

- `hearth_install.tinder_manifest` — MVP `tinder.toml` validation aligned with FR-0003 install needs.
- `hearth_install.plugin_add` — classify sources (reject OCI / registry shorthand per ticket), shallow `git clone` or filesystem copy, `scripts/install`, registry append (`save_plugin_registry`), `generate_plugin_compose`, optional `docker compose up -d <slug>` when base compose exists.
- `hearth_install.plugin_compose.save_plugin_registry` — round-trip YAML for schema v1 dialect.
- `hearth_cli.cli` — `hearth --plugin --add <url-or-path>` and `hearth --plugin list`.

### VAL

- `./develop test` — PASS (24 tests). `deploy/compose/hearth-test-entry.sh` installs **`git`** in the test image once so clone-based tests run in Docker (host `python3` runs were ad hoc only).

---

## 2026-05-10 — T-FR-0003-09 TEST→DEV→VAL (stack control)

**Branch:** `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-09-stack-control`  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-09-stack-control/`

### TEST

- Extended `tests/test_hearth_cli.py` with parametrized stack-command assertions and coverage for `--project-name`, `heart/compose/.env`, and status health probing.

### DEV

- `hearth start|stop|restart|status|logs` map to docker compose with shared `--project-name` (default `hearth`, override `HEARTH_COMPOSE_PROJECT_NAME`) and optional `heart/compose/.env` or `HEARTH_COMPOSE_ENV_FILE`.
- `hearth compose` uses the same prefix; `hearth status` runs `ps -a` then optionally GETs `/api/health` via `HEARTH_HUB_HEALTH_URL` or `docker compose port hub <port>` discovery (`--skip-health` to skip).

### VAL

- `./develop test tests/test_hearth_cli.py` and `./develop test` — PASS (Docker `hearth-test` profile). No host-local test exception.

---

## 2026-05-10 — T-FR-0003-10 TEST→DEV→VAL (Kindling plugin contract)

**Branch:** `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-10-kindling-plugin-contract`  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-10-kindling-plugin-contract/`

### TEST

- Confirmed there is no `vendor/kindling/` checkout or public Kindling submodule in this repo state, so the ticket is implemented as a Hearth-side mirror per the ticket instruction.
- Added `tests/test_kindling_plugin_contract.py` to assert a rendered plugin root contains executable `plugin`, executable `scripts/install`, `tinder.toml`, and a Python admin passthrough target.
- Initial focused test failed as expected with `ModuleNotFoundError: No module named 'hearth_kindling_contract'`.

### DEV

- Added `deploy/kindling-contract/` with `hearth_kindling_contract.render_plugin_template(...)` and the mirrored `templates/plugin-python/` contract.
- Documented the mirror in `deploy/kindling-contract/README.md`, linked it from the FR-0003 artifact index, and amended the Kindling satellite design to state the temporary mirror and replacement rule once upstream Kindling exists.
- Upstream/submodule PR note: not applicable yet because Kindling is design-only; this ticket's PR into `feat/FR-0003-hearth-pi-docker-cli` is the implementation link.

### VAL

- `./develop test tests/test_kindling_plugin_contract.py` — PASS (4 tests, Docker Compose `hearth-test` service).
- `./develop test` — PASS (11 tests, Docker Compose `hearth-test` service).
- No host-local validation exception; tests ran through `./develop`.

---

## 2026-05-10 — T-FR-0003-05 TEST→DEV→VAL (plugin registry compose)

**Branch:** `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-05-plugin-registry-compose`  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-05-plugin-registry-compose/`

### TEST

- Added golden-file coverage for **`heart/state/plugins.yaml`** to **`heart/compose/overrides/generated.plugins.yml`**.
- Covered enabled-only output, image and build-context services, plugin env injection, default registry idempotence, and missing enabled plugin dirs.

### DEV

- Implemented `hearth_install.plugin_compose`: schema-v1 registry reader, validation, default registry writer, and deterministic Compose override rendering.
- Wired `ensure_heart_layout()` to create **`state/plugins.yaml`** and added `python -m hearth_install --generate-plugin-compose`.
- Updated install-layout docs/templates to document the registry and generated override.

### VAL

- Containerized tests: `./develop test` — **PASS** (`10 passed`).
- Compose config check: generated two fake plugin services from a temp **`heart/`** tree and ran `docker compose -f <generated.plugins.yml> config --quiet` — **PASS**.
- Integration smoke: `docker compose -f <generated.plugins.yml> up -d` with two `busybox:1.36` fake plugin services — **PASS**; both services reached running state and were stopped with `docker compose down`.
- Host-local exception: the temp fixture generator used host `python3` with `PYTHONPATH=deploy/hearth-install` because the validation target was the generated file consumed by Docker Compose; tests themselves ran inside the repo's Docker Compose `hearth-test` service.

---

## 2026-05-10 — T-FR-0003-01 TEST→DEV→VAL (deployment Docker-on-Pi)

**Branch:** `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-01-deployment-docker-pi`  
**Worktree:** `.worktrees/FR-0003-hearth-pi-docker-cli/T-FR-0003-01-deployment-docker-pi/`

### TEST — skeleton → `docs/design/deployment.md` mapping

| Skeleton slice (`10-design-00-skeleton.md`) | Covered in `deployment.md` |
|---------------------------------------------|----------------------------|
| Purpose (Compose on Pi, contracts) | Opening **Authority** paragraph + **Docker profile (Pi)** |
| Actors (operator, `./install`, `hearth`, Compose vs systemd) | **Targets** table (Pi rows), **Docker profile** supervisor vs **systemd units (prod, bare-metal alternative)** section |
| Install root / `HEARTH_INSTALL_ROOT`, `heart/` | **Docker profile** operator + mapping table |
| Public surfaces (`VERSION.json`, registry, compose paths, CLIs) | Mapping table rows + **Updates** (`hearth --update` intent) + cross-links to skeleton/README |
| `hearth` / `plugin` CLI sketches | **Updates** + pointer to skeleton for full flag matrix (not duplicated) |
| Data in/out (`heart/var`, plugins, secrets) | Mapping table (`heart/var/`, `heart/plugins/`) |
| Sequencing vs `deployment.md` / `install.sh` tension | Authority paragraph (pick one profile); **Install script** renamed bare-metal; FR-0003 `./install` called out |
| Open questions (image build, rootless, hub vs file-first) | **DESIGN-GAP — Docker profile** |

**Note:** Git cannot nest branch refs `feat/…/T-…` under `feat/FR-0003-hearth-pi-docker-cli`; ticket branch is `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-01-deployment-docker-pi` (same pattern as FR-0002 ticket branches).

### DEV

Amended **`docs/design/deployment.md`**: Pi **Docker profile** with mermaid bootstrap flow, mapping table, explicit **DESIGN-GAP** list, systemd path labeled **bare-metal alternative**, install section scoped to **`deploy/install.sh`**.

### VAL

- **`T-FR-0001-10`** still references `deploy/install.sh` idempotently; link from deployment doc uses anchor to `tickets.md#…` path unchanged for parsers.
- Docs site: `docker compose … run docs build --strict` — **PASS** (2026-05-10).

---

## 2026-05-10 — Unpark implementation (operator)

**Stage:** policy / branch bootstrap

**Recap:** Confirmed **no `T-FR-0003-xx` dependency on FR-0002**; prior park was option A scheduling only. Set FR-0003 to **`in-progress`** in [`REGISTRY.md`](../REGISTRY.md), opened **`feat/FR-0003-hearth-pi-docker-cli`** + repo-root **`CURRENT.md`**, updated [`tasks/ticket-progress.md`](../../ticket-progress.md) and global [`tasks/handoffs/2026-05-10-fr0003-unpark.md`](../../handoffs/2026-05-10-fr0003-unpark.md). **No FR-0004** — stubs in existing tickets suffice for FR-0002 coupling.

**Next:** **[T-FR-0003-01](tickets.md#t-fr-0003-01--design-contract-amend-deployment-for-docker-on-pi)** TEST→DEV→VAL or **`/identify-frontier`**.

---

## 2026-05-09 — Operator choice: defer implementation (option A)

**Stage:** scheduling

**Recap:** Requester chose **option A**: stay **design-only on `main`** until **FR-0002** settles; **do not** open **`feat/FR-0003-hearth-pi-docker-cli`** or start **`T-FR-0003-xx`** until then. [`REGISTRY.md`](../REGISTRY.md) status set to **`parked`** with this note.

**Next:** After FR-0002 closeout, flip FR-0003 toward **`in-progress`** in the registry when the feature branch exists, then **`/identify-frontier`** → **`/develop-frontier`** starting with **[T-FR-0003-01](tickets.md#t-fr-0003-01--design-contract-amend-deployment-for-docker-on-pi)** (or the parallel batch allowed by deps).

---

## 2026-05-09 — Intake + design + tickets (agent)

**Stage:** Stage 0–2 (intake, L0 design, ticket DAG)

**Recap (plain English):** Registered **[FR-0003](../REGISTRY.md)** as **Hearth Pi Docker CLI** (`hearth` + `./install` + per-plugin `plugin`). Wrote intake, skeleton contracts (install tree **`<install-dir>/heart`**, MVP git-only plugin add, explicit **DESIGN-GAP** for central registry), and **13** implementation tickets with a wide parallel front after **T-FR-0003-02**. Noted tension with **`docs/design/deployment.md`** systemd-first Pi story — **T-FR-0003-01** amends docs for a **Docker profile**. **T-FR-0003-13** lands **CLI parity** rules in Cursor + Claude stacks. No code or **`feat/`** branch yet.

**Next:** Superseded by operator **option A** (above): no FR-0003 implementation until **FR-0002** closes.
