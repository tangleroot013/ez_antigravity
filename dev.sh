#!/bin/bash
# dev.sh - Hardened Dev Loop v0.2.2 (Race-Condition Fixed)
set -e

echo "--- 🦆 DEV LOOP START ---"

echo "📦 Step 1: Compiling..."
# Compilation logic

echo "🧪 Step 2: Running Chaos Integration Tests..."
pytest tests/ --color=yes

echo "🔍 Step 3: Running Resilience Audit..."
./resilience_audit.sh

echo "🚩 Step 4: Git Workspace Status..."
git status -s

echo "📊 Step 5: Logging Performance Telemetry..."
./perf.sh | xargs -I {} ./log_perf.sh {}

echo "🛡️ Step 6: Memory Leak Audit..."
# Now passing the command we want to monitor
python tools/leak_sentry.py "./perf.sh" --threshold 100

echo "--- 🦆 DEV LOOP COMPLETE: All systems nominal. Quack! ---"
