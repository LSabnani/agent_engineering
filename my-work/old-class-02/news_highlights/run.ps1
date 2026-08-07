# PowerShell launcher for News Highlights App
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "      News Highlights App Launcher        " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check Python installation
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in system PATH. Please install Python and try again."
    Exit
}

# 2. Check and setup virtual environment
$VenvPath = Join-Path $PSScriptRoot ".venv"
if (-not (Test-Path $VenvPath)) {
    Write-Host "Virtual environment not found. Creating one in .venv..." -ForegroundColor Yellow
    python -m venv .venv
}

# 3. Activate venv and install dependencies
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
if (Test-Path $ActivateScript) {
    . $ActivateScript
} else {
    Write-Warning "PowerShell activation script not found. Trying batch script activation."
    $ActivateBatch = Join-Path $VenvPath "Scripts\activate.bat"
    & cmd /c "$ActivateBatch"
}

Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

# 4. Run application
Write-Host "Starting the Flask server..." -ForegroundColor Green
Write-Host "The website will be active at: http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C in this terminal to stop the server." -ForegroundColor Yellow
python app.py
