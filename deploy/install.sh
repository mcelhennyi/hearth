#!/usr/bin/env bash
# deploy/install.sh — idempotent bare-metal Hearth installer — T-FR-0001-10
#
# Targets:
#   Linux   — Raspberry Pi OS 64-bit (Debian bookworm) with systemd
#   macOS   — 14+ (Apple Silicon) with launchd
#
# Usage:
#   sudo ./deploy/install.sh              # normal install
#   ./deploy/install.sh --dry-run         # print steps without applying
#   ./deploy/install.sh --prefix /tmp/test  # install under a custom root (testing)
#
# Idempotent: safe to run multiple times; already-done steps print [ok].
set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

OPT_HEARTH="/opt/hearth"
ETC_HEARTH="/etc/hearth"
VAR_HEARTH="/var/hearth"
DRY_RUN=""
PREFIX=""

for arg in "$@"; do
  case "$arg" in
    --dry-run)   DRY_RUN=1 ;;
    --prefix=*)  PREFIX="${arg#--prefix=}" ;;
    --prefix)    shift; PREFIX="${1}" ;;
    *) ;;
  esac
done

if [[ -n "$PREFIX" ]]; then
  OPT_HEARTH="${PREFIX}/opt/hearth"
  ETC_HEARTH="${PREFIX}/etc/hearth"
  VAR_HEARTH="${PREFIX}/var/hearth"
fi

VENV="${OPT_HEARTH}/venv"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
ok()   { echo "[ok]  $*"; }
step() { echo "[-->] $*"; }
warn() { echo "[!]   $*" >&2; }

run() {
  if [[ -n "$DRY_RUN" ]]; then
    echo "[dry] $*"
  else
    "$@"
  fi
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    warn "Required command not found: $1"
    return 1
  fi
  ok "found $1 at $(command -v "$1")"
}

ensure_dir() {
  local dir="$1" mode="${2:-755}"
  if [[ -d "$dir" ]]; then
    ok "directory exists: $dir"
  else
    step "creating $dir"
    run mkdir -p "$dir"
    run chmod "$mode" "$dir"
  fi
}

# ---------------------------------------------------------------------------
# Detect platform
# ---------------------------------------------------------------------------
PLATFORM="$(uname -s)"
case "$PLATFORM" in
  Linux)  PLATFORM_IS_LINUX=1 ;;
  Darwin) PLATFORM_IS_MACOS=1 ;;
  *)
    warn "Unsupported platform: $PLATFORM"
    exit 1
    ;;
esac

# ---------------------------------------------------------------------------
# Step 1 — Prerequisite checks
# ---------------------------------------------------------------------------
step "Checking prerequisites"

if [[ -n "${PLATFORM_IS_LINUX:-}" ]]; then
  require_cmd apt-get  || warn "apt-get not found; skipping package install"
  require_cmd systemctl || warn "systemctl not found; service management skipped"
fi

if [[ -n "${PLATFORM_IS_MACOS:-}" ]]; then
  require_cmd brew  || warn "brew not found; skipping package install"
  require_cmd launchctl || warn "launchctl not found; service management skipped"
fi

require_cmd caddy || warn "caddy not found; install caddy before running hearth"

if ! python3 --version 2>/dev/null | grep -qE 'Python 3\.(1[2-9]|[2-9][0-9])'; then
  warn "Python 3.12+ required; current: $(python3 --version 2>&1)"
fi

# ---------------------------------------------------------------------------
# Step 2 — Directory layout
# ---------------------------------------------------------------------------
step "Ensuring directory layout"
ensure_dir "${OPT_HEARTH}"
ensure_dir "${ETC_HEARTH}"
ensure_dir "${VAR_HEARTH}"           700
ensure_dir "${VAR_HEARTH}/plugins"
ensure_dir "${VAR_HEARTH}/run"       750
ensure_dir "${VAR_HEARTH}/secrets"   700
ensure_dir "${VAR_HEARTH}/log"

# ---------------------------------------------------------------------------
# Step 3 — Sync code to /opt/hearth (or note if already there)
# ---------------------------------------------------------------------------
step "Linking/copying repo to ${OPT_HEARTH}"
if [[ "${REPO_ROOT}" == "${OPT_HEARTH}" ]]; then
  ok "repo root IS install root; no copy needed"
else
  if [[ -n "$DRY_RUN" ]]; then
    echo "[dry] rsync -a --delete ${REPO_ROOT}/ ${OPT_HEARTH}/"
  else
    # If rsync is available, use it; otherwise warn (CI / minimal images).
    if command -v rsync >/dev/null 2>&1; then
      rsync -a --delete --exclude='.git' --exclude='.worktrees' \
            "${REPO_ROOT}/" "${OPT_HEARTH}/"
      ok "synced ${REPO_ROOT} → ${OPT_HEARTH}"
    else
      warn "rsync not found; skipping code sync (assume ${OPT_HEARTH} is already populated)"
    fi
  fi
fi

# ---------------------------------------------------------------------------
# Step 4 — Python virtual environment + packages
# ---------------------------------------------------------------------------
step "Ensuring Python venv at ${VENV}"
if [[ -d "${VENV}" ]]; then
  ok "venv already exists: ${VENV}"
else
  step "Creating venv"
  run python3 -m venv "${VENV}"
fi

step "Installing hearth-install and hearth-cli packages"
run "${VENV}/bin/pip" install -q \
  -e "${OPT_HEARTH}/deploy/hearth-install" \
  -e "${OPT_HEARTH}/deploy/hearth-cli"

# ---------------------------------------------------------------------------
# Step 5 — System service installation
# ---------------------------------------------------------------------------
if [[ -n "${PLATFORM_IS_LINUX:-}" ]] && command -v systemctl >/dev/null 2>&1; then
  step "Installing systemd units"

  SYSTEMD_DIR="/etc/systemd/system"
  for unit in hearth-hub.service "hearth-plugin@.service"; do
    src="${SCRIPT_DIR}/systemd/${unit}"
    dst="${SYSTEMD_DIR}/${unit}"
    if [[ ! -f "$src" ]]; then
      warn "Unit source not found: $src"
      continue
    fi
    if [[ -n "$DRY_RUN" ]]; then
      echo "[dry] install ${src} → ${dst}"
    else
      install -m 644 "$src" "$dst"
      ok "installed ${dst}"
    fi
  done

  if [[ -z "$DRY_RUN" ]]; then
    run systemctl daemon-reload
    run systemctl enable hearth-hub.service
    run systemctl start  hearth-hub.service || warn "hearth-hub.service start failed (may not be running yet)"
  fi
fi

if [[ -n "${PLATFORM_IS_MACOS:-}" ]] && command -v launchctl >/dev/null 2>&1; then
  step "Installing launchd plists"

  LAUNCH_DAEMONS="/Library/LaunchDaemons"
  if [[ -n "$PREFIX" ]]; then
    LAUNCH_DAEMONS="${PREFIX}${LAUNCH_DAEMONS}"
    run mkdir -p "${LAUNCH_DAEMONS}"
  fi

  src="${SCRIPT_DIR}/launchd/com.hearth.hub.plist"
  dst="${LAUNCH_DAEMONS}/com.hearth.hub.plist"
  if [[ -f "$src" ]]; then
    if [[ -n "$DRY_RUN" ]]; then
      echo "[dry] install ${src} → ${dst}"
    else
      install -m 644 "$src" "$dst"
      ok "installed ${dst}"
      if [[ -z "$PREFIX" ]]; then
        launchctl load -w "$dst" 2>/dev/null || warn "launchctl load failed (may already be loaded)"
      fi
    fi
  else
    warn "launchd plist not found: $src"
  fi
fi

# ---------------------------------------------------------------------------
# Step 6 — Smoke check
# ---------------------------------------------------------------------------
if [[ -z "$DRY_RUN" ]] && [[ -z "$PREFIX" ]]; then
  step "Smoke check: https://hearth.home.arpa/api/health"
  if command -v curl >/dev/null 2>&1; then
    if curl -sf --max-time 5 https://hearth.home.arpa/api/health >/dev/null 2>&1; then
      ok "https://hearth.home.arpa/api/health responded"
    else
      warn "Health check failed (service may still be starting up)"
    fi
  else
    warn "curl not found; skipping smoke check"
  fi
fi

echo ""
echo "Hearth install complete."
if [[ -n "$DRY_RUN" ]]; then
  echo "(dry-run mode: no changes were made)"
fi
