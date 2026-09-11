#!/usr/bin/env bash
set -euo pipefail

# agy-sweep: One-keystroke workspace cleanup script
# Safely purges backup debris, temporary logs, and pycache without touching .archive/

echo "🦆 Sweeping agy-workspace debris..."

# 1. Remove timestamped backup files and .bak files in root and scripts/
# We use find to avoid "No such file or directory" errors when the glob is empty.
find . -maxdepth 2 -type f \( -name "*.bak" -o -name "*.before-recovery" -o -name ".backup.*" \) -delete

# 2. Clear root level temporary caches
rm -rf .pytest_cache
rm -rf pycache

# 3. Recursively purge all __pycache__ directories in src and tests
find src tests -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

echo "✨ Pond cleaned! Kept .archive/ safe. Quack!"
