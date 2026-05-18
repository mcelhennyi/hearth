# Finish-feature handoff — FR-0003 (2026-05-16)

**Feature:** `FR-0003` — Hearth Pi Docker CLI and install bootstrap  
**Integration branch:** `feat/FR-0003-hearth-pi-docker-cli` @ merge with `origin/main` (finish-feature)  
**PR to `main`:** https://github.com/mcelhennyi/hearth/pull/13

## Executive summary

All **`T-FR-0003-01` … `T-FR-0003-13`** tickets are **TEST / DEV / VAL `done`** on the feature branch, including capstone **`T-FR-0003-12`** (install smoke script + amd64/arm64 GitHub Actions workflow). Ticket/stage branches were merged into **`feat/FR-0003-hearth-pi-docker-cli`** over multiple waves; remote **`feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-*`** branches are retained for audit.

This finish-feature pass merged **`origin/main`** into the feature branch to clear **PR #13** merge conflicts, re-ran validation, and updated process bookkeeping.

## Merged ticket branches (audit)

| Ticket | Remote branch (retained) |
|--------|---------------------------|
| T-FR-0003-01 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-01-deployment-docker-pi` |
| T-FR-0003-02 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-02-install-layout` |
| T-FR-0003-03 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-03-install-bootstrap` |
| T-FR-0003-04 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-04-cli-core` |
| T-FR-0003-05 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-05-plugin-registry-compose` |
| T-FR-0003-06 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-06-update` |
| T-FR-0003-07 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-07-plugin-add-list` |
| T-FR-0003-08 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-08-plugin-enter` |
| T-FR-0003-09 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-09-stack-control` |
| T-FR-0003-10 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-10-kindling-plugin-contract` |
| T-FR-0003-11 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-11-plugin-executable` |
| T-FR-0003-12 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-12-smoke-arm-ci` |
| T-FR-0003-13 | `feat/FR-0003-hearth-pi-docker-cli-T-FR-0003-13-cli-parity` |

Feature tip (latest finish-feature pass): see git log on **`feat/FR-0003-hearth-pi-docker-cli`**.

## Validation summary

- **`./develop test`** — **76 passed** (feature worktree).
- **`./scripts/ci/hearth-install-smoke.sh`** — PASS; workflow **`.github/workflows/hearth-install-smoke.yml`** (amd64 + arm64).
- **Pi hardware VAL** — **PASS** (operator confirmed); steps captured in repo-root **`SETUP.md`**.
- **Design amendment HRT-DEP-001** — install tree **`heart/` → `hearth/`** (code + docs).

## Suggested next step

Human review and **merge PR #13** to **`main`**. On merge:

1. **Delete** repo-root **`CURRENT.md`** from **`main`** (branch-local only).
2. Write **`tasks/feature-history/FR-0003-hearth-pi-docker-cli/90-closeout.md`** and set **`REGISTRY.md`** status.
3. Optionally run **`scripts/ci/hearth-install-smoke.sh`** on a Pi and log results.

## Options

| Option | When |
|--------|------|
| **Merge PR #13** | Default — FR-0003 implementation is complete on the feature branch. |
| **Request changes** | If review finds gaps; fix on **`feat/FR-0003-hearth-pi-docker-cli`** and push (no push to **`main`** from automation). |
| **Defer Pi VAL** | Accept CI smoke only; track Pi run as operator follow-up in **`serial-diary.md`**. |
