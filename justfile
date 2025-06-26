# Justfile for EDGAR Query Tool
# Install just: https://github.com/casey/just
# Usage: just <recipe>

# Default recipe
default:
    @just --list

# Install dependencies
install:
    uv sync

# Install with dev dependencies  
install-dev:
    uv sync --dev

# Run API server
api:
    uv run python main_api.py

# Run web server
web:
    uv run python main_web.py

# Run both servers (Windows only)
both:
    scripts\start_services.bat

# Run tests
test:
    uv run pytest tests/ -v

# Run tests with coverage
test-cov:
    uv run pytest tests/ --cov=src/edgar_query --cov-report=html

# Lint code
lint:
    uv run ruff check src/ tests/

# Lint and fix auto-fixable issues
lint-fix:
    uv run ruff check src/ tests/ --fix

# Lint and fix including unsafe fixes (like removing whitespace)
lint-fix-all:
    uv run ruff check src/ tests/ --fix --unsafe-fixes

# Format code
format:
    uv run ruff format src/ tests/

# Check if code is formatted (CI/CD friendly)
format-check:
    uv run ruff format src/ tests/ --check

# Type check
type-check:
    uv run mypy src/

# Run all quality checks and fixes
qa: lint-fix-all format type-check

# Run all quality checks
check: lint type-check test

# Build package
build:
    uv build

# Clean build artifacts
clean:
    powershell -Command "Get-ChildItem -Path . -Include '__pycache__', '*.pyc', 'build', 'dist', '*.egg-info' -Recurse | Remove-Item -Recurse -Force"

# Setup data directories
setup-data:
    powershell -Command "New-Item -ItemType Directory -Force -Path 'data\edgar_data', 'data\backups'"

# Check environment
check-env:
    @echo "OPENAI_API_KEY: $(if ($env:OPENAI_API_KEY) { "SET" } else { "NOT SET" })"

# Complete dev setup
dev-setup: install-dev setup-data check-env
    @echo "Development environment ready!"
