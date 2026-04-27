# FR-0002 Caddy dev stack

This ticket's stack serves a static placeholder over local HTTPS at `https://hearth.home.arpa/` using Caddy `tls internal`.
It serves static files and proxies `/api/*` to the FastAPI hub service.

## Hostname setup

Use local DNS so `hearth.home.arpa` resolves to your host machine:

- **Pi-hole / router DNS** record (recommended), or
- **`/etc/hosts`** entry on each client (including your iPhone test machine), for example:

```text
192.168.1.50 hearth.home.arpa
```

## Commands

From repo root:

- `./develop up -d` - start Caddy in the background
- `./develop down` - stop the stack
- `./develop ca-export` - temporarily serve `http://<host>:8080/ca.crt` (10-minute max) for iPhone trust setup
- `./develop vapid-gen` - generate `var/hearth/secrets/vapid.{pub,priv}` for Web Push
- `./develop api pytest` - run API tests in container
- `./develop web npm run test` - run web tests in container

For local Mac validation without hostname changes, use:

```bash
curl -k --resolve hearth.home.arpa:443:127.0.0.1 https://hearth.home.arpa/
```
