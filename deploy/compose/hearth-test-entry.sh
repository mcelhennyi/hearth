#!/bin/sh
# Run repo pytest inside the hearth-test Compose service (`./develop test`).
set -eu
cd /work
pip install -q pip setuptools wheel
pip install -q -e ".[test]"
exec pytest -q "$@"
