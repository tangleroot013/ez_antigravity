#!/bin/bash
# Carter's Unified Dev Orchestrator
# Quack! One command to rule the pond.

set -e # Exit immediately if a command fails

echo "--- 🦆 DEV LOOP START ---"

echo "📦 Step 1: Compiling..."
python3 -m py_compile src/ez_antigravity/grav_engine.py

echo "🧪 Step 2: Running Chaos Integration Tests..."
pytest -q tests/test_chaos_integration.py

echo "🔍 Step 3: Running Resilience Audit..."
./resilience_audit.sh

echo "🚩 Step 4: Git Workspace Status..."
git status --short

echo "--- 🦆 DEV LOOP COMPLETE: All systems nominal. Quack! ---"
