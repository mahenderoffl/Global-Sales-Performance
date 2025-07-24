@echo off
echo Starting Responsive Global Sales Dashboard...
echo.
echo Setting up Python virtual environment...
cd /d "C:\Users\user\Desktop\visualization project"

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing required packages...
    venv\Scripts\python.exe -m pip install --upgrade pip
    venv\Scripts\python.exe -m pip install streamlit plotly pandas numpy openpyxl
)

echo.
echo Starting Responsive Dashboard...
echo Open your browser to: http://localhost:8503
echo Press Ctrl+C to stop the dashboard
echo.

REM Run the responsive dashboard
venv\Scripts\python.exe -m streamlit run src\dashboard_responsive.py --server.port 8503

pause
