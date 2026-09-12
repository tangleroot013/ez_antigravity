#!/bin/bash
# Carter's Performance Benchmark
# Quack! Ensures the physics engine doesn't slow down.

echo "🦆 Running performance benchmark..."

# Run a simple n-body simulation and time it
time python -c "
import time
from src.ez_antigravity.grav_engine import CommandGravEngine
engine = CommandGravEngine()
start = time.time()
for _ in range(100):
    engine.compute_step()
end = time.time()
print(f'✅ Performance: {(end - start)/100:.6f} seconds per step')
"

# Store the result in a file for tracking
echo "Performance: $(date): $(python -c 'import time; from src.ez_antigravity.grav_engine import CommandGravEngine; engine = CommandGravEngine(); start = time.time(); [engine.compute_step() for _ in range(100)]; end = time.time(); print((end - start)/100)')" >> performance.log
