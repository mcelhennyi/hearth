## 2026-05-10 — `/develop-frontier 0003` orchestration

**Stage:** policy + queue beacon

**Recap:** Operator invoked **`/develop-frontier 0003`**. Set [`REGISTRY.md`](../REGISTRY.md) FR-0003 → **`in-progress`**, aligned [`README.md`](../README.md) + [`tasks/ticket-progress.md`](../../ticket-progress.md); superseded scheduling-only park for FR-0003. Parallel-capable FR-0003 ticket on current tracker: **`T-FR-0003-01`** only (`Deps: none`). Launched one implementation subagent for that ticket.

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
