# Hearth setup — Pi Docker profile + iPhone PWA prototype (FR-0002 / FR-0003)

Operator guide for a **Raspberry Pi** (or similar ARM host) using repo-root **`./install`**, the **`hearth`** CLI, and the **FR-0002** Mantle PWA + Web Push stack at **`https://hearth.home.arpa/`**.

**Deployment target (this guide):** **Raspberry Pi** — the FR-0002 closeout host. **Mac mini** home-server validation is a **later phase** (after merge or under FR-0001); it is **not** required to follow this SETUP. On macOS, use **`./develop`** in the repo checkout for local dev only until a Mac mini operator runbook exists.

**Branch:** use **`main`** (FR-0002 merged via [PR #3](https://github.com/mcelhennyi/hearth/pull/3)).

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

**LAN DNS (required for iPhones):** Hearth uses the hostname **`hearth.home.arpa`**. iPhones cannot use a Mac-style **`/etc/hosts`** entry. Plan for **Pi-hole** (recommended) or another LAN DNS that resolves that name to your Hearth Pi — see [§5](#5-dns-and-pi-hole-required-for-iphones).

---

## 2. Clone the deploy repository

```bash
cd ~
git clone https://github.com/mcelhennyi/hearth.git
cd hearth
git checkout main
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

### Install the `hearth` CLI permanently (`~/.bashrc`)

After `./install`, add the install root and CLI to your login shell so new SSH sessions have `hearth` on `PATH` (adjust the path if you used a different **`HEARTH_DEPLOY`**):

```bash
# Append once (idempotent marker — safe to re-run)
grep -q 'HEARTH_INSTALL_ROOT' ~/.bashrc 2>/dev/null || cat >> ~/.bashrc <<'EOF'

# Hearth operator CLI (hearth start, hearth pwa build, hearth ca-export, …)
export HEARTH_INSTALL_ROOT="${HEARTH_INSTALL_ROOT:-$HOME/hearth-deploy}"
export PATH="$HEARTH_INSTALL_ROOT/hearth/bin:$PATH"
EOF

source ~/.bashrc
hearth doctor
```

If your install root is not `~/hearth-deploy`, set it explicitly before appending, for example:

```bash
export HEARTH_INSTALL_ROOT=/home/pi/hearth
```

**zsh (optional):** use the same two `export` lines in `~/.zshrc` instead of `~/.bashrc`.

For the current session only (without editing `~/.bashrc`):

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

**`hearth pwa build`** — compiles `apps/hub/web` and copies the built UI into  
`$HEARTH_DEPLOY/hearth/compose/static/` (HTML, JS, icons, PWA manifest). Run after every UI-related `git pull`.

**`hearth restart caddy`** — restarts the reverse-proxy container so it reloads **Caddyfile** rules (for example SPA fallback for `/dashboard`). You usually need **both** after an update: build publishes files; restart applies proxy config.

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

## 5. DNS and Pi-hole (required for iPhones)

Hearth is reached at **`https://hearth.home.arpa/`**. That name must resolve on **every device**, especially **iPhones**, to the **LAN IP of the machine running Caddy** (your Hearth Pi).

Find that IP on the Hearth host:

```bash
hostname -I    # e.g. 192.168.1.50 — use the first address on your home subnet
```

### Why Pi-hole (or equivalent LAN DNS)

| Device | `/etc/hosts` works? | Typical symptom if DNS is wrong |
|--------|-------------------|----------------------------------|
| **Mac** (dev) | Yes — easy to add `192.168.x.x hearth.home.arpa` | Site works on Mac |
| **iPhone** | **No** — no editable hosts file | Safari: **“Safari can’t find the server”** / **“server can’t be found”** |
| **Home Screen PWA** | Same as iPhone | Opens `/dashboard` first; fails without DNS **and** Caddy SPA fallback |

**Lesson from prototype validation:** Mac reachable + iPhone not reachable on the same Wi‑Fi almost always means the Mac has a **hosts-file or resolver shortcut** the phone does not. Fix **LAN DNS**, not the Hearth stack.

Pi-hole is the recommended approach: one **local DNS record** for the whole house, DHCP can hand every client the Pi-hole IP, and you avoid per-device hacks.

Pi-hole may run on the **same** Raspberry Pi as Hearth or on **another** always-on host. The DNS record must point to the **Hearth/Caddy** IP, not necessarily the Pi-hole IP.

### 5.1 Install Pi-hole (if you do not have it yet)

Official installer (run on the Pi or VM that will be your DNS server — often a Pi, not always the Hearth box):

```bash
curl -sSL https://install.pi-hole.net | bash
```

Follow the text UI:

- Pick a **static LAN IP** for the Pi-hole host (reserve it in your router DHCP).
- Choose **upstream DNS** (e.g. Cloudflare `1.1.1.1` / Google `8.8.8.8`) for queries Pi-hole does not answer locally.
- Note the **admin password** printed at the end (or set via `pihole setpassword`).

Admin UI: **`http://pi.hole/admin`** or **`http://<PIHOLE-LAN-IP>/admin`**.

Useful checks on the Pi-hole host:

```bash
pihole status
dig hearth.home.arpa @127.0.0.1 +short    # after §5.2 — should show Hearth Pi IP
```

Docs: [https://docs.pi-hole.net/](https://docs.pi-hole.net/)

### 5.2 Add the Hearth DNS record in Pi-hole

1. Open **Pi-hole Admin → Local DNS → DNS Records** (menu labels vary slightly by version).
2. **Domain:** `hearth.home.arpa`
3. **IP address:** Hearth Pi LAN IP from `hostname -I` (e.g. `192.168.1.50`)
4. Save.

Verify from any machine that uses Pi-hole as DNS:

```bash
dig hearth.home.arpa @<PIHOLE-LAN-IP> +short
# expect: 192.168.x.x  (Hearth Pi, not Pi-hole unless they are the same box)
```

### 5.3 Point clients at Pi-hole

**Router (best):** DHCP DNS server = **Pi-hole LAN IP** only (or Pi-hole primary, router secondary). Renew leases (toggle Wi‑Fi on the iPhone).

**iPhone (per network, if router DHCP is not updated yet):**

**Settings → Wi‑Fi → (your network) → Configure DNS → Manual** → add **only** the Pi-hole IP → save → toggle Wi‑Fi off/on.

Confirm: **Settings → Wi‑Fi → (network) → DNS** shows the Pi-hole address.

**Avoid for Hearth testing:** guest Wi‑Fi (often blocks LAN), iCloud Private Relay, VPN, or cellular-only — the phone must resolve `hearth.home.arpa` on **home Wi‑Fi**.

### 5.4 Mac-only `/etc/hosts` (development shortcut, not enough alone)

For a Mac without Pi-hole yet:

```bash
# /etc/hosts — example only
192.168.1.50   hearth.home.arpa
```

This does **not** help iPhones. Still add the Pi-hole record in [§5.2](#52-add-the-hearth-dns-record-in-pi-hole).

---

## 6. Trust the local CA on each iPhone (required)

On the **Pi**, with the stack running (`hearth start` if needed):

```bash
hearth ca-export
```

This blocks for up to **10 minutes** and serves the root CA at **`http://<PI-LAN-IP>:8080/ca.crt`**.

**Why not always-on?** The file is your **local root CA**; anyone on the LAN who installs it could trust sites signed by that CA. Timed export limits exposure. Re-run `hearth ca-export` whenever you add a device, remove the profile, or **recreate Caddy’s Docker volume** (new CA — old profiles stop working).

**Re-trust after:** new iPhone, removed profile, `docker volume` wipe, or “connection is not private” after DNS was fixed.

On each **iPhone** (same Wi‑Fi, Pi-hole resolving `hearth.home.arpa`):

1. Safari → **`http://<PI-LAN-IP>:8080/ca.crt`** (use **http**, not https; use the Pi’s IP).
2. Install the downloaded configuration profile.
3. **Settings → General → VPN & Device Management** → install the profile.
4. **Settings → General → About → Certificate Trust Settings** → enable **full trust** for the Caddy local root CA.  
   **Without step 4, Safari shows “This Connection Is Not Private.”**
5. Force-quit Safari, then open **`https://hearth.home.arpa/`**.

---

## 7. iPhone PWA + push walkthrough

1. Safari → **`https://hearth.home.arpa/`** — no certificate warning (install CA first).  
   The URL may immediately change to **`/dashboard`** — that is normal (React Router). The server must serve `index.html` for `/dashboard` (Caddy `try_files` in the shipped Caddyfile).
2. Confirm the **PWA-ready** screen and bottom tabs.
3. **Share → Add to Home Screen** while the address bar shows **`https://hearth.home.arpa/`** (not the raw Pi IP — TLS cert is for the hostname).
4. Stay on **home Wi‑Fi** (not cellular). **Close Safari.** Open **Hearth** from the **home-screen icon** (not Safari).  
   The Home Screen app often opens **`/dashboard` first**; without Pi-hole DNS it fails even when Safari worked once.  
   Web Push and notifications **do not work** in an ordinary Safari tab on iOS.
5. **Clear stale PWA cache** when the icon shows a white screen but Safari works:  
   - **Settings → Apps → Safari → Advanced → Website Data** → search `hearth` → delete.  
   - Remove the old Home Screen icon (**Remove App → Delete**).  
   - On the Pi: `hearth pwa build` then `hearth restart caddy`.  
   - Re-add to Home Screen from Safari.
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
| **Mac works, iPhone “can’t find server”** | Mac likely has `/etc/hosts`; iPhone needs Pi-hole record + phone DNS → Pi-hole ([§5](#5-dns-and-pi-hole-required-for-iphones)). `dig hearth.home.arpa @<PIHOLE-IP> +short` on Mac. |
| Pi-hole record wrong IP | **DNS Records** must target **Hearth/Caddy** host, not Pi-hole unless same machine. |
| iPhone ignores Pi-hole | **Wi‑Fi → Configure DNS → Manual** → Pi-hole IP only; toggle Wi‑Fi; disable VPN / Private Relay. |
| “Connection is not private” on iPhone | Enable **Certificate Trust Settings** ([§6](#6-trust-the-local-ca-on-each-iphone-required) step 4), not just the profile. Re-run `hearth ca-export` if Caddy volume was recreated. |
| `:8080/ca.crt` does not download | Ensure `hearth ca-export` is running; check Pi firewall; use **http** + Hearth Pi **LAN IP**. |
| `hearth pwa build` fails TypeScript | `git pull` on `feat/FR-0002-iphone-pwa-prototype`; run `hearth pwa build` again. |
| `hearth doctor` / docker errors | Re-login after `usermod -aG docker`; run `docker info`. |
| Wrong hostname | Use **`hearth.home.arpa`**, not the raw IP, in Safari after trust. |
| Orphan **hub-smoke** container | From an old install — `docker rm -f hearth-hub-smoke` after `hearth stop`. |
| PWA white screen, Safari OK | Stale service worker — [§7 step 5](#7-iphone-pwa--push-walkthrough): website data, delete icon, `hearth pwa build`, `hearth restart caddy`, re-add. |
| Home Screen app: “server can’t be found” | Pi-hole / Wi‑Fi / guest network — [§5](#5-dns-and-pi-hole-required-for-iphones). Home Screen opens `/dashboard` first; needs DNS + Caddy SPA fallback. |
| Safari shows `/dashboard`, app broken | Same as above — DNS for standalone app + `hearth restart caddy` after Caddyfile updates. |
| `rm push-subscriptions.json` permission denied | Created by Docker as root — `sudo rm -f ~/hearth/var/hearth/push-subscriptions.json` |
| `VapidPkHashMismatch` in hub logs | Re-subscribe after `vapid-gen` — clear subscriptions file + reset PWA ([§7](#7-iphone-pwa--push-walkthrough) step 8). |

---

## 10. Clean re-test

```bash
hearth stop
rm -rf "$HEARTH_DEPLOY"
```

Repeat from [section 3](#3-install-layout-and-start-the-stack).

---

## 11. Later phase — Mac mini (not in this SETUP)

FR-0002 **closed on Pi + iPhone**; a second acceptance pass on **Mac mini** (Apple Silicon, always-on macOS) is **deferred** to a later phase — likely FR-0001 platform work or a short follow-up runbook.

When that phase runs, expect the same checklist (TLS, Mantle shell, Web Push) using either:

- **`./develop up`** from a repo checkout on the Mac mini (dev Compose profile), or  
- **`./install`** + **`hearth`** once the Docker-on-Mac install path is documented in `docs/design/deployment.md`.

Record results in **`40-prototype-report.md`** → **Environment A (Mac mini)**. Until then, treat Pi + **`SETUP.md`** as the operator source of truth.

---

## Related docs

| Path | Role |
|------|------|
| [`deploy/hearth-install/README.md`](deploy/hearth-install/README.md) | `./install` layout |
| [`docs/design/deployment.md`](docs/design/deployment.md) | Docker profile + iPhone trust |
| [`deploy/compose/README.md`](deploy/compose/README.md) | Dev `./develop` stack (repo checkout; macOS dev, not Mac mini closeout) |
| [`tasks/feature-history/FR-0002-iphone-pwa-prototype/40-prototype-report.md`](tasks/feature-history/FR-0002-iphone-pwa-prototype/40-prototype-report.md) | Prototype closeout evidence (Pi validated; Mac mini deferred) |
