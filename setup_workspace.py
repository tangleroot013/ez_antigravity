import os
import subprocess

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

# Create a secure structure for gravity experiments
run("mkdir -p recovery tests logs")
run("chmod 700 recovery") # OPSEC: only owner can enter recovery
run("touch .gitignore")

with open(".gitignore", "a") as f:
    f.write("\n__pycache__/\n.venv/\n*.bak\n*.before-recovery\nlogs/\n")

print("Workspace sanitized. Quack!")
