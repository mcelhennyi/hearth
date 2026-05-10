## Current Branch

- Ticket: `T-FR-0002-02`
- Branch: `feat/FR-0002-iphone-pwa-prototype-T-FR-0002-02-mantle-bones`
- Worktree: `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones/`
- Status: `complete`

## TEST

- Vitest: 768px layout switch (`src/App.test.tsx`), service worker registration (`src/pwa.test.ts`).
- E2E: Playwright starts `vite preview`; Lighthouse PWA category ≥ 90 via headless Chromium from Playwright (`e2e/lighthouse-pwa.spec.ts`).
- CI: `.github/workflows/hub-web-ci.yml` runs unit tests, build, then Playwright + Lighthouse.
- Current pass: reran host-local npm validation because this branch has no Node Docker/Compose wrapper.
- Result: `TMPDIR=.tmp npm test` passed (3 tests).

## DEV

- `apps/hub/web`: Vite + TypeScript + Tailwind + Vite-PWA, manifest + `src/sw.ts`, Apple meta + `viewport-fit=cover`, four placeholder tab routes, theme tokens from `docs/design/mantle-ui.md`.
- Icons: `docs/design/logo.svg` at `/logo.svg`; maskable PNGs under `public/icons/` for installability audits.
- Production build output: `npm run build` writes to `apps/hub/web/dist/`; `deploy/compose` Caddy mounts that directory at `/srv` over HTTPS.
- Result: `npm run lint` passed; `npm run build` passed after switching Vite-PWA to `injectManifest` for the committed `src/sw.ts`.

## VAL

- Host-local: `npm test`, `npm run lint`, `npm run build`, and `npm run test:e2e` in `apps/hub/web` passed. Playwright browser install used a worktree-local cache as a validation-only exception.
- Caddy/Compose: `./develop up-quick -d` served the built bundle from `apps/hub/web/dist` via Caddy (`Caddy HTTP smoke PASS`); TLS hardware acceptance remains in the FR-0002 closeout path.
