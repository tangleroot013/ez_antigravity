#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH="$(dirname "$0")/src" \
  python -m agy_synth.stream "$@"
