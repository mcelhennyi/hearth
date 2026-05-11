#!/usr/bin/env bash
# @HRT-OPS-012 T-FR-0003-12 — host/CI smoke for install + hearth operator path.
# Runs without pytest: dry-run install, materialized layout, hearth version/doctor/list,
# optional `docker compose config` when Docker is available.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

cleanup() {
  if [[ -n "${SMOKE_TMP:-}" && -d "${SMOKE_TMP}" ]]; then
    rm -rf "${SMOKE_TMP}"
  fi
}
SMOKE_TMP="$(mktemp -d "${TMPDIR:-/tmp}/hearth-install-smoke.XXXXXX")"
trap cleanup EXIT

INSTALL_ROOT="${SMOKE_TMP}/install"
export HEARTH_INSTALL_ROOT="${INSTALL_ROOT}"

echo "== ./install --dry-run =="
./install --dry-run --repo-root "${REPO_ROOT}" --hearth-ref smoke-ci

echo "== ./install (layout + compose files, no docker check / no compose up) =="
./install \
  --repo-root "${REPO_ROOT}" \
  --skip-docker-check \
  --skip-compose-up \
  --hearth-ref smoke-ci

echo "== hearth version =="
./bin/hearth --install-root "${INSTALL_ROOT}" version

echo "== hearth doctor =="
set +e
./bin/hearth --install-root "${INSTALL_ROOT}" doctor
doc_res=$?
set -e
if [[ "${doc_res}" -ne 0 ]]; then
  if command -v docker >/dev/null 2>&1; then
    echo "hearth doctor: expected exit 0 when docker is on PATH" >&2
    exit 1
  fi
  echo "hearth doctor: non-zero without docker CLI (expected); continuing."
fi

echo "== hearth --plugin list =="
./bin/hearth --install-root "${INSTALL_ROOT}" --plugin list

heart="${INSTALL_ROOT}/heart"
overrides="${heart}/compose/overrides/generated.plugins.yml"
if [[ ! -f "${overrides}" ]]; then
  echo "missing generated plugin overrides: ${overrides}" >&2
  exit 1
fi

if command -v docker >/dev/null 2>&1; then
  echo "== docker compose config (install tree) =="
  (
    cd "${heart}/compose"
    docker compose -f docker-compose.yml -f overrides/generated.plugins.yml config >/dev/null
  )
else
  echo "== docker compose config (skipped — no docker on PATH) =="
fi

echo "== hearth-install-smoke: OK =="
