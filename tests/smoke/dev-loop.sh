#!/usr/bin/env bash
# Smoke test: T-FR-0001-01 dev-loop acceptance
#
# Starts the Compose stack, waits for https://hearth.home.arpa/ to return HTTP 200
# with a body containing "Hearth", then tears down.
#
# Usage (host-only; requires Docker and /etc/hosts or DNS for hearth.home.arpa):
#   tests/smoke/dev-loop.sh
#
# VAL note: Docker-in-Docker is not available in the hearth-test container, so
# this test runs on the host as a documented exception. See serial-diary.md T-FR-0001-01.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HEARTH_URL="https://hearth.home.arpa/"
MAX_WAIT=60     # seconds
POLL_INTERVAL=2

# ── helpers ───────────────────────────────────────────────────────────────────

log()  { printf '[smoke] %s\n' "$*"; }
fail() { printf '[smoke] FAIL: %s\n' "$*" >&2; exit 1; }

cleanup() {
  log "Tearing down stack..."
  "${REPO_ROOT}/develop" down --remove-orphans >/dev/null 2>&1 || true
}

# ── 1. Start the stack (detached) ─────────────────────────────────────────────

log "Starting stack: ./develop up -d"
"${REPO_ROOT}/develop" up -d

trap cleanup EXIT

# ── 2. Wait for hearth.home.arpa to respond ───────────────────────────────────

log "Waiting up to ${MAX_WAIT}s for ${HEARTH_URL} ..."
elapsed=0
while true; do
  http_code=$(curl -k -s -o /dev/null -w "%{http_code}" \
    --resolve "hearth.home.arpa:443:127.0.0.1" \
    --max-time 5 \
    "${HEARTH_URL}" 2>/dev/null || true)

  if [[ "${http_code}" == "200" ]]; then
    log "Got HTTP 200 after ${elapsed}s"
    break
  fi

  elapsed=$(( elapsed + POLL_INTERVAL ))
  if [[ ${elapsed} -ge ${MAX_WAIT} ]]; then
    fail "Timed out after ${MAX_WAIT}s waiting for HTTP 200 (last code: ${http_code})"
  fi
  sleep "${POLL_INTERVAL}"
done

# ── 3. Assert body contains "Hearth" ─────────────────────────────────────────

log "Checking response body for 'Hearth'..."
body=$(curl -k -s \
  --resolve "hearth.home.arpa:443:127.0.0.1" \
  --max-time 10 \
  "${HEARTH_URL}")

if echo "${body}" | grep -q "Hearth"; then
  log "Body contains 'Hearth' — PASS"
else
  fail "Body does not contain 'Hearth'. Body: ${body}"
fi

# ── 4. Tear down (via trap) ───────────────────────────────────────────────────

log "Smoke test PASSED"
