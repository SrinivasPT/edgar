#!/usr/bin/env python3
"""
Migration script to update imports from old structure to new structure.
"""

import re
from pathlib import Path


def update_imports_in_file(file_path):
    """Update imports in a single file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Update import patterns
    patterns = [
        # From old agent imports to new service imports
        (
            r"from src\.edgar_query\.agents\.(\w+) import (\w+)Agent",
            r"from edgar.services.\1 import \2Service",
        ),
        (
            r"from edgar\.agents\.(\w+) import (\w+)Agent",
            r"from edgar.services.\1 import \2Service",
        ),
        # Update class name usage
        (r"(\w+)Agent\(", r"\1Service("),
        # Update old package references
        (r"from src\.edgar_query", r"from edgar"),
        (r"from edgar", r"from edgar"),
        (r"import src\.edgar_query", r"import edgar"),
        (r"import edgar", r"import edgar"),
    ]

    for old_pattern, new_pattern in patterns:
        content = re.sub(old_pattern, new_pattern, content)

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {file_path}")
        return True

    return False


def main():
    """Main migration function."""
    project_root = Path(__file__).parent

    # Files to update
    patterns_to_check = [
        "tests/**/*.py",
        "scripts/**/*.py",
        "*.py",
    ]

    updated_files = []

    for pattern in patterns_to_check:
        for file_path in project_root.glob(pattern):
            if file_path.is_file() and file_path.suffix == ".py":
                if update_imports_in_file(file_path):
                    updated_files.append(file_path)

    if updated_files:
        print(f"\nUpdated {len(updated_files)} files:")
        for file_path in updated_files:
            print(f"  - {file_path}")
    else:
        print("No files needed updating.")


if __name__ == "__main__":
    main()
