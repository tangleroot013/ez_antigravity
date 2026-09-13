#!/bin/bash
# baseline_perf.sh - Establish physics loop equilibrium
set -e

ITERATIONS=10
LOG_FILE="audit_logs/perf/baseline_$(date +%Y%m%d).csv"

mkdir -p audit_logs/perf

echo "timestamp,commit,iteration,perf_value" > "$LOG_FILE"

COMMIT=$(git rev-parse --short HEAD)
echo "🦆 Baselining engine performance over $ITERATIONS iterations... Quack!"

for i in $(seq 1 $ITERATIONS); do
    # Execute the performance script and capture the value
    VALUE=$(./perf.sh | grep -oE '[0-9.]+' | tail -1)
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "$TIMESTAMP,$COMMIT,$i,$VALUE" >> "$LOG_FILE"
    echo "Iteration $i/$ITERATIONS: $VALUE"
done

echo "✅ Baseline complete. Data stored in $LOG_FILE"
