#!/usr/bin/env python3
"""
Main entry point for the EDGAR Query Tool API server.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from edgar.api import main

if __name__ == "__main__":
    main()
