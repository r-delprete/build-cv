#!/bin/bash
set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-$SCRIPT_DIR/.venv/bin/python}"

cd "$SCRIPT_DIR"

if [[ "$#" -eq 1 && ( "$1" == "--help" || "$1" == "-h" ) ]]; then
    exec "$PYTHON" "$SCRIPT_DIR/main.py" "$1"
fi

ruff check .
exec "$PYTHON" "$SCRIPT_DIR/main.py" "$@"