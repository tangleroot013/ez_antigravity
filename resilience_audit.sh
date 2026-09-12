#!/bin/bash
# Carter's Workspace Resilience Audit
# Quack! Ensuring no shadow directories or permission drifts.

echo "--- 🦆 Starting Resilience Audit ---"

# 1. Check for shadow directories (root copies of src folders)
if [ -d "ez_antigravity" ]; then
    echo "❌ SHADOW DETECTED: Root directory 'ez_antigravity/' found. Purging..."
    rm -rf ez_antigravity/
    echo "✅ Shadow purged."
else
    echo "✅ No shadow directories found."
fi

# 2. Verify critical file permissions
# Ensure grav_engine.py is 644 (no accidental +x in git)
if [ -f "src/ez_antigravity/grav_engine.py" ]; then
    PERMS=$(stat -c "%a" src/ez_antigravity/grav_engine.py)
    if [ "$PERMS" != "644" ]; then
        echo "❌ PERM DRIFT: grav_engine.py is $PERMS, expected 644. Fixing..."
        chmod 644 src/ez_antigravity/grav_engine.py
    else
        echo "✅ Permissions aligned."
    fi
fi

# 3. Check git cleanliness
if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  GIT DIRTY: Uncommitted changes detected."
else
    echo "✅ Git state is pristine."
fi

echo "--- 🦆 Audit Complete ---"
