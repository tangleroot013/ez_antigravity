#!/bin/bash
# resilience_audit.sh - OPSEC Sentinel for Permission Drift
# Target: Chromebook Crostini / agy-workspace
# Author: Carter (The Duck)

LOG_FILE="audit_logs/permission_drift.log"
mkdir -p audit_logs

echo "[$(date +'%Y-%m-%dT%H:%M:%S')] Starting Permission Integrity Audit..."

# Identify all shell scripts that SHOULD be executable
# We search for .sh files and verify the 100755 mode (or +x bit)
DRIFT_DETECTED=0

while IFS= read -r script; do
    if [ ! -x "$script" ]; then
        echo "ALERT: Permission Drift Detected on $script"
        echo "[$(date +'%Y-%m-%dT%H:%M:%S')] FAIL: $script lost executable bit" >> "$LOG_FILE"
        DRIFT_DETECTED=1
    fi
done < <(find . -name "*.sh" -not -path "*/.git/*")

if [ $DRIFT_DETECTED -eq 1 ]; then
    echo "❌ Integrity Violation: Executable bits missing. Check $LOG_FILE"
    # Proactive recovery attempt
    echo "Attempting atomic re-hardening of .sh assets..."
    find . -name "*.sh" -not -path "*/.git/*" -exec chmod +x {} +
    echo "✅ Recovery applied. Please verify with 'ls -la'."
else
    echo "✅ Pond is still. No permission drift detected."
fi
