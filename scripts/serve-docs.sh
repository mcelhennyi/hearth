#!/usr/bin/env bash
# Host-only MkDocs fallback (venv). Prefer ./develop docs — Docker + bind mount + live reload.
# Run from repo root: ./scripts/serve-docs.sh [-- mkdocs-serve-args...]
#
# Default bind is 127.0.0.1:5081 so docs sit beside the HTTP quick stack
# (./develop up-quick, port 5080). Pass -a or --dev-addr to override.
#
# Creates .venv if missing, installs requirements-docs.txt, then runs
# mkdocs serve via the venv interpreter (fixes "mkdocs: command not found").
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

VENV="$REPO_ROOT/.venv"
REQ="$REPO_ROOT/requirements-docs.txt"

if [[ ! -f "$REQ" ]]; then
  echo "Missing $REQ" >&2
  exit 1
fi

if [[ ! -d "$VENV" ]]; then
  echo "Creating venv at .venv …" >&2
  python3 -m venv "$VENV"
fi

echo "Installing doc dependencies …" >&2
"$VENV/bin/pip" install -q -r "$REQ"

MKDOCS_ARGS=()
if [[ "${1-}" == "--" ]]; then
  shift
  MKDOCS_ARGS+=("$@")
elif [[ $# -gt 0 ]]; then
  MKDOCS_ARGS+=("$@")
fi

DEFAULT_SERVE_ADDR="127.0.0.1:5081"
needs_default_addr=true
i=0
while [[ $i -lt ${#MKDOCS_ARGS[@]} ]]; do
  arg="${MKDOCS_ARGS[$i]}"
  if [[ "$arg" == "-a" || "$arg" == --dev-addr || "$arg" == --dev-addr=* ]]; then
    needs_default_addr=false
    break
  fi
  i=$((i + 1))
done
if [[ "$needs_default_addr" == true ]]; then
  MKDOCS_ARGS=(-a "$DEFAULT_SERVE_ADDR" "${MKDOCS_ARGS[@]}")
fi

exec "$VENV/bin/python" -m mkdocs serve "${MKDOCS_ARGS[@]}"
