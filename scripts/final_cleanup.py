#!/usr/bin/env python3
"""
Cleanup script to remove deprecated files and directories after refactoring.
This script safely removes files that have been replaced by the new structure.
"""

import shutil
from pathlib import Path


def main():
    """Remove deprecated files and directories."""
    project_root = Path(__file__).parent.parent

    # Files and directories to remove (already backed up)
    items_to_remove = [
        "src/",  # Old package structure
        "_scratch_pad/",  # Development scratch files
        "static/",  # Moved to edgar/web/static/
        "main_api.py",  # Replaced by edgar-api command
        "main_web.py",  # Replaced by edgar-web command
    ]

    print("🧹 Cleaning up deprecated files and directories...")
    print("=" * 50)

    removed_items = []

    for item_name in items_to_remove:
        item_path = project_root / item_name

        if item_path.exists():
            try:
                if item_path.is_dir():
                    shutil.rmtree(item_path)
                    print(f"✅ Removed directory: {item_name}")
                else:
                    item_path.unlink()
                    print(f"✅ Removed file: {item_name}")
                removed_items.append(item_name)
            except Exception as e:
                print(f"❌ Failed to remove {item_name}: {e}")
        else:
            print(f"⚠️  {item_name} does not exist (already removed)")

    print("\n" + "=" * 50)

    if removed_items:
        print(f"✨ Successfully removed {len(removed_items)} items:")
        for item in removed_items:
            print(f"   - {item}")
    else:
        print("✨ No items needed removal (already clean)")

    print("\n🎉 Cleanup complete!")
    print("\nThe project now uses the new structure:")
    print("   - edgar/ (main package)")
    print("   - edgar-api command (instead of main_api.py)")
    print("   - edgar-web command (instead of main_web.py)")
    print("   - edgar/web/static/ (instead of static/)")

    # Check for any remaining old imports
    print("\n💡 Next steps:")
    print("   1. Run: python scripts/migrate_imports.py")
    print("   2. Test: edgar --help")
    print("   3. Test: edgar api --help")
    print("   4. Test: edgar web --help")


if __name__ == "__main__":
    main()
