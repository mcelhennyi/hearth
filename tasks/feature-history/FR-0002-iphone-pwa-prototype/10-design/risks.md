# FR-0002 — risks under test

Each row names a risk we believe is the biggest threat to FR-0001's "feels native on iPhone" claim, an explicit **fail trigger** so we know when the prototype has refuted the assumption, and the **amendment we'd write** if it does.

**Server-first close (2026-04-30):** For **R1–R4**, record **`deferred`** in `40-prototype-report.md` with a one-line reason if **Follow-up: iPhone** was not run yet — that is **not** a failed prototype. **R5** may be marked **`pass`** on evidence of timely push to a **desktop Chromium** subscriber against the deployed Pi/Mac mini stack; mark **`pass-with-caveat`** ("APNs / iOS path not yet exercised") until the iPhone side goal runs.

| ID | Risk | Fail trigger | Amendment if it fails |
|----|------|--------------|------------------------|
| R1 | Caddy `tls internal` certs aren't trusted by iOS Safari even after profile install. | After three independent attempts at the documented CA-trust flow, Safari still shows "Not Secure" or refuses to register the service worker. | DESIGN-FLAW vs `deployment.md` § iPhone trust workflow → switch default cert source to Tailscale-issued certs (or `mkcert` + USB-side-loaded profile). Document constraints. |
| R2 | iPhone CA-trust UX is too long for a home-user. | Median walkthrough time on three first-time users (or three runs by Ian, dispassionately) > 8 minutes; or any step requires Settings searches that aren't in the dashboard tile copy. | DESIGN-FLAW vs `mantle-ui.md` § install prompt → expand the dashboard "Add a device" tile into a guided flow with screenshots. Possibly add an `--easy-mode` flag to `./develop ca-export` that opens a QR code linking to the profile. |
| R3 | `display: standalone` doesn't fully hide Safari chrome (status bar, top URL ghost). | After Add to Home Screen, any Safari chrome is visible at launch on iOS 17+. | Likely meta-tag amendment vs `mantle-ui.md` § PWA wiring; possible `apple-mobile-web-app-status-bar-style` change or `viewport-fit=cover` interaction with safe-area CSS. |
| R4 | Service worker fails to install / persist on the iPhone PWA, breaking offline + push. | After install, force-quit, and relaunch, the SW is not active or `pushManager.subscribe` fails. | DESIGN-FLAW vs `mantle-ui.md` § PWA wiring + service worker scope. Could mean cookie/session leakage between scope `/` and `/api/`, or a Vite-PWA config bug. |
| R5 | Web Push from a home box fails — VAPID delivery to Apple's endpoint is rejected, blocked by NAT, or arrives with multi-minute latency. | A test push does not appear within 30 s of `POST /api/push/test` in three of three runs, or repeatedly comes back as `410 Gone` / `400 Bad Request` from the endpoint. | DESIGN-FLAW vs `notifications.md` § Web Push pre-reqs. Could mean VAPID claim contents (audience, exp), payload encoding, or that ISP firewall behaviour requires routing pushes through Ember (turning Phase 2 into a hard MVP dep). |

## Risk-amenable findings register

When the prototype finishes, paste each risk's outcome into `40-prototype-report.md`:

```markdown
## R1 — Caddy `tls internal` cert trust on iOS
- Outcome: pass | fail | pass-with-caveat
- Evidence: <links to screenshots / commits / commands>
- Amendment landed: <commit / "none">
```

The closeout commit links the report from `serial-diary.md` and from the FR-0001 docs amended (if any).
