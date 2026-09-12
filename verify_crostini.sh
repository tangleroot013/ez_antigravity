#!/bin/bash
# Carter's Crostini Sanity Check
# Quack! Ensures the container is running in a healthy state.

echo "--- 🦆 Crostini Environment Check ---"

# 1. Check systemd availability
if ! command -v systemctl &> /dev/null; then
    echo "❌ systemd not found. Crostini may be misconfigured."
    exit 1
fi

# 2. Check user namespace (Crostini runs in user namespace)
if [ ! -e /proc/self/ns/user ]; then
    echo "❌ User namespace not available. Crostini may be broken."
    exit 1
fi

# 3. Check for .venv activation
if [ ! -d ".venv" ] || [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not active. Run 'source .venv/bin/activate'."
fi

# 4. Check disk space in Crostini (common issue)
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}')
if [[ "${DISK_USAGE%\%}" -gt 90 ]]; then
    echo "❌ Crostini disk usage at ${DISK_USAGE}. Clean up before proceeding."
    exit 1
fi

echo "✅ Crostini environment is healthy."
