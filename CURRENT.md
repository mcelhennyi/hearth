# Current branch state

| Field | Value |
|------|--------|
| **FR** | FR-0003 |
| **Feature folder** | `tasks/feature-history/FR-0003-hearth-pi-docker-cli/` |
| **This branch** | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-01-deployment-docker-pi` |
| **Parent branch** | `feat/FR-0003-hearth-pi-docker-cli` |
| **Last meaningful update** | 2026-05-10 |

## What is on this branch

- **`T-FR-0003-01` VAL complete:** `docs/design/deployment.md` documents the **Docker (Pi) profile** (supervisor choice, `heart/` ↔ `/opt`/`/var`/`/etc` mapping, bootstrap mermaid, update intent, **DESIGN-GAP** stubs). **Bare-metal** `deploy/install.sh` / systemd path labeled **alternative**; no contradictory Pi-only-systemd wording.
- **`tasks/ticket-progress.md`:** T-FR-0003-01 TEST/DEV/VAL **done**.
- **`docs/design/tickets-initial.md`:** `triadDone` for **TFR0003_01_***.
- **Diary:** [`serial-diary.md`](tasks/feature-history/FR-0003-hearth-pi-docker-cli/serial-diary.md) — TEST mapping + branch naming note (hyphenated ticket branch; Git ref nesting).

## In flight / blockers

- None for **T-FR-0003-01**. Next eligible: **`T-FR-0003-02`**, **`T-FR-0003-13`** (after merge to feature branch).

## Next

1. Open PR **into** `feat/FR-0003-hearth-pi-docker-cli`; merge then proceed **`T-FR-0003-02`** (install layout).
