# PowerShell script to start Credang AI Mail Automation
$root = $PSScriptRoot

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   Credang AI Mail Automation - Starting Services" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

# 1. Start Backend in separate window
Write-Host "`n[1/2] Starting Backend on http://localhost:8000..." -ForegroundColor Yellow
$backendVenv = Join-Path $root "backend\.venv\Scripts\python.exe"
if (Test-Path $backendVenv) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\backend'; & '$backendVenv' -m uvicorn main:app --reload --port 8000"
} else {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\backend'; uvicorn main:app --reload --port 8000"
}

# 2. Start Frontend in separate window
Write-Host "[2/2] Starting Frontend on http://localhost:3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\frontend'; npm run dev"

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host " Both servers launched in separate windows!" -ForegroundColor Green
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host "   Backend : http://localhost:8000/docs" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green

