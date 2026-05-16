# FR-0003 — Hearth Pi Docker CLI and install bootstrap

**Status:** `integrating` — all **`T-FR-0003-xx`** tickets **VAL `done`** on **`feat/FR-0003-hearth-pi-docker-cli`**; [**PR #13**](https://github.com/mcelhennyi/hearth/pull/13) targets **`main`** (see [`REGISTRY.md`](../REGISTRY.md)).  
**Canonical tickets:** [`tickets.md`](tickets.md)  
**DAG draft:** [`20-tickets-dag.md`](20-tickets-dag.md)

**Relationship to FR-0002:** No **`Deps:`** edge from any **`T-FR-0003-xx`** to FR-0002. FR-0002 (PWA prototype) and FR-0003 (Pi Docker CLI) may proceed on parallel timelines; **hub HTTP health**, **prod Compose images**, and **Mantle routes** may use **fixtures / placeholders** until FR-0001 hub + FR-0002 shell artifacts exist (already anticipated in [`10-design-00-skeleton.md`](10-design-00-skeleton.md) and ticket VAL notes).

**Schedule:** Feature integration complete on branch; human merge of **PR #13** then **`90-closeout.md`**. Optional: Pi-class run of **`scripts/ci/hearth-install-smoke.sh`** (append timing to [`serial-diary.md`](serial-diary.md)).

## Process rule (Hearth CLI parity)

New **operator-facing** platform behavior for this line of work should ship through **`hearth`** and per-plugin **`plugin`** on the Compose / Pi path (see [Docker profile (Pi)](../../../docs/design/deployment.md#docker-profile-pi) in [`docs/design/deployment.md`](../../../docs/design/deployment.md)), or land with an explicit **follow-up ticket** titled for **`identify-frontier`** plus a diary note — same wording as **`.cursor/rules/stack-conventions.mdc`** and **`.claude/rules/development-standards.md`**. Admin web UI may wrap the same contracts later; it does not replace the SSH-first operator surface.

## One-screen summary

Deliver a **Docker Compose–first** production install path for Raspberry Pi class hosts: a repo-root **`./install`** bootstrap (system prep including Docker Engine where needed, layout under **`<install-dir>/hearth`**, first boot via Compose), a user-facing **`hearth`** command (update, plugin add/list/enter, stack status/logs/start/stop, doctor, compose passthrough), and a per-plugin **`plugin`** executable under **`<install-dir>/hearth/plugins/<slug>/plugin`** with lifecycle and admin passthrough — aligned with Kindling’s **`install`** hook for plugins.

**Design tension (resolved in tickets):** [`docs/design/deployment.md`](../../../docs/design/deployment.md) today emphasizes **systemd + bare metal** for Pi; this feature **adds** a documented Docker-on-Pi profile and amends deployment authority so both paths are explicit (see [T-FR-0003-01](tickets.md#t-fr-0003-01--design-contract-amend-deployment-for-docker-on-pi)).

## Artifact index

| File | Role |
|------|------|
| [`00-intake.md`](00-intake.md) | Raw request and success criteria |
| [`10-design-00-skeleton.md`](10-design-00-skeleton.md) | L0 contracts (CLI, layout, data) |
| [`20-tickets-dag.md`](20-tickets-dag.md) | Ticket table + Mermaid DAG |
| [`tickets.md`](tickets.md) | Canonical **`### T-FR-0003-xx`** sections |
| [`serial-diary.md`](serial-diary.md) | Serial session log |
| [`handoffs/2026-05-16-finish-feature.md`](handoffs/2026-05-16-finish-feature.md) | Finish-feature integration handoff (PR #13) |
| [`../../../scripts/ci/hearth-install-smoke.sh`](../../../scripts/ci/hearth-install-smoke.sh) | Host/CI smoke for `./install` + `hearth` (**T-FR-0003-12**); see also [`.github/workflows/hearth-install-smoke.yml`](../../../.github/workflows/hearth-install-smoke.yml) |
| [`../../../deploy/hearth-install/README.md`](../../../deploy/hearth-install/README.md) | **`hearth/`** layout generator, **`VERSION.json`** schema v1, operator templates (**T-FR-0003-02**) |
| [`../../../deploy/kindling-contract/README.md`](../../../deploy/kindling-contract/README.md) | Hearth-side Kindling plugin template mirror: `plugin` shim + `scripts/install` hook (**T-FR-0003-10**) |
| [`handoffs/2026-05-09-operator-option-a.md`](handoffs/2026-05-09-operator-option-a.md) | Historical: scheduling-only deferral (option A), superseded for FR-0003 by [`handoffs/2026-05-10-unpark-start-implementation.md`](handoffs/2026-05-10-unpark-start-implementation.md) |
| [`handoffs/2026-05-10-unpark-start-implementation.md`](handoffs/2026-05-10-unpark-start-implementation.md) | Unpark FR-0003; no FR-0004 split — start implementation now |

## Deferred (follow-up FRs)

- **Central plugin registry / relay names** for `hearth --plugin --add` — MVP is **git URL** (and optional local path); registry resolution is **`DESIGN-GAP`** until the relay exists.
- **Admin-scoped web UI** calling the same operations — track as a separate FR once hub auth and API surfaces exist; this FR defines **CLI contracts** that the UI can wrap.
