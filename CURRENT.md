# CURRENT — feat/FR-0006-design-language-T-FR-0006-05-plugin-frame-state

**Branch:** `feat/FR-0006-design-language-T-FR-0006-05-plugin-frame-state`  
**Worktree:** `.worktrees/FR-0006-design-language/T-FR-0006-05-plugin-frame-state/`  
**Ticket:** T-FR-0006-05 Plugin frame state UI

## Status

TEST / DEV / VAL **done**. 38 Vitest pass (`./develop web npm run test`).

## Shipped

- `apps/hub/web/src/shell/usePluginFrameState.ts` — loading / slow (5s, Reload at 15s) / mounted / error / offline
- `apps/hub/web/src/shell/PluginFrameStates.tsx` — scrim overlays with safe-area padding
- Bridge `subscribe(..., { frame })` for per-iframe ack filtering
- `PluginFrame` wires hook + pushes `hearth.frame.state`

## Next

Merge PR into `feat/FR-0006-design-language`; continue W1 parallel tickets (04, 06, 07, …).
