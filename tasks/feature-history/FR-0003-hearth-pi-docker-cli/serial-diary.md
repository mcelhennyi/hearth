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
