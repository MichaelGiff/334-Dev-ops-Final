#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" -m compileall app.py recommender.py recipes.py tests
"$PYTHON_BIN" -m pytest -q
