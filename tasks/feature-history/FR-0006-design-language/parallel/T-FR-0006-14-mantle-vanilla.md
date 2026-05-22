# T-FR-0006-14 — @kindling/mantle vanilla bridge diary

Branch: `feat/FR-0006-design-language-T-FR-0006-14-mantle-vanilla`
Worktree: `.worktrees/FR-0006-design-language/T-FR-0006-14-mantle-vanilla/`

---

## 2026-05-21 — VAL complete

**Branch:** `feat/FR-0006-design-language-T-FR-0006-14-mantle-vanilla`

### Delivered

- `packages/mantle/src/vanilla/theme.ts` — `mantle.theme.subscribe(cb)` listens for
  `hearth.theme`, same-origin guard, applies `--hearth-*` on `:root`.
- `packages/mantle/src/vanilla/chrome.ts` — `mantle.chrome.mount({ slot, surface, payload })`
  posts mount/unmount round-trip to parent.
- `packages/mantle/src/vanilla/post.ts` — shared `postToParent` helper.
- `packages/mantle/src/types.ts` — aligned with `apps/hub/web/src/shell/types.ts`
  (T-FR-0006-03 contract).
- `packages/mantle/tsup.config.ts` — dual config: ESM/CJS library + IIFE
  `dist/vanilla/mantle.iife.js` (`globalName: mantle`).
- Export `./vanilla/mantle.iife` in `package.json`.
- Vitest jsdom: 10 vanilla tests + 3 scaffold tests (13 total).

### VAL results (host-local)

```
pnpm --filter @kindling/mantle test
  > typecheck: tsc --noEmit  ✓
  > build: tsup              ✓  (ESM + CJS + DTS + IIFE)
  > vitest run               Test Files 3 passed / Tests 13 passed
```

### Status: TEST=done DEV=done VAL=done
