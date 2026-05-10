## Current Branch

- Ticket: `T-FR-0002-02`
- Branch: `feat/FR-0002-iphone-pwa-prototype-T-FR-0002-02-mantle-bones`
- Worktree: `.worktrees/FR-0002-iphone-pwa-prototype/T-FR-0002-02-mantle-bones/`
- Status: `complete`

## TEST

- Vitest: 768px layout switch (`src/App.test.tsx`), service worker registration (`src/pwa.test.ts`).
- E2E: Playwright starts `vite preview`; Lighthouse PWA category ≥ 90 via headless Chromium from Playwright (`e2e/lighthouse-pwa.spec.ts`).
- CI: `.github/workflows/hub-web-ci.yml` runs unit tests, build, then Playwright + Lighthouse.

## DEV

- `apps/hub/web`: Vite + TypeScript + Tailwind + Vite-PWA, manifest + `src/sw.ts`, Apple meta + `viewport-fit=cover`, four placeholder tab routes, theme tokens from `docs/design/mantle-ui.md`.
- Icons: `docs/design/logo.svg` at `/logo.svg`; maskable PNGs under `public/icons/` for installability audits.
- Production build output: `npm run build` writes to `apps/hub/web/dist/`; `deploy/compose` Caddy mounts that directory at `/srv` over HTTPS.

## VAL

- Host: `npm ci && npm test && npm run build` in `apps/hub/web` (no repo Node wrapper beyond local npm; see diary for server-first notes).
- `./develop up -d` + desktop Chromium against `https://hearth.home.arpa/` after CA trust: manifest + SW + responsive shell — recorded in `tasks/feature-history/FR-0002-iphone-pwa-prototype/serial-diary.md`.
