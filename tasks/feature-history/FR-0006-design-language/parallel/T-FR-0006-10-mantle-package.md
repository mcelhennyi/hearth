# T-FR-0006-10 — @kindling/mantle package scaffold diary

Branch: `feat/FR-0006-design-language-T-FR-0006-10-mantle-package`
Worktree: `.worktrees/FR-0006-design-language/T-FR-0006-10-mantle-package/`

---

## 2026-05-21 — VAL complete

**Branch:** `feat/FR-0006-design-language-T-FR-0006-10-mantle-package`

### What was found on entry

Previous run had partially scaffolded the package. All source files were in
place:

- `packages/mantle/package.json` — complete except version was `0.0.0`; updated to `0.1.0`
- `packages/mantle/tsup.config.ts` — ESM + CJS + dts for three entry points
- `packages/mantle/tsconfig.json` — ES2022, Bundler resolution, strict
- `packages/mantle/vitest.config.ts` — node environment, src test glob
- `packages/mantle/src/index.ts` — barrel with type re-exports
- `packages/mantle/src/types.ts` — ChromeButton, ChromeMenu, FrameState, ThemeTokens, InboundMessage, OutboundMessage
- `packages/mantle/src/tokens.css` — dark-default palette, light via prefers-color-scheme; matches `docs/design/mantle-ui.md § Theme tokens`
- `packages/mantle/src/vanilla/index.ts` — stub (implementations land in T-FR-0006-14)
- `packages/mantle/src/package.test.ts` — 3 vitest tests: export map resolution, main re-exports types, ChromeButton type shape
- `packages/mantle/README.md` — usage, build commands, design doc links
- `packages/mantle/LICENSE` — MIT
- `pnpm-workspace.yaml` — already included `packages/*`

### Issues resolved

- `dist/` was present but missing `.d.ts` files — rollup native binary missing from
  node_modules (pnpm store corruption). Ran `pnpm install` to reinstall all 553
  packages; subsequent `pnpm --filter @kindling/mantle build` succeeded and
  generated `dist/index.js`, `dist/index.cjs`, `dist/index.d.ts`, `dist/types.*`,
  `dist/vanilla/index.*`.

### VAL results (host-local — no Docker path for this package build)

```
pnpm --filter @kindling/mantle test
  > typecheck: tsc --noEmit  ✓
  > build: tsup              ✓  (ESM + CJS + DTS, 3 entry points)
  > vitest run               Test Files 1 passed / Tests 3 passed
```

Token file `src/tokens.css` contains all required tokens matching
`docs/design/mantle-ui.md § Theme tokens`:
- `--hearth-bg`, `--hearth-surface`, `--hearth-fg`, `--hearth-muted`
- `--hearth-accent`, `--hearth-accent-fg`, `--hearth-error`
- `--hearth-radius-sm/md/lg`, `--hearth-font-sans`
- `--hearth-safe-top`, `--hearth-safe-bottom`

### Note on token naming

The task spec listed `--hearth-color-bg` style aliases, but `docs/design/mantle-ui.md`
(the source of truth) specifies `--hearth-bg`, `--hearth-fg`, etc. without a
`-color-` infix. The implementation follows the design doc. No DESIGN-GAP raised
as the doc is unambiguous.

### Status: TEST=done DEV=done VAL=done
