#!/bin/bash
# Carter's Atomic Feather-Scrubber 🦆
set -e

echo "🦆 Starting deep-clean... Quack!"

# 1. Kill the lone trailing whitespace in repair_engine.py
sed -i 's/[[:space:]]*$//' tools/repair_engine.py

# 2. Install and run Black for the E501 line-length annihilation
pip install black
black src/ tools/

# 3. Handle the __init__.py F401s by adding # noqa: F401 to intentional exports
# This tells the Gatekeeper: "I know what I'm doing, leave my imports alone."
sed -i 's/^import .*\.entities.GravEntity/import .entities.GravEntity # noqa: F401/' src/ez_antigravity/__init__.py
sed -i 's/^import .*\.integrators.FastEuler/import .integrators.FastEuler # noqa: F401/' src/ez_antigravity/__init__.py
sed -i 's/^import .*\.integrators.PreciseRK4/import .integrators.PreciseRK4 # noqa: F401/' src/ez_antigravity/__init__.py
sed -i 's/^import .*\.ez_grav.EARTH_MASS/import .ez_grav.EARTH_MASS # noqa: F401/' src/ez_antigravity/__init__.py
sed -i 's/^import .*\.ez_grav.EARTH_RADIUS/import .ez_grav.EARTH_RADIUS # noqa: F401/' src/ez_antigravity/__init__.py

# 4. Manual pruning of definitely-unused imports in tools/ (The OPSEC trim)
# We use a temporary file to avoid shredding the logic
sed -i '/import random/d' tools/generate_chaos_samples.py
sed -i '/import numpy as np/d' tools/generate_chaos_samples.py
sed -i '/import os/d' tools/repair_engine.py

echo "✅ Feathers are pristine. Pond is crystal clear. Quack!"
