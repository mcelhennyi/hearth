# FR-0002 Caddy dev stack

This stack serves the **built** Mantle hub UI (see **Mantle static bundle** below) over local HTTPS at `https://hearth.home.arpa/` using Caddy `tls internal`.

## Hostname setup

Use local DNS so `hearth.home.arpa` resolves to your host machine:

- **Pi-hole / router DNS** record (recommended), or
- **`/etc/hosts`** entry on each client (including your iPhone test machine), for example:

```text
192.168.1.50 hearth.home.arpa
```

## Mantle static bundle (`T-FR-0002-02`)

Caddy serves the **built** hub UI from `apps/hub/web/dist/`. Before `./develop up`, build the Vite app once (or after UI changes):

```bash
(cd apps/hub/web && npm ci && npm run build)
```

This writes `index.html`, `sw.js`, `manifest.webmanifest`, and hashed assets into `apps/hub/web/dist/`, which is bind-mounted to `/srv` in the `caddy` and `caddy-http` services.

## Commands

From repo root:

- `./develop up -d` - start Caddy in the background
- `./develop down` - stop the stack
- `./develop ca-export` - temporarily serve `http://<host>:8080/ca.crt` (10-minute max) for iPhone trust setup

For local Mac validation without hostname changes, use:

```bash
curl -k --resolve hearth.home.arpa:443:127.0.0.1 https://hearth.home.arpa/
```
