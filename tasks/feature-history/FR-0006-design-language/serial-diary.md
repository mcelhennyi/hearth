# FR-0006 — Serial diary

> Append-only. Newest entries at the **bottom** (this file is the raw chain; see `DIARY.md` at closeout for newest-first merged view).

---

## 2026-05-21 — Stage 0: intake + registry reservation

- Allocated **FR-0006 `design-language`** in `tasks/feature-history/REGISTRY.md` (status `design`, next_id → 7).
- Reserved tag ids in `tasks/TAG-REGISTRY.md`: **DG-U2..U11, DG-T1; DF-U1..U3; RW-U3, RW-U4**.
- Pre-design audit performed 2026-05-21 across four quadrants (dashboard, mantle, kindling, grocery-list) — 26 gaps identified, user triaged path A (triage-then-design).
- `@kindling/mantle` package decided as in-scope for this FR (user choice 2026-05-21).
- Authored `README.md` and `00-intake.md` for this FR folder.

## 2026-05-21 — Stage 1: design amendments

- Amended `docs/design/dashboard.md` (DG-U2/U3/U4/U5/U10, DF-U1/U2, RW-U3/U4): edit-mode UX, collisions, empty state, grid metrics, `system` and `strip` block specs, launcher cross-ref, reference-impl framing.
- Amended `docs/design/mantle-ui.md` (DG-U6/U7/U8/U9, DG-U11 tags, DF-U3, desktop/mobile bottom-bar styling): chrome-slot contract with caps and overflow, plugin frame states, Settings modal + theme persistence, title scope, desktop dock dropped.
- Amended `docs/design/plugin-contract.md` (DG-T1): in-frame plugin chrome rules.
- Amended `docs/design/mockups/README.md` (RW-U4): reference-impl vs spec authority order.
- Commit `e383868` pushed to `origin/main`.

## 2026-05-21 — Stage 2: design skeleton + tickets

- Authored `10-design-00-skeleton.md` — public API/postMessage/component-package surfaces only; behavior lives in the amended design docs.
- Authored `20-tickets-dag.md` with 15-ticket Mermaid DAG (W0 parallel: T01/T02/T03/T10).
- Authored `tickets.md` with `### T-FR-0006-01..15` canonical sections including phases (TEST/DEV/VAL) and acceptance.
- Updated `tasks/ticket-progress.md` and `tasks/feature-history/TICKET-SOURCES.md`.
- **Next:** push, then author kindling FR-0001 and grocery FR-0002 tickets, then present develop-or-stop.

## 2026-05-21 — T-FR-0006-10: `@kindling/mantle` package scaffold

- Worktree: `.worktrees/FR-0006-design-language/T-FR-0006-10-mantle-package/` on `feat/FR-0006-design-language-T-FR-0006-10-mantle-package`.
- Added `packages/mantle/` (tsup ESM+CJS+dts, `src/tokens.css` per `mantle-ui.md`, stub barrels, `types.ts`, vitest exports-map tests).
- `pnpm-workspace.yaml` includes `packages/*`; `.pnpm-store/` gitignored (not committed).
- VAL: `./develop web` → `pnpm --filter @kindling/mantle test` (build + typecheck + vitest) in Docker.
- **Next:** PR into `feat/FR-0006-design-language`; unblocks T-FR-0006-11/12/14 (not T-15 publish).
