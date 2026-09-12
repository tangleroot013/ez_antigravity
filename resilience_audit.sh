#!/bin/bash
# Carter's Refined Workspace Resilience Audit
# Quack! Distinguishing between real drift and local debris.

echo "--- 🦆 Starting Resilience Audit ---"

# 1. Check for shadow directories
if [ -d "ez_antigravity" ]; then
    echo "❌ SHADOW DETECTED: Root directory 'ez_antigravity/' found. Purging..."
    rm -rf ez_antigravity/
    echo "✅ Shadow purged."
else
    echo "✅ No shadow directories found."
fi

# 2. Verify critical file permissions
if [ -f "src/ez_antigravity/grav_engine.py" ]; then
    PERMS=$(stat -c "%a" src/ez_antigravity/grav_engine.py)
    if [ "$PERMS" != "644" ]; then
        echo "❌ PERM DRIFT: grav_engine.py is $PERMS, expected 644. Fixing..."
        chmod 644 src/ez_antigravity/grav_engine.py
    else
        echo "✅ Permissions aligned."
    fi
fi

# 3. Precision Git Check
# Check only for modified tracked files
if [[ -n $(git status --porcelain | grep '^ M') ]]; then
    echo "⚠️  GIT DRIFT: Modified tracked files detected. Commit your changes!"
else
    echo "✅ Git tracked state is pristine."
fi

# Check for untracked files (informational only)
if [[ -n $(git status --porcelain | grep '??') ]]; then
    echo "ℹ️  LOCAL DEBRIS: Untracked files exist in the workspace."
else
    echo "✅ Workspace is perfectly clean."
fi

echo "--- 🦆 Audit Complete ---"
