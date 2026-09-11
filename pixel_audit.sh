#!/bin/bash
set -euo pipefail

# RESOLVE PATHS (Based on Initiative D)
# We search the current directory to find exactly where these files live
V3=$(find . -name "__3_" | head -n 1)
V6=$(find . -name "__6_" | head -n 1)
REPORT="~/agy-workspace/v3_v6_pixel_audit.txt"

if [ -z "$V3" ] || [ -z "$V6" ]; then
    echo "❌ Error: Could not find __3_ or __6_ in the current directory."
    echo "Found V3: ${V3:-NOT FOUND}"
    echo "Found V6: ${V6:-NOT FOUND}"
    exit 1
fi

echo "🦆 Quack! Intel locked. Comparing $V3 vs $V6..."

# Generate raw diff
diff -u "$V3" "$V6" > ~/agy-workspace/audit_logs/raw_diff.txt

# Python filter for Visual Deltas
python3 -c "
import os

visual_keywords = ['style', 'class', 'div', 'px', 'rem', 'vh', 'vw', 'color', 'margin', 'padding', 'position', 'top', 'left', 'z-index', 'flex', 'grid']
raw_diff_path = os.path.expanduser('~/agy-workspace/audit_logs/raw_diff.txt')
report_path = os.path.expanduser('~/agy-workspace/v3_v6_pixel_audit.txt')

try:
    with open(raw_diff_path, 'r') as f:
        lines = f.readlines()

    with open(report_path, 'w') as out:
        out.write('=== VISUAL DELTA REPORT: V3 -> V6 ===\n\n')
        for line in lines:
            if line.startswith('-') and not line.startswith('---'):
                if any(k in line.lower() for k in visual_keywords):
                    out.write(line)
    print('✅ Audit complete. Report generated at: ' + report_path)
except Exception as e:
    print(f'❌ Python Error: {e}')
"
