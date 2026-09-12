import os
import sys

def fix_permissions():
    if os.geteuid() != 0:
        print("❌ ERROR: This script must be run as root!")
        sys.exit(1)
    
    target = "src/ez_antigravity"
    print(f"Quack! Diving into {target} to clear the muck...")
    
    for root, dirs, files in os.walk(target):
        # Fix directory permissions to 755 (drwxr-xr-x)
        os.chmod(root, 0o755)
        for f in files:
            # Fix file permissions to 644 (-rw-r--r--)
            os.chmod(os.path.join(root, f), 0o644)
            
    print("✅ Permissions restored. The pond is crystal clear!")

if __name__ == "__main__":
    fix_permissions()
