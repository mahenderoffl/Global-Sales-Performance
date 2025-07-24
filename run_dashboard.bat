@echo off
echo Starting Global Sales Performance Dashboard...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Navigate to src directory
cd src

REM Run the dashboard
echo.
echo ======================================
echo    Dashboard Starting...
echo    Open your browser and go to:
echo    http://localhost:8501
echo ======================================
echo.

"%~dp0venv\Scripts\streamlit.exe" run "%~dp0src\dashboard.py" --server.port 8501

pause
