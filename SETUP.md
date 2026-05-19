# Hearth setup — Pi Docker profile + iPhone PWA prototype (FR-0002 / FR-0003)

Operator guide for a **Raspberry Pi** (or similar ARM host) using repo-root **`./install`**, the **`hearth`** CLI, and the **FR-0002** Mantle PWA + Web Push stack at **`https://hearth.home.arpa/`**.

**Branch:** `feat/FR-0002-iphone-pwa-prototype` (merge via PR to `main`).

**Install tree:** `<install-dir>/hearth/` (design amendment **HRT-DEP-001** — not `heart/`).

---

## 1. Prerequisites (one-time)

On the Pi (SSH or local terminal):

```bash
uname -m    # expect aarch64

sudo apt update
sudo apt install -y git python3

curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"
```

Log out and back in (or `newgrp docker`) so `docker` works without `sudo`.

```bash
docker info
docker compose version   # v2.20 or newer
python3 --version
```

---

## 2. Clone the deploy repository

```bash
cd ~
git clone https://github.com/mcelhennyi/hearth.git
cd hearth
git fetch origin feat/FR-0002-iphone-pwa-prototype
git checkout feat/FR-0002-iphone-pwa-prototype
git pull
```

Choose an **install root** (parent directory; `./install` creates **`hearth/`** inside it):

```bash
export HEARTH_DEPLOY=~/hearth-deploy
export HEARTH_INSTALL_ROOT="$HEARTH_DEPLOY"
```

---

## 3. Install layout and start the stack

From the **repository root** (`~/hearth`):

```bash
chmod +x ./install
./install --dry-run "$HEARTH_DEPLOY"

./install "$HEARTH_DEPLOY" --hearth-ref "$(git rev-parse --short HEAD)"
```

This writes:

- `$HEARTH_DEPLOY/hearth/compose/docker-compose.yml` — Caddy (`tls internal`) + hub API
- `$HEARTH_DEPLOY/hearth/compose/.env` — `HEARTH_REPO_ROOT` pointing at your git checkout (required for builds)
- `$HEARTH_DEPLOY/hearth/compose/caddy/` — Caddy configs copied from the repo
- `$HEARTH_DEPLOY/hearth/bin/hearth` — CLI shim

Add the CLI to your shell (optional but recommended):

```bash
export PATH="$HEARTH_DEPLOY/hearth/bin:$PATH"
```

---

## 4. Build the Mantle PWA and VAPID keys

Still from the repo checkout; uses Docker via `./develop` under the hood:

```bash
hearth pwa vapid-gen
hearth pwa build
```

`hearth pwa build` compiles `apps/hub/web` and publishes the bundle to  
`$HEARTH_DEPLOY/hearth/compose/static/` (what Caddy serves).

Restart Caddy so it picks up new static files:

```bash
hearth restart caddy
```

Verify:

```bash
hearth status --skip-health
curl -sk --resolve hearth.home.arpa:443:127.0.0.1 https://hearth.home.arpa/api/health
```

Expect `{"status":"ok"}`.

---

## 5. DNS — `hearth.home.arpa`

The iPhone and Pi must resolve **`hearth.home.arpa`** to the Pi’s **LAN IP** (e.g. `192.168.1.50`):

- **Pi-hole / router DNS** (recommended), or
- **`/etc/hosts`** on the Pi, and equivalent DNS on the iPhone.

Find the Pi IP: `hostname -I`

---

## 6. Trust the local CA on each iPhone (required)

On the **Pi**, with the stack running (`hearth start` if needed):

```bash
hearth ca-export
```

This blocks for up to **10 minutes** and serves the root CA at **`http://<PI-LAN-IP>:8080/ca.crt`**.

On each **iPhone** (same Wi‑Fi):

1. Safari → **`http://<PI-LAN-IP>:8080/ca.crt`** (use **http**, not https; use the Pi’s IP).
2. Install the downloaded configuration profile.
3. **Settings → General → VPN & Device Management** → install the profile.
4. **Settings → General → About → Certificate Trust Settings** → enable **full trust** for the Caddy local root CA.  
   **Without step 4, Safari shows “This Connection Is Not Private.”**
5. Force-quit Safari, then open **`https://hearth.home.arpa/`**.

---

## 7. iPhone PWA + push walkthrough

1. Safari → **`https://hearth.home.arpa/`** — no certificate warning (install CA first).
2. Confirm the **PWA-ready** screen and bottom tabs.
3. **Share → Add to Home Screen**.
4. **Close Safari.** Open **Hearth** from the **home-screen icon** (not Safari).  
   Web Push and notifications **do not work** in an ordinary Safari tab on iOS.
5. If the home-screen app is a **white screen**: delete the icon, clear Safari website data for `hearth.home.arpa`, run `hearth pwa build` on the Pi, `hearth restart caddy`, then add to home screen again (stale service-worker cache).
6. Tap **Send test notification** → allow notifications.
7. Push should arrive within ~30 seconds.
8. After any `hearth pwa vapid-gen`, run `sudo rm -f ~/hearth/var/hearth/push-subscriptions.json` (file is owned by Docker) and repeat steps 4–7.

Record results in  
`tasks/feature-history/FR-0002-iphone-pwa-prototype/40-prototype-report.md`.

---

## 8. Day-2 operator commands

| Task | Command |
|------|---------|
| Start stack | `hearth start` |
| Stop stack | `hearth stop` |
| Logs | `hearth logs` or `hearth logs -f caddy` |
| Re-export CA | `hearth ca-export` |
| Rebuild UI after git pull | `hearth pwa build` then `hearth restart caddy` |
| Plugin registry | `hearth --plugin list` |
| Doctor | `hearth doctor` |

Low-level compose passthrough: `hearth compose -- ps`

---

## 9. Troubleshooting

| Problem | What to try |
|--------|-------------|
| “Connection is not private” on iPhone | Enable **Certificate Trust Settings** (section 6 step 4), not just the profile. |
| `:8080/ca.crt` does not download | Ensure `hearth ca-export` is running; check Pi firewall; use LAN IP. |
| `hearth pwa build` fails TypeScript | `git pull` on `feat/FR-0002-iphone-pwa-prototype`; run `hearth pwa build` again. |
| `hearth doctor` / docker errors | Re-login after `usermod -aG docker`; run `docker info`. |
| Wrong hostname | Use **`hearth.home.arpa`**, not the raw IP, in Safari after trust. |
| Orphan **hub-smoke** container | From an old install — `docker rm -f hearth-hub-smoke` after `hearth stop`. |
| PWA white screen, Safari OK | Stale service worker — `hearth pwa build`, `hearth restart caddy`, delete home-screen icon, clear website data, re-add. |
| `rm push-subscriptions.json` permission denied | Created by Docker as root — `sudo rm -f ~/hearth/var/hearth/push-subscriptions.json` |
| `VapidPkHashMismatch` in hub logs | Re-subscribe after `vapid-gen` — clear subscriptions file + reset PWA (step 8 above). |

---

## 10. Clean re-test

```bash
hearth stop
rm -rf "$HEARTH_DEPLOY"
```

Repeat from [section 3](#3-install-layout-and-start-the-stack).

---

## Related docs

| Path | Role |
|------|------|
| [`deploy/hearth-install/README.md`](deploy/hearth-install/README.md) | `./install` layout |
| [`docs/design/deployment.md`](docs/design/deployment.md) | Docker profile + iPhone trust |
| [`deploy/compose/README.md`](deploy/compose/README.md) | Dev `./develop` stack (repo checkout) |
| [`tasks/feature-history/FR-0002-iphone-pwa-prototype/40-prototype-report.md`](tasks/feature-history/FR-0002-iphone-pwa-prototype/40-prototype-report.md) | Prototype closeout evidence |
