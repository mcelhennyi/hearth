# FR-0002 Caddy dev stack

This ticket's stack serves a static placeholder over local HTTPS at `https://hearth.home.arpa/` using Caddy `tls internal` (per `tasks/feature-history/FR-0002-iphone-pwa-prototype/tickets.md` → **T-FR-0002-01**).

## Hostname setup

Use local DNS so `hearth.home.arpa` resolves to the machine running Docker:

- **Pi-hole / router DNS** A record (recommended on a homelab), or
- **mDNS** only if your environment resolves this name (uncommon for `.arpa`), or
- **`/etc/hosts`** on each client, for example:

```text
192.168.1.50 hearth.home.arpa
```

## Commands

From repo root:

- `./develop up -d` — start Caddy with TLS on `:443`
- `./develop down` — stop Compose services for this compose file
- `./develop ca-export` — temporarily serve `http://<host>:8080/ca.crt` (10-minute max) for device CA trust
- `./develop up-quick` — HTTP-only static server on `:5080` (no TLS; fast iteration)
- `./develop docs` — MkDocs in Docker (see `./develop help`)

For local validation without changing system DNS, use:

```bash
curl -k --resolve hearth.home.arpa:443:127.0.0.1 https://hearth.home.arpa/
```
