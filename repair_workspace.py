import os
import shutil
import subprocess
from pathlib import Path

def fix_permissions():
    print("Quack! Starting comprehensive workspace permission and git state repair...")
    
    # Target directories to maintain strict permission hygiene
    targets = [
        Path("src/ez_antigravity"),
        Path("tests"),
        Path("tools")
    ]
    
    for target in targets:
        if target.exists():
            print(f"📁 Inspecting and repairing target directory: {target}")
            try:
                target.chmod(0o755)
                for path in target.rglob("*"):
                    if path.is_dir():
                        path.chmod(0o755)
                    elif path.is_file():
                        path.chmod(0o644)
            except (PermissionError, OSError) as e:
                print(f"⚠️ Warning setting permissions on {target}: {e}")
                print("   Root ownership detected. Try running with: sudo python3 repair_workspace.py")

    # Remove embedded .git directory inside Mermaids or other submodules
    submodules_to_clean = [
        Path("Mermaids/.git")
    ]
    
    for submodule_git in submodules_to_clean:
        if submodule_git.exists():
            print(f"🧹 Removing nested .git repository from {submodule_git.parent}...")
            shutil.rmtree(submodule_git, ignore_errors=True)

    # Clean git cache and re-add to ensure pristine index tracking
    try:
        print("🔄 Refreshing git index and staging changes...")
        # Use check=False for rm because it may fail if the directory isn't in the index
        subprocess.run(["git", "rm", "-r", "--cached", "Mermaids"], capture_output=True, check=False)
        subprocess.run(["git", "add", "."], check=True)
        print("✅ Git index updated and synchronized successfully.")
    except Exception as e:
        print(f"⚠️ Git staging warning: {e}")

    print("🎉 Comprehensive workspace repair completed successfully! Quack! The pond is crystal clear.")

if __name__ == "__main__":
    fix_permissions()
