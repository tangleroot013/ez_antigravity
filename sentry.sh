#!/bin/bash
echo "--- 🦆 OPSEC Sentry Scan ---"

# Search for common secret patterns (API keys, passwords) in the src folder
echo "🔍 Scanning for leaked secrets..."
grep -rE "API_KEY|SECRET|PASSWORD|TOKEN" src/ | grep -v "None" && echo "❌ SECRET LEAK DETECTED!" || echo "✅ No obvious secrets found."

# Check for world-writable files (Security Risk)
echo "🔐 Checking for world-writable files..."
find . -type f -perm -o+w | grep -v ".git" && echo "❌ SECURITY RISK: World-writable files found!" || echo "✅ Permissions are tight."

echo "--- 🦆 Sentry Scan Complete ---"
