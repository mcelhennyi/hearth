# FR-0000 closeout — Repository bootstrap

**Closed:** 2026-05-19 — work landed on **`main`** via **`init-skeleton`** (no feature PR; tooling-only scope).

## Executive summary

**FR-0000** established the Hearth repository as a **process- and stack-scaffolded** project: **`.skeleton/`** submodule, AI dev workflow (**`docs/ai-context.md`**, **`.cursor/`**, **`.claude/`**), feature/ticket tracking (**`tasks/`**), authoritative **product design** under **`docs/design/`**, and a recorded **technology stack** in **`.cursor/rules/stack-conventions.mdc`**. Product implementation (Compose dev loop, hub apps tree) is explicitly owned by **FR-0001** (**`T-FR-0001-01`** onward), not this FR.

## Delivered surfaces

| Surface | Location |
|---------|----------|
| Skeleton submodule + sync | `.skeleton/`, `./sync-skeleton`, `skeleton.manifest` |
| Stack conventions | `.cursor/rules/stack-conventions.mdc` |
| Architecture + design corpus | `docs/design/` (overview, deployment, mantle-ui, …) |
| Feature / ticket process | `tasks/feature-history/`, `tasks/ticket-progress.md`, `REGISTRY.md` |
| Operator / dev entry | `README.md`, `SETUP.md` (extended by later FRs) |

## Ticket

| Ticket | Summary | Status |
|--------|---------|--------|
| `T-FR-0000-01` | Choose stack and scaffold repository | TEST / DEV / VAL **done** |

## Validation

- **TEST:** `INIT.MD` / skeleton init checklist satisfied for org workflow.
- **DEV:** Root process files, design stubs, and stack rules present; **`./sync-skeleton`** path documented.
- **VAL:** Fresh clone + documented init/sync path reproducible; downstream FRs (**FR-0002**, **FR-0003**) built on this base without reopening bootstrap.

## Deferred / follow-up

| Item | Tracking |
|------|----------|
| Runnable hub + Compose dev loop | **FR-0001** `T-FR-0001-01` |
| Published docs site (MkDocs) | Optional; not required for FR-0000 close |
| Skeleton template improvements | Upstream **`.skeleton/`** + `./sync-skeleton` |

## Suggested next step

Continue **FR-0001** — active ticket **`T-FR-0001-01`** (repo scaffold and Compose dev loop) in worktree `.worktrees/FR-0001-hearth-platform/T-FR-0001-01-repo-scaffold/`.

## Options

| Option | When |
|--------|------|
| **Develop FR-0001** | Default — complete `T-FR-0001-01` TEST→DEV→VAL, merge to `feat/FR-0001-hearth-platform` |
| **`/identify-frontier`** | After more FR-0001 tickets are staffed |
| **`./sync-skeleton`** | When pulling template updates from upstream skeleton |

## Audit

- **Integration:** Direct commits on **`main`** (bootstrap / init-skeleton era); no `feat/FR-0000-*` integration PR.
- **Handoff:** [`handoffs/2026-05-19-closeout.md`](handoffs/2026-05-19-closeout.md)
