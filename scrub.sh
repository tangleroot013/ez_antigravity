#!/bin/bash
echo "--- 🦆 Initiating Workspace Scrub ---"

# Remove those messy pytest.ini backups and old JSON backups
echo "🧹 Clearing stale backup files..."
rm -f pytest.ini.backup.*
rm -f HANDOVER.json.backup.*

# Rotate logs: Keep the last 5, purge the rest
if [ -d "logs" ]; then
    echo "♻️  Rotating logs..."
    ls -t logs/*.log 2>/dev/null | tail -n +6 | xargs -r rm
fi

# Clear temporary audit files
rm -rf tmp_audit/* 2>/dev/null

echo "✅ Pond is sparkling clean. Quack!"
