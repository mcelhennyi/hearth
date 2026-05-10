#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

STACK_URL="https://hearth.home.arpa/"
KNOWN_BODY="Hearth prototype placeholder"

cleanup() {
  ./develop down >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "[T-FR-0002-01] starting stack"
./develop up -d

echo "[T-FR-0002-01] waiting for HTTPS placeholder"
for _ in {1..40}; do
  # Transient TLS handshake errors while Caddy issues internal certs — retry quietly.
  if curl -ks --resolve hearth.home.arpa:443:127.0.0.1 "$STACK_URL" 2>/dev/null | grep -Fq "$KNOWN_BODY"; then
    break
  fi
  sleep 1
done

HTML="$(curl -ksS --resolve hearth.home.arpa:443:127.0.0.1 "$STACK_URL")"
echo "$HTML" | grep -Fq "$KNOWN_BODY"

echo "[T-FR-0002-01] starting CA export"
./develop ca-export >/tmp/t-fr-0002-01-ca-export.log 2>&1 &
CA_EXPORT_PID=$!

for _ in {1..30}; do
  if curl -fsS "http://127.0.0.1:8080/ca.crt" >/tmp/t-fr-0002-01-ca.crt; then
    break
  fi
  sleep 1
done

test -s /tmp/t-fr-0002-01-ca.crt
grep -Fq "BEGIN CERTIFICATE" /tmp/t-fr-0002-01-ca.crt

kill "$CA_EXPORT_PID" >/dev/null 2>&1 || true
wait "$CA_EXPORT_PID" >/dev/null 2>&1 || true

echo "[T-FR-0002-01] PASS"
