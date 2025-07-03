@echo off
REM Infrastructure Issue Reporter - Windows Setup Script
REM This script automates the setup process for Windows systems

echo ========================================
echo Infrastructure Issue Reporter Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo pip found:
pip --version
echo.

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Create uploads directory
echo Creating uploads directory...
if not exist "src\static\uploads" mkdir "src\static\uploads"

REM Create demo data
echo Creating demo data and admin user...
python create_demo_data.py
if errorlevel 1 (
    echo ERROR: Failed to create demo data
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Admin Login Credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo To start the application:
echo   1. Open Command Prompt in this directory
echo   2. Run: venv\Scripts\activate.bat
echo   3. Run: python src\main.py
echo   4. Open browser to: http://localhost:5001
echo.
echo For network access, see DEPLOYMENT.md
echo.

REM Ask if user wants to start the application now
set /p start_now="Start the application now? (y/n): "
if /i "%start_now%"=="y" (
    echo.
    echo Starting Infrastructure Issue Reporter...
    echo Press Ctrl+C to stop the application
    echo.
    python src\main.py
)

pause

