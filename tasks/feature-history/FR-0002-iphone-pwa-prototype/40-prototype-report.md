# FR-0002 prototype report

Status: in progress (`T-FR-0002-04`)

## Scope

This report closes FR-0002 by documenting real-device acceptance results for:

- local TLS + iPhone trust flow
- standalone PWA launch behavior
- service worker persistence
- web push round-trip

## Preflight (completed in containerized environment)

- [x] `./develop vapid-gen`
- [x] `./develop api pytest`
- [x] `./develop web npm run test`
- [x] `./develop up -d`
- [x] `curl -sk --resolve hearth.local:443:127.0.0.1 https://hearth.local/api/health`
- [x] `curl -sk --resolve hearth.local:443:127.0.0.1 -X POST https://hearth.local/api/push/test`
- [x] `./develop down`

## Acceptance runbook evidence (real iPhone)

### Environment A (Mac mini host)

- Host details: TODO
- iPhone model + iOS version: TODO
- Recording path: TODO

Checklist:

- [ ] `./develop up` successful
- [ ] Safari opens `https://hearth.local/` without cert error after trust flow
- [ ] Add to Home Screen completed
- [ ] Home-screen launch is standalone with expected status bar tint/safe areas
- [ ] Notification permission granted
- [ ] "Send test notification" arrives in <= 30s
- [ ] Tap notification returns into PWA
- [ ] Force-quit + relaunch still renders shell

Artifacts:

- Screenshot/video refs: TODO
- Relevant logs and timestamps: TODO

### Environment B (Pi 4 host)

- Host details: TODO
- iPhone model + iOS version: TODO
- Recording path: TODO

Checklist:

- [ ] `./develop up` successful
- [ ] Safari opens `https://hearth.local/` without cert error after trust flow
- [ ] Add to Home Screen completed
- [ ] Home-screen launch is standalone with expected status bar tint/safe areas
- [ ] Notification permission granted
- [ ] "Send test notification" arrives in <= 30s
- [ ] Tap notification returns into PWA
- [ ] Force-quit + relaunch still renders shell

Artifacts:

- Screenshot/video refs: TODO
- Relevant logs and timestamps: TODO

## Risk verdicts (R1-R5)

### R1 — Caddy `tls internal` cert trust on iOS

- Outcome: TODO (`pass` | `fail` | `pass-with-caveat`)
- Evidence: TODO
- Amendment landed: TODO (`none` or commit link)

### R2 — iPhone CA-trust UX effort

- Outcome: TODO (`pass` | `fail` | `pass-with-caveat`)
- Evidence: TODO
- Amendment landed: TODO (`none` or commit link)

### R3 — Standalone launch behavior

- Outcome: TODO (`pass` | `fail` | `pass-with-caveat`)
- Evidence: TODO
- Amendment landed: TODO (`none` or commit link)

### R4 — Service worker install/persistence

- Outcome: TODO (`pass` | `fail` | `pass-with-caveat`)
- Evidence: TODO
- Amendment landed: TODO (`none` or commit link)

### R5 — Web Push delivery latency/reliability

- Outcome: TODO (`pass` | `fail` | `pass-with-caveat`)
- Evidence: TODO
- Amendment landed: TODO (`none` or commit link)

## FR-0001 impact summary

- Docs updated from FR-0002 findings:
  - `docs/design/deployment.md`: TODO
  - `docs/design/mantle-ui.md`: TODO
  - `docs/design/notifications.md`: TODO
- If no amendments were required, note why: TODO

## Closeout status

- `T-FR-0002-04 TEST`: in progress (awaiting real-device evidence)
- `T-FR-0002-04 DEV`: pending
- `T-FR-0002-04 VAL`: pending
