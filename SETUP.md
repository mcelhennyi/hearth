# Hearth Docker-profile setup (Raspberry Pi)

Operator guide for validating **FR-0003** on real Pi hardware: repo-root **`./install`**, **`<install-dir>/hearth/`** layout, and the **`hearth`** CLI.

**Branch:** `feat/FR-0003-hearth-pi-docker-cli` (see [PR #13](https://github.com/mcelhennyi/hearth/pull/13)).

**What this tests:** Install bootstrap, filesystem layout, CLI, and `docker compose up -d` on ARM. The default stack is **hub-smoke** (Alpine placeholder) until FR-0001 hub images exist — not the full hub UI, Caddy, or iPhone PWA (FR-0002).

**Install tree name:** **`hearth/`** under your install root (design amendment **HRT-DEP-001**). Do not use the old `heart/` directory name.

---

## 1. Prerequisites (one-time)

On the Pi (SSH or local terminal):

```bash
# 64-bit Raspberry Pi OS recommended
uname -m    # expect aarch64

# Git + Python 3
sudo apt update
sudo apt install -y git python3

# Docker Engine + Compose v2 (needs 2.20+ for compose "include:")
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"
```

**Log out and back in** (or run `newgrp docker`) so `docker` works without `sudo`.

Verify:

```bash
docker info
docker compose version   # v2.20 or newer
python3 --version        # 3.11+ is fine; 3.12 ideal
```

---

## 2. Get the code

```bash
cd ~
git clone https://github.com/mcelhennyi/hearth.git
cd hearth
git fetch origin feat/FR-0003-hearth-pi-docker-cli
git checkout feat/FR-0003-hearth-pi-docker-cli
git pull
```

If you already cloned the repo:

```bash
cd ~/hearth
git fetch origin
git checkout feat/FR-0003-hearth-pi-docker-cli
git pull
```

Choose an **install root** (parent directory; the tool creates **`hearth/`** inside it):

```bash
export HEARTH_DEPLOY=~/hearth-deploy
```

---

## 3. Optional: automated smoke (quick check)

From the repository root:

```bash
chmod +x ./install scripts/ci/hearth-install-smoke.sh
./scripts/ci/hearth-install-smoke.sh
```

Expect **`hearth-install-smoke: OK`** at the end. This uses a temporary directory and skips `docker compose up`; useful before a full install.

---

## 4. Full install

```bash
cd ~/hearth   # repository root

# Plan only — no filesystem changes
./install --dry-run "$HEARTH_DEPLOY"

# Layout + hearth shim + compose files + docker compose up -d
./install "$HEARTH_DEPLOY" --hearth-ref "$(git rev-parse --short HEAD)"
```

**Success indicators:**

- Exit code **0**
- **`$HEARTH_DEPLOY/hearth/`** exists with `compose/`, `plugins/`, `state/`, `var/`, `bin/`, `VERSION.json`, `README.md`
- **hub-smoke** container running (Alpine placeholder)

```bash
ls -la "$HEARTH_DEPLOY/hearth/"
docker compose -f "$HEARTH_DEPLOY/hearth/compose/docker-compose.yml" ps
```

---

## 5. `hearth` CLI smoke

```bash
export HEARTH_INSTALL_ROOT="$HEARTH_DEPLOY"
export PATH="$HEARTH_DEPLOY/hearth/bin:$PATH"

hearth version
hearth doctor
hearth --plugin list
hearth status
```

Optional stack control:

```bash
hearth stop
hearth start
hearth logs
```

Add **`export PATH=...`** and **`export HEARTH_INSTALL_ROOT=...`** to `~/.bashrc` or `~/.profile` if you want `hearth` on every login.

---

## 6. Record hardware validation (VAL)

For the feature diary, note:

- Pi **model** and OS (`cat /etc/os-release`)
- **Date** and rough duration of `./install`
- Pass/fail: dry-run, full install, `hearth doctor`, `docker compose ps`

Append to:

`tasks/feature-history/FR-0003-hearth-pi-docker-cli/serial-diary.md`

---

## 7. Troubleshooting

| Problem | What to try |
|--------|-------------|
| `permission denied` on `docker` | Re-login after `usermod -aG docker`, or `newgrp docker` |
| Compose errors about `include:` | Upgrade Docker; need Compose **v2.20+** (`docker compose version`) |
| Leftover **`heart/`** directory from an old try | Remove install root or rename `heart` → `hearth` |
| `./install: Permission denied` | `chmod +x ./install` |
| `hearth doctor` fails | Run `docker info` as the same user who will run `hearth` |

---

## 8. Clean re-test

```bash
export HEARTH_DEPLOY=~/hearth-deploy
hearth stop    # if a previous install succeeded
rm -rf "$HEARTH_DEPLOY"
```

Then repeat [section 4](#4-full-install).

---

## 9. Out of scope for this setup

| Topic | Where it lives |
|-------|----------------|
| Full hub app + Mantle PWA | FR-0001 / FR-0002 |
| `hearth.home.arpa`, TLS, iPhone trust | FR-0002, `docs/design/deployment.md` |
| Bare-metal systemd install | `deploy/install.sh`, FR-0001-10 |
| Central plugin registry names | DESIGN-GAP; MVP is git URL only |

---

## Related docs

| Path | Role |
|------|------|
| [`deploy/hearth-install/README.md`](deploy/hearth-install/README.md) | Layout generator and `./install` details |
| [`docs/design/deployment.md`](docs/design/deployment.md) | Docker profile (Pi), amendment **HRT-DEP-001** |
| [`tasks/feature-history/FR-0003-hearth-pi-docker-cli/`](tasks/feature-history/FR-0003-hearth-pi-docker-cli/) | Feature tickets, diary, handoffs |
| [`scripts/ci/hearth-install-smoke.sh`](scripts/ci/hearth-install-smoke.sh) | Host/CI smoke script |
