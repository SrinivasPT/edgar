#!/usr/bin/env python3
"""
Script to clean up old directory structure after refactoring.
This script will:
1. Create a backup of the old structure
2. Remove deprecated files and directories
"""

import shutil
from datetime import datetime
from pathlib import Path


def main():
    """Main cleanup function."""
    project_root = Path(__file__).parent.parent

    # Create backup directory
    backup_dir = project_root / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(exist_ok=True)

    print(f"Creating backup in: {backup_dir}")

    # Backup old structure
    old_dirs_to_backup = [
        "src",
        "_scratch_pad",
        "static",  # Old static directory
    ]

    old_files_to_backup = [
        "main_api.py",
        "main_web.py",
    ]

    # Backup directories
    for dir_name in old_dirs_to_backup:
        old_dir = project_root / dir_name
        if old_dir.exists():
            backup_target = backup_dir / dir_name
            shutil.copytree(old_dir, backup_target)
            print(f"Backed up: {dir_name}")

    # Backup files
    for file_name in old_files_to_backup:
        old_file = project_root / file_name
        if old_file.exists():
            shutil.copy2(old_file, backup_dir / file_name)
            print(f"Backed up: {file_name}")

    print("\nBackup completed. You can now safely remove the old structure:")
    print("The following directories and files have been backed up and can be removed:")

    for dir_name in old_dirs_to_backup:
        old_dir = project_root / dir_name
        if old_dir.exists():
            print(f"  - {dir_name}/")

    for file_name in old_files_to_backup:
        old_file = project_root / file_name
        if old_file.exists():
            print(f"  - {file_name}")

    print(f"\nBackup location: {backup_dir}")
    print(
        "\nTo complete the cleanup, you can manually remove the backed-up files and directories."
    )


if __name__ == "__main__":
    main()
