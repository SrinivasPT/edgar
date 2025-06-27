#!/usr/bin/env python3
"""
Development task runner for EDGAR Query Tool.
Replaces the need for scripts.toml by providing common development tasks.

Usage:
    python dev.py <task>

Available tasks:
    test         - Run tests
    test-cov     - Run tests with coverage
    lint         - Check code quality
    lint-fix     - Fix auto-fixable linting issues
    format       - Format code
    format-check - Check if code is formatted
    type-check   - Run type checking
    qa           - Run full quality assurance (lint + format + type-check)
    setup-data   - Create data directories
    check-env    - Check environment variables
    build        - Build the package
    clean        - Clean build artifacts
    api          - Start API server
    web          - Start web server
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description=""):
    """Run a shell command and print the result."""
    if description:
        print(f"🔨 {description}")

    if isinstance(cmd, str):
        cmd = cmd.split()

    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False


def main():
    """Main task runner."""
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    task = sys.argv[1]
    project_root = Path(__file__).parent

    tasks = {
        "test": (["uv", "run", "pytest", "tests/", "-v"], "Running tests..."),
        "test-cov": (
            ["uv", "run", "pytest", "tests/", "--cov=edgar", "--cov-report=html"],
            "Running tests with coverage...",
        ),
        "lint": (
            ["uv", "run", "ruff", "check", "edgar/", "tests/"],
            "Checking code quality...",
        ),
        "lint-fix": (
            ["uv", "run", "ruff", "check", "edgar/", "tests/", "--fix"],
            "Fixing auto-fixable issues...",
        ),
        "format": (
            ["uv", "run", "ruff", "format", "edgar/", "tests/"],
            "Formatting code...",
        ),
        "format-check": (
            ["uv", "run", "ruff", "format", "edgar/", "tests/", "--check"],
            "Checking code formatting...",
        ),
        "type-check": (["uv", "run", "mypy", "edgar/"], "Running type checks..."),
        "build": (["uv", "build"], "Building package..."),
        "api": (["edgar-api"], "Starting API server..."),
        "web": (["edgar-web"], "Starting web server..."),
    }

    # Special tasks that need custom logic
    if task == "qa":
        print("🔨 Running full quality assurance...")
        success = True
        success &= run_command(
            ["uv", "run", "ruff", "check", "edgar/", "tests/", "--fix"]
        )
        success &= run_command(["uv", "run", "ruff", "format", "edgar/", "tests/"])
        success &= run_command(["uv", "run", "mypy", "edgar/"])
        if success:
            print("✅ All QA checks passed!")
        else:
            print("❌ Some QA checks failed")
            sys.exit(1)
        return

    elif task == "setup-data":
        print("🔨 Creating data directories...")
        data_dir = project_root / "data" / "edgar_data"
        backup_dir = project_root / "data" / "backups"
        data_dir.mkdir(parents=True, exist_ok=True)
        backup_dir.mkdir(parents=True, exist_ok=True)
        print("✅ Data directories created")
        return

    elif task == "check-env":
        import os

        print("🔨 Checking environment...")
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"OPENAI_API_KEY: {'SET' if api_key else 'NOT SET'}")
        return

    elif task == "clean":
        print("🔨 Cleaning build artifacts...")
        import shutil

        for path in ["build", "dist", "*.egg-info"]:
            path_obj = project_root / path
            if path_obj.exists():
                if path_obj.is_dir():
                    shutil.rmtree(path_obj)
                else:
                    path_obj.unlink()
        print("✅ Build artifacts cleaned")
        return

    # Run predefined tasks
    if task in tasks:
        cmd, description = tasks[task]
        success = run_command(cmd, description)
        if success:
            print(f"✅ Task '{task}' completed successfully")
        else:
            print(f"❌ Task '{task}' failed")
            sys.exit(1)
    else:
        print(f"❌ Unknown task: {task}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
