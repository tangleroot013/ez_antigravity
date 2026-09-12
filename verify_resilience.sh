#!/bin/bash
# Carter's Resilience Audit - Quack!
echo "--- [RESILIENCE AUDIT START] ---"
# Check venv health
if [ -d ".venv" ]; then echo "✅ Venv exists"; else echo "❌ Venv missing"; fi
# Check Git cleanliness
if [[ $(git status --porcelain) ]]; then echo "⚠️ Uncommitted changes detected"; else echo "✅ Git state clean"; fi
# Check for world-writable files (OPSEC)
find . -type f -perm -0002 | grep -v ".git" && echo "❌ World-writable files found!" || echo "✅ Permissions hardened"
echo "--- [AUDIT COMPLETE] ---"
