@echo off
REM Entroplain Setup Script for Windows
REM Run from PowerShell or Command Prompt

echo ==============================================================
echo   ENTROPAIN SETUP - Windows
echo ==============================================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is required but not installed.
    echo   Download from: https://www.python.org/downloads/
    echo   Make sure to check "Add Python to PATH" during installation.
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo + Python %PYTHON_VERSION% found

REM Install entroplain
echo.
echo Installing entroplain...
pip install --upgrade entroplain

REM Verify installation
python -c "import entroplain" 2>nul
if errorlevel 1 (
    echo X Installation failed
    exit /b 1
)
echo + entroplain installed successfully

REM Check for API keys
echo.
echo ==============================================================
echo   API KEY SETUP
echo ==============================================================

set PROVIDERS=
if defined OPENAI_API_KEY (
    echo + OPENAI_API_KEY is set
    set PROVIDERS=%PROVIDERS% openai
)
if defined ANTHROPIC_API_KEY (
    echo + ANTHROPIC_API_KEY is set
    set PROVIDERS=%PROVIDERS% anthropic
)
if defined NVIDIA_API_KEY (
    echo + NVIDIA_API_KEY is set
    set PROVIDERS=%PROVIDERS% nvidia
)
if defined GOOGLE_API_KEY (
    echo + GOOGLE_API_KEY is set
    set PROVIDERS=%PROVIDERS% google
)

if "%PROVIDERS%"=="" (
    echo.
    echo ! No API keys found. Set at least one:
    echo.
    echo    set OPENAI_API_KEY=your-key
    echo    set ANTHROPIC_API_KEY=your-key
    echo    set NVIDIA_API_KEY=your-key
    echo    set GOOGLE_API_KEY=your-key
    echo.
    echo    To make permanent, add to System Environment Variables:
    echo    - Search "Environment Variables" in Start menu
    echo    - Edit "User variables" or "System variables"
    echo    - Add new variable with name and key
)

echo.
echo ==============================================================
echo   QUICK START
echo ==============================================================
echo.
echo   REM Analyze entropy:
echo   entroplain analyze "Your prompt here"
echo.
echo   REM Stream with early exit:
echo   entroplain stream --exit-on-converge "Your prompt here"
echo.
echo   REM Start proxy with dashboard:
echo   entroplain-proxy --port 8765 --provider openai
echo   REM Then open http://localhost:8765/dashboard
echo.
echo ==============================================================
echo Setup complete!
