# FR-0003 — Hearth Pi Docker CLI and install bootstrap

**Status:** `parked` for **implementation** until **FR-0002** closes (see [`REGISTRY.md`](../REGISTRY.md)); design + ticket DAG on `main` are done.  
**Canonical tickets:** [`tickets.md`](tickets.md)  
**DAG draft:** [`20-tickets-dag.md`](20-tickets-dag.md)

**Schedule:** Do **not** open **`feat/FR-0003-hearth-pi-docker-cli`** or start **`T-FR-0003-xx`** TEST/DEV/VAL while **FR-0002** is still in flight. After FR-0002 closes, create the feature worktree and begin with **[T-FR-0003-01](tickets.md#t-fr-0003-01--design-contract-amend-deployment-for-docker-on-pi)** (or run **`/identify-frontier`** if resuming mid-graph). Sequencing next to **FR-0001** is a separate capacity call.

## One-screen summary

Deliver a **Docker Compose–first** production install path for Raspberry Pi class hosts: a repo-root **`./install`** bootstrap (system prep including Docker Engine where needed, layout under **`<install-dir>/heart`**, first boot via Compose), a user-facing **`hearth`** command (update, plugin add/list/enter, stack status/logs/start/stop, doctor, compose passthrough), and a per-plugin **`plugin`** executable under **`<install-dir>/heart/plugins/<slug>/plugin`** with lifecycle and admin passthrough — aligned with Kindling’s **`install`** hook for plugins.

**Design tension (resolved in tickets):** [`docs/design/deployment.md`](../../../docs/design/deployment.md) today emphasizes **systemd + bare metal** for Pi; this feature **adds** a documented Docker-on-Pi profile and amends deployment authority so both paths are explicit (see [T-FR-0003-01](tickets.md#t-fr-0003-01--design-contract-amend-deployment-for-docker-on-pi)).

## Artifact index

| File | Role |
|------|------|
| [`00-intake.md`](00-intake.md) | Raw request and success criteria |
| [`10-design-00-skeleton.md`](10-design-00-skeleton.md) | L0 contracts (CLI, layout, data) |
| [`20-tickets-dag.md`](20-tickets-dag.md) | Ticket table + Mermaid DAG |
| [`tickets.md`](tickets.md) | Canonical **`### T-FR-0003-xx`** sections |
| [`serial-diary.md`](serial-diary.md) | Serial session log |
| [`handoffs/2026-05-09-operator-option-a.md`](handoffs/2026-05-09-operator-option-a.md) | Schedule: defer implementation until FR-0002 closes (option A) |

## Deferred (follow-up FRs)

- **Central plugin registry / relay names** for `hearth --plugin --add` — MVP is **git URL** (and optional local path); registry resolution is **`DESIGN-GAP`** until the relay exists.
- **Admin-scoped web UI** calling the same operations — track as a separate FR once hub auth and API surfaces exist; this FR defines **CLI contracts** that the UI can wrap.
