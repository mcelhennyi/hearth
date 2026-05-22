# CURRENT — T-FR-0006-03 postMessage bridge

**Branch:** `feat/FR-0006-design-language-T-FR-0006-03-postmessage-bridge`  
**Ticket:** T-FR-0006-03 · **FR-0006** design-language  
**PR base:** `feat/FR-0006-design-language`

## Status

TEST / DEV / VAL **done** on this branch. Ready to merge into `feat/FR-0006-design-language`.

## Delivered

- `apps/hub/web/src/shell/usePostMessageBridge.ts` — same-origin guard, typed subscribe bus, `pushToPlugin` / `broadcastToAllPlugins`
- `apps/hub/web/src/shell/types.ts` — inbound/outbound protocol types
- `apps/hub/web/src/shell/inboundDefaults.ts` — toast console stub, haptic vibrate when available
- `App.tsx` — bridge + `hearth.title` → `document.title`
- `PluginFrame.tsx` — postMessage ownership comment only (no duplicate listener)

## Next

- Merge ticket branch → `feat/FR-0006-design-language`
- W1 tickets (04/05/06/12/14) subscribe to the bridge for theme, chrome, frame state
