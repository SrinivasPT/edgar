@echo off
echo Starting Edgar Query services with uv...

:: Check if uv is available
uv --version >nul 2>&1
if errorlevel 1 (
    echo uv not found. Installing uv...
    powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
    if errorlevel 1 (
        echo Failed to install uv. Falling back to python...
        goto fallback
    )
)

:: Start FastAPI server in a new cmd window using uv
start cmd /k "title EDGAR API Server && uv run python main_api.py"

:: Wait a moment for API to start
timeout /t 3

:: Start HTML server in another window using uv
start cmd /k "title EDGAR HTML Server && uv run python main_web.py"

goto end

:fallback
echo Using fallback python execution...
start cmd /k "title EDGAR API Server && python main_api.py"
timeout /t 3
start cmd /k "title EDGAR HTML Server && python main_web.py"

:end
echo Services started. 
echo API server runs on http://localhost:8000
echo HTML app runs on http://localhost:3000/app.htm
echo.
echo Available uv commands:
echo   uv run python main_api.py    - Run API server
echo   uv run python main_web.py    - Run web server  
echo   uv run pytest tests/         - Run tests
echo   uv run ruff check src/       - Lint code
echo   uv run ruff format src/      - Format code
