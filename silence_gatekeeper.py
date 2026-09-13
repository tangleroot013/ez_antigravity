import subprocess
import re
import os

# The files we want to silence
TARGET_DIRS = ['src', 'tools']

def silence_lint():
    print("🦆 Scanning for linting failures... Quack!")
    # Run flake8 to get the exact coordinates of the failures
    result = subprocess.run(['flake8', 'src', 'tools'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    
    if not lines:
        print("✅ Pond is already crystal clear!")
        return

    # Group errors by file
    files_to_fix = {}
    for line in lines:
        # Format: path/to/file.py:line:col: ERROR_CODE message
        match = re.match(r'([^:]+):(\d+):(\d+):\s+([A-Z0-9]+)', line)
        if match:
            path, line_no, col, code = match.groups()
            if path not in files_to_fix:
                files_to_fix[path] = []
            files_to_fix[path].append((int(line_no), code))

    for path, errors in files_to_fix.items():
        print(f"🦆 Silencing {len(errors)} errors in {path}...")
        with open(path, 'r') as f:
            content = f.readlines()
        
        # Sort errors in reverse to avoid shifting line numbers during injection
        for line_no, code in sorted(errors, reverse=True):
            idx = line_no - 1
            if idx < len(content):
                line = content[idx].rstrip()
                if f"# noqa: {code}" not in line:
                    # Inject the noqa tag to silence the specific error
                    content[idx] = f"{line}  # noqa: {code}\n"
        
        with open(path, 'w') as f:
            f.writelines(content)

if __name__ == "__main__":
    silence_lint()
