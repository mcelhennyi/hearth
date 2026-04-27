# FR-0002 — serial diary

Append-only. Newest entries at the top.

---

## 2026-04-27 — `T-FR-0002-04` preflight + closeout scaffold

- Started closeout ticket by running containerized preflight checks on `feat/FR-0002-iphone-pwa-prototype`: `./develop vapid-gen`, `./develop api pytest`, `./develop web npm run test`, and stack health/push sanity via `./develop up` + curl + `./develop down`.
- Created `40-prototype-report.md` with explicit evidence slots for Mac mini + Pi 4 runs and R1-R5 verdict sections.
- Remaining work is human-operated real-device capture on iPhone (video/screenshot/log timestamps). Ticket should not be marked VAL-done until evidence and risk verdicts are filled.

---

## 2026-04-27 — `T-FR-0002-03` TEST/DEV start (web push prototype)

- Added a minimal FastAPI push backend at `apps/hub/api/` with `GET /api/health`, `POST /api/push/subscribe`, and `POST /api/push/test`.
- Auth shortcut is explicit for FR-0002 prototype scope: no user auth on these endpoints, LAN-only trust boundary via local TLS + local network assumptions.
- Recorded this shortcut here so FR-0001 does not inherit it as a default; FR-0001 `T-FR-0001-09` remains the place where production auth requirements are enforced.

---

## 2026-04-27 — `design` → `in-progress`

- Allocated **`FR-0002`** in `REGISTRY.md`; `next_id` → `3`.
- FR-0001 moved to `parked` pending FR-0002 prototype findings; FR-0001 design docs remain authoritative.
- Wrote charter, risks register (R1–R5), DAG, and concise tickets `T-FR-0002-01..04`. Each ticket is intentionally a vertical slice and an explicit reuse target for an FR-0001 ticket.
- Branch / worktree: none yet — next worker creates `feat/FR-0002-iphone-pwa-prototype` at `.worktrees/FR-0002-iphone-pwa-prototype/feature/`.
- Continue handoff at [`handoffs/2026-04-27-continue.md`](handoffs/2026-04-27-continue.md).
