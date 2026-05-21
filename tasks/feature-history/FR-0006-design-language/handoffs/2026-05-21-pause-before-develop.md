# Handoff — pause before develop (FR-0006)

**Date:** 2026-05-21 · **Status:** design complete, paused before implementation · **No closeout** (feature is not complete).

## Where we are

- All FIX-tier audit items closed in `docs/design/{dashboard.md, mantle-ui.md, plugin-contract.md, mockups/README.md}` (commit `e383868`).
- FR-0006 design skeleton (`10-design-00-skeleton.md`), DAG (`20-tickets-dag.md`), and canonical tickets (`tickets.md`) authored (commit `8fb2559`).
- 15 tickets registered in `tasks/ticket-progress.md` (`T-FR-0006-01..15`).
- Tag reservations pushed (`DG-U2..U11`, `DG-T1`, `DF-U1..U3`, `RW-U3`, `RW-U4`).

## Why we paused

User validates the plan before any implementation begins. Resume is **manual** via `/feature-request-continue`.

## Resume contract — what to do when restarted

When the user runs `/feature-request-continue` (in this repo or via the projects-root coordinator), execute the following **without re-asking** for the develop-or-stop decision:

1. **Verify nothing has shifted on `main`:**
   - `git fetch && git log --oneline origin/main ^HEAD || true` — if anything beyond `8fb2559` appears, summarise it before acting.
2. **Create the feature integration worktree:**
   - `git worktree add .worktrees/FR-0006-design-language/feature feat/FR-0006-design-language` (branch off current `origin/main`).
   - Initialise repo-root `CURRENT.md` on that branch (`docs/ai-context.md` § Branch state).
3. **Update `tasks/ticket-progress.md` → Current focus + Parallel streams:**
   - Active ticket: `T-FR-0006-01` (smallest eligible W0 starter); Session status `developing`; Parallel streams row for FR-0006.
4. **Launch `/develop-frontier`** with **W0 parallel-capable** tickets in **all three repos** as the user-confirmed scope:
   - **This repo:** `T-FR-0006-01` (system tiles & strips API), `T-FR-0006-02` (dashboard layout API), `T-FR-0006-03` (Mantle postMessage bridge), `T-FR-0006-10` (`@kindling/mantle` scaffold).
   - **kindling:** `T-FR-0001-01` (Python template tokens + theme listener) — see [`kindling/tasks/feature-history/FR-0001-plugin-ui-system/handoffs/2026-05-21-pause-before-develop.md`](https://github.com/mcelhennyi/kindling/blob/main/tasks/feature-history/FR-0001-plugin-ui-system/handoffs/2026-05-21-pause-before-develop.md).
   - **grocery-list:** `T-FR-0002-01` (Vite + React scaffold) — see [`grocery-list/tasks/feature-history/FR-0002-mantle-ui/handoffs/2026-05-21-pause-before-develop.md`](https://github.com/mcelhennyi/grocery-list/blob/master/tasks/feature-history/FR-0002-mantle-ui/handoffs/2026-05-21-pause-before-develop.md).
   - **Six subagents in parallel**, one per ticket; one child worktree per ticket under each repo's `.worktrees/FR-NNNN-<slug>/`.
5. **Cross-repo coordination:** kindling T-FR-0001-02 and grocery T-FR-0002-02..08 soft-depend on hearth `T-FR-0006-15` (npm publish). Do **not** block W0; those dependent tickets stay pending until hearth T-FR-0006-10..14 are VAL-done and T-FR-0006-15 publishes.

## Out of scope on resume

- Do **not** open the default-branch PR until **§2d feature-complete gate** is met for FR-0006 (every `### T-FR-0006-xx` is VAL `done` in `tasks/ticket-progress.md`).
- Do **not** write `90-closeout.md` until feature-complete.
- Do **not** delete remote `feat/*` branches at any point.

## Executive summary

Design closed; tickets ready; full W0 (6 parallel subagents across 3 repos) authorised for next session.

## Suggested next step (for the resuming agent)

Run `/feature-request-continue` here, then immediately execute the **Resume contract** steps above without further prompts.

## Options on resume (only if state changed)

- **A. Same plan (default)** — follow the resume contract above. Use unless something below applies.
- **B. State drift on `main`** — if new commits beyond `8fb2559` exist that touched FR-0006 files, re-run the audit summary and present options before launching `/develop-frontier`.
- **C. User overrides scope** — if the user pivots (e.g., "do only hearth FR-0006"), reduce the subagent set and update `ticket-progress.md` accordingly.
