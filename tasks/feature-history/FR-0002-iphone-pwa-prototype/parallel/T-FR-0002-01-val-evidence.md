# T-FR-0002-01 — VAL evidence (local) + server-first blocker

**Ticket:** `T-FR-0002-01` — Caddy + `tls internal` + static placeholder  
**Canonical criteria:** `tasks/feature-history/FR-0002-iphone-pwa-prototype/tickets.md` (VAL row).

## VAL criteria (server-first)

On a real Mac mini **or** Raspberry Pi 4, run the Compose stack; from a desktop browser on the same LAN (or SSH port-forward if documented), open `https://hearth.home.arpa/` after trusting the exported local CA on **that** client — **no TLS warning**. Record host IP, OS, and client in `serial-diary.md` or the closeout report.

## What ran in this implementation session (local)

| Check | Result | Notes |
|-------|--------|--------|
| `scripts/test-t-fr-0002-01.sh` | PASS (2026-05-10) | Darwin host with Docker: stack up; `curl --resolve hearth.home.arpa:443:127.0.0.1 https://hearth.home.arpa/` returns HTML containing **Hearth prototype placeholder**; `http://127.0.0.1:8080/ca.crt` returns a PEM certificate. |
| DEV deliverables | Present | `deploy/compose/docker-compose.yml`, `deploy/caddy/Caddyfile.dev`, `deploy/static/index.html`, `./develop` commands `up`, `down`, `ca-export`, `deploy/compose/README.md` (hosts / mDNS note). |

No PR CI workflow ran for this ticket path in-repo at commit time; evidence is the bash script above.

## VAL blocker (automated agent)

This session **cannot** attach to operator LAN hardware or complete CA trust + desktop browser verification against a Mac mini or Pi. **VAL remains open** until an operator runs the server-first steps and updates `tasks/ticket-progress.md`.

## When VAL is genuinely complete

1. Append server-first results to `serial-diary.md` (host IP, OS, browser, TLS OK).
2. Set **VAL** = `done` for `T-FR-0002-01` in `tasks/ticket-progress.md`.
3. Add `class TFR0002_01_TEST,TFR0002_01_DEV,TFR0002_01_VAL triadDone` to `docs/design/tickets-initial.md` (mermaid block).
