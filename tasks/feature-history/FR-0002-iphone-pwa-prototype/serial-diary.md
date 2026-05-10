# FR-0002 — serial diary

Append-only. Newest entries at the top.

---

## 2026-05-10 — T-FR-0002-02 Mantle PWA bones complete

- **TEST:** Vitest (`App.test.tsx`, `pwa.test.ts`); Playwright + Lighthouse **11.x** PWA category ≥90 (`e2e/lighthouse-pwa.spec.ts`). Lighthouse 12+ dropped the dedicated PWA category — dependency pinned accordingly until CI moves to successor metrics.
- **DEV:** `apps/hub/web` Mantle shell; production build → `apps/hub/web/dist/`; Compose mounts `dist` at `/srv` for HTTPS + HTTP-quick Caddy profiles (`deploy/compose/docker-compose.yml`). Vite-PWA uses `injectManifest` so the committed `src/sw.ts` is the generated `/sw.js`.
- **VAL (server-first):** Build hub web, `./develop up -d`, trust local CA on desktop client, open `https://hearth.home.arpa/` — manifest loads, SW registers, shell matches mobile bottom tabs vs desktop top bar in responsive preview. Pi/Mac mini LAN proof follows `HOWTO-complete-FR-0002.md` when hardware run is staffed.
- **Host-local exception:** No Node Docker/Compose wrapper exists yet for `apps/hub/web`; `npm test`, `npm run lint`, `npm run build`, and `npm run test:e2e` were run host-local. Playwright Chromium was installed into a worktree-local cache for the Lighthouse gate. `./develop up-quick -d` served the built bundle via Caddy after Docker socket access was granted for validation.

## 2026-04-30 — Server-first VAL; iPhone deferred

- **Decision:** Ticket **VAL** and FR-0002 **close** prioritize proving the stack on **Mac mini / Pi** with **desktop browsers** (same LAN, CA trusted on that client). **iPhone** (CA UX, Add to Home Screen, on-device push) is a **non-blocking side goal**, tracked in `40-prototype-report.md` under **Follow-up: iPhone** when run.
- **Canonical text:** `tickets.md` VAL rows, feature `README.md` acceptance, `10-design/charter.md` "What succeed means".

## 2026-04-27 — `design` → `in-progress`

- Allocated **`FR-0002`** in `REGISTRY.md`; `next_id` → `3`.
- FR-0001 moved to `parked` pending FR-0002 prototype findings; FR-0001 design docs remain authoritative.
- Wrote charter, risks register (R1–R5), DAG, and concise tickets `T-FR-0002-01..04`. Each ticket is intentionally a vertical slice and an explicit reuse target for an FR-0001 ticket.
- Branch / worktree: none yet — next worker creates `feat/FR-0002-iphone-pwa-prototype` at `.worktrees/FR-0002-iphone-pwa-prototype/feature/`.
- Continue handoff at [`handoffs/2026-04-27-continue.md`](handoffs/2026-04-27-continue.md).
