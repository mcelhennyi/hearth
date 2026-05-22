# CURRENT — T-FR-0006-11 mantle base components

**Branch:** `feat/FR-0006-design-language-T-FR-0006-11-mantle-components`  
**Worktree:** `.worktrees/FR-0006-design-language/T-FR-0006-11-mantle-components/`  
**Ticket:** T-FR-0006-11 — @kindling/mantle base components

## Phase status

| Phase | Status |
|-------|--------|
| TEST | done |
| DEV | done |
| VAL | done |

## Delivered

- `packages/mantle/src/components/*` — Page, PageHeader, Card, Section, List, EmptyState, Button, IconButton, Input, TextArea, Select, Switch
- `packages/mantle/src/components.css` — token-driven styles, 44px touch targets, focus rings
- Vitest + Testing Library + vitest-axe (14 tests, all pass in Docker)

## VAL

```bash
./develop web sh -c "cd /workspace && corepack enable && corepack prepare pnpm@9.15.0 --activate && pnpm --filter @kindling/mantle test"
```

## Next

Open PR → `feat/FR-0006-design-language`; merge; continue W1 (12 hooks, 14 vanilla, shell tickets).
