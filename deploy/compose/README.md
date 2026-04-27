# FR-0002 Caddy dev stack

This ticket's stack serves a static placeholder over local HTTPS at `https://hearth.local/` using Caddy `tls internal`.

## Hostname setup

Use one of these options so `hearth.local` resolves to your host machine:

- **mDNS** if your LAN setup already resolves `.local` hostnames to your machine, or
- **`/etc/hosts`** entry on each client (including your iPhone test machine), for example:

```text
192.168.1.50 hearth.local
```

## Commands

From repo root:

- `./develop up -d` - start Caddy in the background
- `./develop down` - stop the stack
- `./develop ca-export` - temporarily serve `http://<host>:8080/ca.crt` (10-minute max) for iPhone trust setup

For local Mac validation without hostname changes, use:

```bash
curl -k --resolve hearth.local:443:127.0.0.1 https://hearth.local/
```
