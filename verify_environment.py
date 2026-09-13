#!/usr/bin/env python3
"""
verify_environment.py - Zero-Trust Environment & Git Verification for ez_grav
"""
import sys, os, subprocess, json, importlib.util

def print_header(title):
    print(f"\n\033[1;36m=== {title} ===\033[0m")

def verify_python():
    print_header("1. Python Environment")
    print(f"Executable : {sys.executable}")
    print(f"Version    : {sys.version.split()[0]}")
    if sys.version_info >= (3, 8):
        print("\033[1;32m[OK] Python version compatible.\033[0m")

def verify_dependencies():
    print_header("2. Package Dependencies")
    required = ["pytest"]
    for pkg in required:
        if importlib.util.find_spec(pkg):
            print(f" \033[1;32m[OK]\033[0m '{pkg}' is installed.")
        else:
            print(f" \033[1;31m[MISSING]\033[0m '{pkg}' not found. Attempting heal...")
            res = subprocess.run([sys.executable, "-m", "pip", "install", pkg], capture_output=True)
            if res.returncode == 0:
                print(f" \033[1;32m[HEALED]\033[0m Successfully installed {pkg}.")
            else:
                print(f" \033[1;31m[FAILED]\033[0m Could not install {pkg}.")

def verify_ssh_agent():
    print_header("3. SSH Agent Security")
    sock = os.environ.get("SSH_AUTH_SOCK")
    if sock and os.path.exists(sock):
        res = subprocess.run(["ssh-add", "-l"], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"\033[1;32m[OK]\033[0m Agent active with identities loaded at {sock}.")
        else:
            print(f"\033[1;33m[WARN]\033[0m Agent active but no identities loaded.")
    else:
        print(f"\033[1;31m[ERROR]\033[0m SSH_AUTH_SOCK missing or socket not found.")

def verify_devcontainer():
    print_header("4. Devcontainer Config")
    path = ".devcontainer/devcontainer.json"
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                json.load(f)
            print(f"\033[1;32m[OK]\033[0m {path} is valid JSON.")
        except Exception as e:
            print(f"\033[1;31m[ERROR]\033[0m JSON parse failure: {e}")
    else:
        print(f"\033[1;33m[INFO]\033[0m {path} not found.")

def verify_git():
    print_header("5. Git Ops")
    try:
        branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
        print(f" \033[1;32m[OK]\033[0m Branch: {branch}")
        remote = subprocess.check_output(["git", "remote", "-v"], text=True).strip().split('\n')[0]
        print(f" Remote: {remote}")
    except Exception as e:
        print(f"\033[1;31m[ERROR]\033[0m Git check failed: {e}")

def run_tests():
    print_header("6. Unit Tests")
    if os.path.exists("test_ez_grav.py"):
        res = subprocess.run([sys.executable, "-m", "pytest", "test_ez_grav.py", "-v"])
        if res.returncode == 0:
            print("\033[1;32m[OK] All tests passed!\033[0m")
    else:
        print("\033[1;33m[SKIP]\033[0m test_ez_grav.py not found.")

if __name__ == "__main__":
    print("\033[1;33m" + "="*60 + "\n ez_grav Zero-Trust Diagnostic Tool\n" + "="*60 + "\033[0m")
    verify_python()
    verify_dependencies()
    verify_ssh_agent()
    verify_devcontainer()
    verify_git()
    run_tests()
    print(f"\n\033[1;32mVerification complete! Quack!\033[0m")
