#!/bin/bash
# log_perf.sh - Performance Telemetry Logger (Hardened)
# Target: grav_engine physics loop
# Author: Carter (The Duck)

LOG_FILE="audit_logs/perf/engine_perf.csv"

# Initialize CSV header if file is new
if [ ! -f "$LOG_FILE" ]; then
    echo "timestamp,commit,perf_value" > "$LOG_FILE"
fi

# Run the benchmark and capture the final line
RAW_RESULT=$(./perf.sh | tail -n 1)

# OPSEC Data Scrubbing: Extract only the floating point number
# This strips "✅ Performance: ", " seconds per step", etc.
CLEAN_VALUE=$(echo "$RAW_RESULT" | grep -oE '[0-9.]+')

COMMIT=$(git rev-parse --short HEAD)
TIMESTAMP=$(date +'%Y-%m-%dT%H:%M:%S')

if [ -z "$CLEAN_VALUE" ]; then
    echo "❌ Error: Could not parse performance value from output: $RAW_RESULT"
    exit 1
fi

echo "$TIMESTAMP,$COMMIT,$CLEAN_VALUE" >> "$LOG_FILE"
echo "✅ Telemetry Logged: $CLEAN_VALUE (Commit: $COMMIT)"
