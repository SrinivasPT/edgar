@echo off
REM Batch script to lint and fix code with ruff

echo Running ruff linter and formatter...
echo.

echo [1/3] Checking and fixing linting issues...
uv run ruff check src/ tests/ --fix --unsafe-fixes
if %ERRORLEVEL% neq 0 (
    echo Error: Ruff check failed
    pause
    exit /b 1
)

echo.
echo [2/3] Formatting code...
uv run ruff format src/ tests/
if %ERRORLEVEL% neq 0 (
    echo Error: Ruff format failed
    pause
    exit /b 1
)

echo.
echo [3/3] Running type checker...
uv run mypy src/
if %ERRORLEVEL% neq 0 (
    echo Warning: Type check failed - please review the issues above
)

echo.
echo ✅ Code quality checks completed!
echo.
pause
