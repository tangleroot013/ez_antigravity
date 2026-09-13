#!/usr/bin/env python3
"""agy-sanity: pre-flight workspace validator for ez_antigravity."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

UNESCAPED_UNDERSCORE = re.compile(r"(?<!\\)_")


def repository_root() -> Path:
    """Return the Git repository root."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def check_pytest(repo: Path) -> bool:
    print("🦆 [1/4] Running canonical pytest suite...")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"],
        cwd=repo,
        text=True,
    )

    if result.returncode == 0:
        print("✅ All active unit tests passed cleanly.")
        return True

    print("❌ Pytest failures detected.")
    return False


def check_untracked_tests(repo: Path) -> bool:
    print("\n🦆 [2/4] Checking for untracked test leaks...")

    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--others",
            "--exclude-standard",
            "-z",
            "--",
            "tests/**",
            "tests/*.py",
            "test_*.py",
            "*_test.py",
        ],
        cwd=repo,
        check=True,
        capture_output=True,
    )

    paths = [Path(raw.decode("utf-8")) for raw in result.stdout.split(b"\0") if raw]

    untracked_tests = [path for path in paths if ".archive" not in path.parts]

    if untracked_tests:
        print("⚠️ Found untracked test files:")
        for path in untracked_tests:
            print(f"  - {path}")

        print("👉 Track them in Git or move obsolete files into .archive/.")
        return False

    print("✅ No untracked test leaks found.")
    return True


def check_katex_syntax(repo: Path) -> bool:
    print("\n🦆 [3/4] Auditing Markdown for KaTeX formatting...")

    markdown_files = [
        path
        for path in repo.rglob("*.md")
        if not any(
            excluded in path.parts
            for excluded in {".git", ".venv", ".archive", "__pycache__"}
        )
    ]

    text_block_pattern = re.compile(r"\\text\{([^{}]*)\}")
    errors_found = 0

    for markdown_file in markdown_files:
        content = markdown_file.read_text(encoding="utf-8")

        for line_number, line in enumerate(content.splitlines(), start=1):
            for match in text_block_pattern.finditer(line):
                text_body = match.group(1)

                if UNESCAPED_UNDERSCORE.search(text_body):
                    print(
                        f"❌ KaTeX error in {markdown_file}:{line_number}: "
                        f"{match.group(0)!r}"
                    )
                    print(
                        "   Fix: escape the underscore as '\\_' inside " "\\text{...}."
                    )
                    errors_found += 1

    if errors_found == 0:
        print("✅ LaTeX / KaTeX math blocks are compliant.")
        return True

    return False


def check_whitespace(repo: Path) -> bool:
    print("\n🦆 [4/4] Checking Git whitespace errors...")

    result = subprocess.run(
        ["git", "diff", "--check"],
        cwd=repo,
        text=True,
    )

    if result.returncode == 0:
        print("✅ No whitespace errors found.")
        return True

    print("❌ Whitespace errors detected.")
    return False


def main() -> int:
    print("\nAGY-WORKSPACE PRE-FLIGHT SANITY\n")

    try:
        repo = repository_root()
    except subprocess.CalledProcessError as error:
        print(f"❌ Not inside a Git repository: {error}", file=sys.stderr)
        return 1

    checks = (
        check_pytest(repo),
        check_untracked_tests(repo),
        check_katex_syntax(repo),
        check_whitespace(repo),
    )

    print("\n------------------------------------------")

    if all(checks):
        print("🎉 Workspace is healthy and ready to commit. Quack!")
        return 0

    print("🚨 Sanity check failed. Review the issues above.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
