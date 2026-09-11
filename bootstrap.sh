#!/bin/bash
set -euo pipefail

# bootstrap.sh - The ez_grav environment initializer
# Quack! Hardening the perimeter for high-precision telemetry.

PROJECT_NAME="ez_grav"
VENV_NAME=".venv"

echo -e "\nInitializing $PROJECT_NAME development environment... Quack!\n"

# 1. Verify Python 3 availability
if ! command -v python3 &> /dev/null; then 
    echo "Error: python3 is required but not installed. Aborting." >&2 
    exit 1 
fi

echo "==> Found Python runtime: $(python3 --version)"

# 2. Provision workspace structure
echo "==> Provisioning workspace directory structure..."
mkdir -p .devcontainer src tests docs

# 3. Generate config files using a Python heredoc
echo "==> Generating devcontainer configuration and dependency manifest..."
python3 <<'PYEOF'
import os
import json

devcontainer_json = {
    "name": "ez_grav Development Environment",
    "image": "mcr.microsoft.com/devcontainers/python:1-3.11-bullseye",
    "features": { "ghcr.io/devcontainers/features/github-cli:1": {} },
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "streetsidesoftware.code-spell-checker"
            ]
        }
    },
    "postCreateCommand": "pip3 install --user -r requirements.txt || true",
    "remoteUser": "vscode"
}

requirements = "pytest>=7.0.0\npyyaml>=6.0\n"

with open(".devcontainer/devcontainer.json", "w") as f:
    json.dump(devcontainer_json, f, indent=4)

with open("requirements.txt", "w") as f:
    f.write(requirements)

print("Devcontainer and requirements files generated successfully.")
PYEOF

# 4. Set up local Python virtual environment
if [ ! -d "$VENV_NAME" ]; then 
    echo "> Creating local Python virtual environment ($VENV_NAME)..."
    python3 -m venv "$VENV_NAME" 
fi

echo "==> Installing dependencies..."
source "$VENV_NAME/bin/activate"
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

# 5. Hardening permissions
chmod +x bootstrap.sh

# 6. Git initialization
if [ ! -d ".git" ]; then 
    echo "> Initializing fresh Git repository..."
    git init
    git add .devcontainer requirements.txt bootstrap.sh
    echo "> Initial project skeleton staged." 
else 
    echo "==> Git repository already initialized." 
fi

echo -e "\nEnvironment hardened and fully provisioned. Ready for deployment!"
echo "To activate your local shell session, run: source $VENV_NAME/bin/activate\n"
