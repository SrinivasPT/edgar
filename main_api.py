#!/usr/bin/env python3
"""
Main entry point for the EDGAR Query Tool API server.
"""

import os
import sys
from pathlib import Path

import uvicorn

# Ensure we're in the project root directory
project_root = Path(__file__).parent
os.chdir(project_root)

# Add the src directory to Python path
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


def main():
    """Main entry point for the API server."""
    try:
        from edgar_query.api.server import app

        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Make sure you're running from the project root directory")
        print("and that all dependencies are installed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
