import re
from pathlib import Path


def migrate_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if "from .telemetry import logger" not in content:
        content = "from .telemetry import logger\n" + content

    new_content = re.sub(r'print\((.*?)\)', r'logger.info(\1)', content)

    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        return True
    return False


def main():
    src_dir = Path("src/ez_antigravity")
    count = 0
    for py_file in src_dir.rglob("*.py"):
        if migrate_file(py_file):
            print(f"🦆 Migrated {py_file} to structured logging...")
            count += 1
    print(f"✅ Migration complete. {count} files updated. Quack!")


if __name__ == "__main__":
    main()
