# T-FR-0006-11 — @kindling/mantle base components diary

Branch: `feat/FR-0006-design-language-T-FR-0006-11-mantle-components`  
Worktree: `.worktrees/FR-0006-design-language/T-FR-0006-11-mantle-components/`

---

## 2026-05-21 — VAL complete

### Surface

Implemented layout and form primitives per `docs/design/mantle-ui.md` § Component primitives:

- Page (safe-area padding), PageHeader, Card, Section, List, EmptyState
- Button (default/accent/ghost/danger), IconButton, Input, TextArea, Select, Switch
- `components.css` using `--hearth-*` tokens; `./components.css` export added

### Tests

- `src/components/components.test.tsx` — render, variants, 44px min touch targets, axe (no violations)
- `src/package.test.ts` — export map + built `Page`/`Button`/`Switch` from dist

### VAL (Docker)

```
./develop web sh -c "cd /workspace && corepack enable && corepack prepare pnpm@9.15.0 --activate && pnpm --filter @kindling/mantle test"
```

- typecheck ✓
- tsup build ✓ (ESM ~8.7 KB index.js with components)
- vitest: **14 passed**

### Build note

tsup elides runtime when the entry is type-only re-exports; fixed by per-component `export { X } from "./components/X"` in `src/index.ts` and `platform: "browser"` + `jsx: "automatic"`.

### Status: TEST=done DEV=done VAL=done
