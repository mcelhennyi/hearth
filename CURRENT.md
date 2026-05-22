# Current branch state

**Branch:** `feat/FR-0006-design-language-T-FR-0006-10-mantle-package`
**Ticket:** T-FR-0006-10 — `@kindling/mantle` package scaffold
**Status:** TEST/DEV/VAL complete — PR open for merge into `feat/FR-0006-design-language`

## What was done

- **TEST:** `packages/mantle` vitest (`package.test.ts`) — exports map + tokens CSS + dist artifacts; `tsc --noEmit` in test script.
- **DEV:** `packages/mantle/` — `package.json` (`@kindling/mantle`, public, sideEffects CSS), tsup ESM+CJS+dts, `src/tokens.css` per `docs/design/mantle-ui.md`, stub barrels + `types.ts`, README, LICENSE; `pnpm-workspace.yaml` includes `packages/*`; `.pnpm-store/` gitignored.
- **VAL:** `pnpm --filter @kindling/mantle build` (+ test) via `./develop web` in Docker.

## Next step

Merge this PR into `feat/FR-0006-design-language`. Unblocks **T-FR-0006-11** (base components), **T-FR-0006-12** (hooks), **T-FR-0006-14** (vanilla). **T-FR-0006-15** (npm publish) remains out of scope until tickets 10–14 are VAL-done.
