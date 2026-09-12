#!/usr/bin/env bash
set -Eeuo pipefail

echo "== Repository candidates =="
find "$HOME" -type d -name ez_jukebox -print 2>/dev/null | head -20

echo
echo "== atomic_io.py candidates =="
find "$HOME" -type f -path '*/ez_jukebox/atomic_io.py' -print 2>/dev/null | head -20

echo
echo "== Systemd unit =="
systemctl --user cat ez-jukebox-import.service || true

echo
echo "== Recent service log =="
journalctl --user -u ez-jukebox-import.service -n 80 --no-pager || true

echo
echo "== Import from current shell =="
python - <<'PYEOF'
import importlib.util
import os
import sys

print("Python:", sys.executable)
print("Working directory:", os.getcwd())
print("sys.path:")
for item in sys.path:
    print("  ", item)

spec = importlib.util.find_spec("ez_jukebox")
print("ez_jukebox spec:", spec)

try:
    import ez_jukebox.atomic_io as atomic_io
    print("atomic_io:", atomic_io.__file__)
except Exception as exc:
    print(type(exc).__name__ + ":", exc)
PYEOF

echo
echo "== Git status =="
git status --short --untracked-files=all
