# CURRENT — T-FR-0006-09 edit mode

**Branch:** `feat/FR-0006-design-language-T-FR-0006-09-edit-mode`  
**Worktree:** `.worktrees/FR-0006-design-language/T-FR-0006-09-edit-mode/`

## Phase: VAL (complete)

- **TEST:** 6 Vitest in `apps/hub/web/src/dashboard/edit/edit.test.tsx` (long-press, Edit button, collisions, reduced-motion, PUT Done, no PUT Cancel).
- **DEV:** `apps/hub/web/src/dashboard/edit/` — EditModeProvider, EditGrid, EditChrome, BlockPicker, collisions + layout draft helpers; wired in `DashboardView` + `App.tsx`; `--hearth-error` token.
- **VAL:** `npx vitest run src/dashboard` — 12 passed (4 files). API unchanged (no `./develop test`).

## Handoff

PR → `feat/FR-0006-design-language`. Parent merges ticket branch.
