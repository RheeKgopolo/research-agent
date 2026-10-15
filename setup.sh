#!/usr/bin/env bash
# One-time setup: creates .venv, installs dependencies, creates .env, runs the offline tests.
set -euo pipefail
cd "$(dirname "$0")"

PY=""
for c in python3.13 python3.12 python3; do
  if command -v "$c" >/dev/null && "$c" -c 'import sys; sys.exit(sys.version_info < (3, 12))'; then PY="$c"; break; fi
done
[ -n "$PY" ] || { echo "Python 3.12+ is required (macOS: brew install python@3.12)"; exit 1; }

echo "Using $($PY --version)"
"$PY" -m venv .venv
.venv/bin/python -m pip install -q --upgrade pip
.venv/bin/python -m pip install -q -r requirements-dev.txt
[ -f .env ] || { cp .env.example .env; echo "Created .env - add your API keys"; }
.venv/bin/python -m pytest -q
echo "Done. Activate with: source .venv/bin/activate"
