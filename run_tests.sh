#!/usr/bin/env bash
set -Eeuo pipefail

# 1. Define the strictly required workspace
TARGET_DIR="/home/tangleroot013/agy-workspace"

printf '%s\n' '=== 1. Navigating to Target Workspace ==='
if [ ! -d "$TARGET_DIR" ]; then
    printf 'Error: Target directory %s does not exist. Quack!\n' "$TARGET_DIR" >&2
    exit 1
fi

cd "$TARGET_DIR"

printf 'Working directory: '
pwd
printf 'Git root: '
git rev-parse --show-toplevel

printf '%s\n\n=== 2. Source and Test File Verification ===\n' ''
# Ensure essential files exist
for file in "src/__init__.py" "src/ez_grav.py" "tests/test_grav_engine.py" "pytest.ini"; do
    if [ ! -f "$file" ]; then
        printf 'Missing critical file: %s\n' "$file" >&2
        exit 1
    fi
done

ls -la src/ez_grav.py src/__init__.py tests/test_grav_engine.py

printf '\nTest files found:\n'
find tests -maxdepth 1 -type f -print | sort

printf '%s\n\n=== 3. Verifying Package Resolution ===\n' ''
# This prevents us from testing the wrong version of the code
ACTUAL_PATH=$(python3 -c "import src.ez_grav; print(src.ez_grav.__file__)")
EXPECTED_PATH="$TARGET_DIR/src/ez_grav.py"

printf 'Expected: %s\n' "$EXPECTED_PATH"
printf 'Actual:   %s\n' "$ACTUAL_PATH"

if [[ "$ACTUAL_PATH" != "$EXPECTED_PATH" ]]; then
    printf '\nERROR: Python is importing the wrong ez_grav.py! Quack!\n' >&2
    exit 1
fi

printf '%s\n\n=== 4. SSH Fingerprints & Git Status ===\n' ''
ssh-add -l || printf 'No SSH identities loaded.\n'
git status --short

printf '%s\n\n=== 5. Running Grav Engine Pytest Suite ===\n' ''
# Use python -m pytest to ensure current directory is in sys.path
# Force the rootdir and config file to the workspace
python3 -m pytest \
    --rootdir="$TARGET_DIR" \
    -c "$TARGET_DIR/pytest.ini" \
    tests \
    -v

printf '%s\n\nVerification complete! Quack!\n' ''
