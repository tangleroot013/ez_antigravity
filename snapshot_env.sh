#!/bin/bash
# snapshot_env.sh - Environment DNA Map
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SNAP_DIR="backups/snapshots/$TIMESTAMP"
mkdir -p "$SNAP_DIR"

pip freeze > "$SNAP_DIR/python_deps.txt"
systemctl list-units --type=service --state=running > "$SNAP_DIR/active_services.txt"
ldd $(which python3) > "$SNAP_DIR/binary_deps.txt"
git rev-parse HEAD > "$SNAP_DIR/commit_hash.txt"

echo "✅ Nest-Snapshot saved to $SNAP_DIR"
