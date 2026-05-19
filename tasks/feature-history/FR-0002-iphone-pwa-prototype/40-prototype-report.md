# FR-0002 prototype report

Status: **closeout** (`T-FR-0002-04`, 2026-05-19)

## Scope

This report closes FR-0002 by documenting acceptance results for:

- local TLS + iPhone trust flow
- standalone PWA launch behavior
- service worker persistence
- web push round-trip

## Preflight (completed in containerized environment)

- [x] `./develop vapid-gen`
- [x] `./develop api pytest`
- [x] `./develop web npm run test`
- [x] `./develop up -d`
- [x] `curl -sk --resolve hearth.home.arpa:443:127.0.0.1 https://hearth.home.arpa/api/health`
- [x] `curl -sk --resolve hearth.home.arpa:443:127.0.0.1 -X POST https://hearth.home.arpa/api/push/test`
- [x] `./develop down`

## Acceptance runbook evidence (real iPhone)

### Environment A (Mac mini host)

- Host details: not run for this closeout (Pi-first validation).
- iPhone model + iOS version: n/a
- Recording path: n/a

Checklist:

- [ ] `./develop up` successful
- [ ] Safari opens `https://hearth.home.arpa/` without cert error after trust flow
- [ ] Add to Home Screen completed
- [ ] Home-screen launch is standalone with expected status bar tint/safe areas
- [ ] Notification permission granted
- [ ] "Send test notification" arrives in <= 30s
- [ ] Tap notification returns into PWA
- [ ] Force-quit + relaunch still renders shell

Artifacts: deferred — see Environment B.

### Environment B (Pi 4 host — `hearth-server`)

- Host details: Raspberry Pi 4 (`pi@hearth-server`), Docker-profile install under `~/hearth` + `HEARTH_DEPLOY`, branch `feat/FR-0002-iphone-pwa-prototype` @ `cf35e3e+`.
- iPhone: same LAN as Pi; `hearth.home.arpa` resolves to Pi LAN IP.
- Recording path: operator-validated 2026-05-19 (no video archived in-repo).

Checklist:

- [x] Stack up (`./develop up -d` / install compose)
- [x] Safari opens `https://hearth.home.arpa/` without cert error after trust flow (required **Certificate Trust Settings** full-trust toggle — see R2)
- [x] Web Push: **Send test notification** — push arrived on iPhone
- [ ] Add to Home Screen — not recorded in diary (follow-up)
- [ ] Home-screen standalone launch — not recorded (follow-up)
- [ ] Tap notification returns into PWA — not recorded (follow-up)
- [ ] Force-quit + relaunch — not recorded (follow-up)

Artifacts:

- Operator notes: TLS failed until Settings → General → About → **Certificate Trust Settings** enabled full trust for the Caddy local root CA (profile install alone is insufficient).
- Push delivery confirmed on device after permission grant.

## Follow-up: iPhone (optional hardening)

Remaining Home Screen / standalone / relaunch checks can be captured in a short screen recording and linked here without blocking FR-0002 server-first close.

## Risk verdicts (R1-R5)

### R1 — Caddy `tls internal` cert trust on iOS

- Outcome: **pass**
- Evidence: Safari loads `https://hearth.home.arpa/` without warning after profile install + Certificate Trust Settings enable (Pi / iPhone, 2026-05-19).
- Amendment landed: deployment.md iPhone trust workflow — explicit LAN `http://<host>:8080/ca.crt` URL and Certificate Trust Settings step (this PR).

### R2 — iPhone CA-trust UX effort

- Outcome: **pass-with-caveat**
- Evidence: Two-step flow (profile + Certificate Trust Settings) is easy to miss; operator hit "connection is not private" until step 2. No timed multi-user study.
- Amendment landed: `SETUP.md` + `hearth ca-export` on-screen instructions; deployment.md diagram updated (this PR).

### R3 — Standalone launch behavior

- Outcome: **deferred**
- Evidence: not exercised on iPhone during Pi closeout session.
- Amendment landed: none

### R4 — Service worker install/persistence

- Outcome: **pass-with-caveat**
- Evidence: push subscription + delivery implies SW registered; force-quit/relaunch not re-tested on device.
- Amendment landed: none

### R5 — Web Push delivery latency/reliability

- Outcome: **pass**
- Evidence: test push arrived on iPhone after **Send test notification** (Pi stack, 2026-05-19).
- Amendment landed: none

## FR-0001 impact summary

- Docs updated from FR-0002 findings:
  - `docs/design/deployment.md`: iPhone trust workflow clarifies `hearth ca-export`, LAN IP download URL, Certificate Trust Settings (this PR).
  - `docs/design/mantle-ui.md`: no amendment required for prototype scope.
  - `docs/design/notifications.md`: no amendment required; Web Push path validated.
- FR-0002 reuses into `T-FR-0001-04`, `T-FR-0001-05`, `T-FR-0001-09` per `tickets.md`.

## Closeout status

- `T-FR-0002-04 TEST`: done
- `T-FR-0002-04 DEV`: done
- `T-FR-0002-04 VAL`: done (Pi + iPhone TLS/push; optional Home Screen items deferred)
