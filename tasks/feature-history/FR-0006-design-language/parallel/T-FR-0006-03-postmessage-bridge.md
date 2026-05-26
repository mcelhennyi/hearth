# T-FR-0006-03 — Mantle postMessage bridge (parallel diary)

**Branch:** `feat/FR-0006-design-language-T-FR-0006-03-postmessage-bridge`  
**Worktree:** `.worktrees/FR-0006-design-language/T-FR-0006-03-postmessage-bridge/`

## 2026-05-21 — VAL (agent revalidation)

- **Revalidation run (host-local, documented exception):** `npx vitest run` — 5 files, 24 tests, all pass. Note: Docker test path failed due to missing `@rollup/rollup-darwin-arm64` in the worktree's npm install; resolved by running `npm install` in `apps/hub/web` first. Host-local test run is the documented exception.
- **Status:** TEST/DEV/VAL all `done`. PR to be opened to `feat/FR-0006-design-language`.

## 2026-05-21 — VAL

- **TEST/DEV/VAL:** `apps/hub/web/src/shell/{types,usePostMessageBridge,inboundDefaults}.ts` + Vitest (`usePostMessageBridge.test.tsx`); `App.tsx` wires `hearth.title` → `document.title`; `PluginFrame.tsx` placeholder removed.
- **Tests:** `./develop web npm run test -- --run` — 5 files, 22 tests, all pass (Docker).
- **Manual smoke (VAL):** With hub dev up and an enabled app plugin iframe, open DevTools console on the shell page and run:
  ```js
  const f = document.querySelector('iframe');
  f?.contentWindow?.postMessage({ type: 'hearth.title', title: 'Smoke' }, location.origin);
  ```
  Expect tab title `Smoke — Hearth` and `[hearth.toast]` log if the plugin (or the snippet) also sends `{ type: 'hearth.toast', level: 'info', message: 'ok' }`.
