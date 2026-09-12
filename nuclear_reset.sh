#!/bin/bash
# Carter's Nuclear Reset
# WARNING: This wipes local changes and artifacts to restore a pristine state.
# Quack! Clear the pond!

echo "☢️  INITIATING NUCLEAR RESET... ☢️"
read -p "Are you sure you want to wipe all uncommitted changes and artifacts? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborting. The pond remains untouched."
    exit 1
fi

echo "🧹 Purging untracked files and directories..."
git clean -fd
git checkout .

echo "♻️  Re-verifying environment..."
./resilience_audit.sh

echo "✅ Workspace restored to last known good commit. Quack!"
