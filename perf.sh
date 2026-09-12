#!/bin/bash
# Run the engine through cProfile to find bottlenecks
echo "--- 🦆 Gravity Engine Performance Profile ---"
python3 -m cProfile -s cumulative src/ez_antigravity/grav_engine.py | head -n 20
echo "--- 🦆 Profile Complete ---"
