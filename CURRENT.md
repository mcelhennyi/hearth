# CURRENT — T-FR-0006-06 chrome slots

**Branch:** `feat/FR-0006-design-language-T-FR-0006-06-chrome-slots`  
**Ticket:** T-FR-0006-06 · **FR-0006** design-language  
**PR base:** `feat/FR-0006-design-language`

## Status

TEST / DEV / VAL **done** on this branch. Ready to merge into `feat/FR-0006-design-language`.

## Delivered

- `apps/hub/web/src/shell/useChromeSlotRegistry.ts` — mount/update/unmount via bridge; ≤8 cap; route-change clear
- `apps/hub/web/src/shell/ChromeSlot.tsx` — ChromeButton/ChromeMenu + overflow (top=3, bottom=4)
- `apps/hub/web/src/shell/chrome.css` — mock-aligned slot layout
- `App.tsx` — `.chrome-slot--top`, `.plugin-bottom-slots`, `.has-chrome-slots`, app-mode chrome bars
- `PluginFrame.tsx` — `data-plugin-slug` for invoke/error targeting
- Vitest: 11 new tests (registry, ChromeSlot, App route-change); **35** total web tests pass (host `npm run test`)

## Next

- Merge ticket branch → `feat/FR-0006-design-language`
- W1 peers: T-FR-0006-05 frame state, T-FR-0006-07 dashboard grid
