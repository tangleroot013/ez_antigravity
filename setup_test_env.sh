#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_DIR="${HOME}/agy-workspace"

cd "${PROJECT_DIR}"

if [[ ! -d ".venv" ]]; then
    python -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest

python -m pytest --version
python -m pytest -q
