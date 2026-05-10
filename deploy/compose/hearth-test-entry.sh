#!/bin/sh
# Run repo pytest inside the hearth-test Compose service (`./develop test`).
set -eu
export DEBIAN_FRONTEND=noninteractive
if ! command -v git >/dev/null 2>&1; then
  apt-get update -qq
  apt-get install -y -qq --no-install-recommends git >/dev/null
fi
cd /work
pip install -q pip setuptools wheel
pip install -q -e ".[test]"
exec pytest -q "$@"
