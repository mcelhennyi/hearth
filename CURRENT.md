# CURRENT — T-FR-0006-12 mantle hooks

**Branch:** `feat/FR-0006-design-language-T-FR-0006-12-mantle-hooks`  
**Worktree:** `.worktrees/FR-0006-design-language/T-FR-0006-12-mantle-hooks/`  
**Ticket:** T-FR-0006-12 — `@kindling/mantle` hooks

## Triad

| Phase | Status |
|-------|--------|
| TEST | done |
| DEV | done |
| VAL | done |

## Delivered

- `packages/mantle/src/types.ts` — plugin-centric postMessage types aligned with `apps/hub/web/src/shell/types.ts`
- `packages/mantle/src/bridge.ts` — `createPluginBridge()` (origin guard, subscribe, post to parent)
- Hooks: `useMantle`, `useTheme`, `useUser`, `useChromeSlot`, `useHaptics`, `useNotifications`, `useSpark` (stub)
- `MantleProvider` + Vitest coverage (15 tests)

## Next step

Merge PR into `feat/FR-0006-design-language`; continue W1 frontier (04, 05, 06, 07, 11, 14).
