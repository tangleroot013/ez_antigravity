#!/bin/bash
# Carter's Crostini Auto-Recovery
# Quack! Fixes Crostini before you even notice it's broken.

echo "--- 🦆 Crostini Auto-Recovery ---"

# 1. Check and repair systemd
if ! command -v systemctl &> /dev/null; then
    echo "❌ systemd not found. Attempting repair..."
    sudo apt-get update && sudo apt-get install -y systemd
    if ! command -v systemctl &> /dev/null; then
        echo "❌ systemd repair failed. Crostini may be broken."
        exit 1
    fi
    echo "✅ systemd repaired."
fi

# 2. Check and repair dbus
if ! command -v dbus-launch &> /dev/null; then
    echo "❌ dbus not found. Attempting repair..."
    sudo apt-get update && sudo apt-get install -y dbus
    if ! command -v dbus-launch &> /dev/null; then
        echo "❌ dbus repair failed."
        exit 1
    fi
    echo "✅ dbus repaired."
fi

# 3. Check and repair .venv
if [ ! -d ".venv" ] || [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment missing or inactive. Attempting repair..."
    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt
    fi
    pip install pytest
    echo "✅ Virtual environment repaired."
fi

# 4. Run Crostini sanity check
if ! ./verify_crostini.sh; then
    echo "❌ Crostini sanity check failed after repair."
    exit 1
fi

echo "✅ Crostini auto-recovery complete."
