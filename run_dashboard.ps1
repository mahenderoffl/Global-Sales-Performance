# Global Sales Performance Dashboard Launcher
Write-Host "Starting Global Sales Performance Dashboard..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Navigate to src directory
Set-Location src

# Run the dashboard
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "    Dashboard Starting..." -ForegroundColor Cyan
Write-Host "    Open your browser and go to:" -ForegroundColor Cyan
Write-Host "    http://localhost:8501" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

streamlit run dashboard.py

Read-Host "Press Enter to continue..."
