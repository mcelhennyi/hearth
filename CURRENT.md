# CURRENT — T-FR-0006-13 mantle overlays

**Branch:** `feat/FR-0006-design-language-T-FR-0006-13-mantle-overlays`  
**Worktree:** `.worktrees/FR-0006-design-language/T-FR-0006-13-mantle-overlays/`

## Phase: VAL (complete)

- **TEST:** `overlays.test.tsx` — Sheet/Dialog postMessage open/close; Toast no-throw + console stub.
- **DEV:** `<Sheet>`, `<Dialog>`, `<Toast>`; `hearth.sheet` / `hearth.dialog` outbound types; in-iframe `OverlayFallback`.
- **VAL:** Host `pnpm test` in worktree — **36** Vitest passed. Docker `./develop web` path lacks worktree mount (blocker for CI-parity VAL in this worktree).

## Next

Open PR → `feat/FR-0006-design-language`; parent merges W2 batch with 08/09 when all VAL-done.
