# FR-0002 — serial diary

Append-only. Newest entries at the top.

---

## 2026-05-10 — T-FR-0002-01 local smoke; VAL pending hardware

- **Local:** `scripts/test-t-fr-0002-01.sh` PASS (Docker on development host); placeholder HTML and CA export URL asserted.
- **VAL:** Not marked done — server-first proof on **Mac mini or Pi** + desktop browser with trusted CA still required per `tickets.md`. Recorded in `parallel/T-FR-0002-01-val-evidence.md`.
- **Design:** Removed premature `triadDone` styling for `TFR0002_01_*` from `docs/design/tickets-initial.md` until VAL is complete on hardware.

---

## 2026-04-30 — Server-first VAL; iPhone deferred

- **Decision:** Ticket **VAL** and FR-0002 **close** prioritize proving the stack on **Mac mini / Pi** with **desktop browsers** (same LAN, CA trusted on that client). **iPhone** (CA UX, Add to Home Screen, on-device push) is a **non-blocking side goal**, tracked in `40-prototype-report.md` under **Follow-up: iPhone** when run.
- **Canonical text:** `tickets.md` VAL rows, feature `README.md` acceptance, `10-design/charter.md` "What succeed means".

## 2026-04-27 — `design` → `in-progress`

- Allocated **`FR-0002`** in `REGISTRY.md`; `next_id` → `3`.
- FR-0001 moved to `parked` pending FR-0002 prototype findings; FR-0001 design docs remain authoritative.
- Wrote charter, risks register (R1–R5), DAG, and concise tickets `T-FR-0002-01..04`. Each ticket is intentionally a vertical slice and an explicit reuse target for an FR-0001 ticket.
- Branch / worktree: none yet — next worker creates `feat/FR-0002-iphone-pwa-prototype` at `.worktrees/FR-0002-iphone-pwa-prototype/feature/`.
- Continue handoff at [`handoffs/2026-04-27-continue.md`](handoffs/2026-04-27-continue.md).
