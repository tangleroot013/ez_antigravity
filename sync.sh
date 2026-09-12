#!/bin/bash
echo "--- 🦆 Syncing Dependencies ---"

# Update pip and install requirements
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Prune stale packages (uninstall things not in requirements.txt)
pip freeze > current_env.txt
sort -u requirements.txt > req_sorted.txt
comm -23 <(sort current_env.txt) req_sorted.txt | xargs -r pip uninstall -y

rm current_env.txt req_sorted.txt
echo "✅ Environment synchronized. Quack!"
