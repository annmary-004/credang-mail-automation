@echo off
echo ========================================================
echo   Credang AI Mail Automation - Starting Web App
echo ========================================================
echo.
cd /d "%~dp0backend"

echo Launching App Server on http://localhost:8000 ...
"C:\Users\hp\.local\bin\uv.exe" run --with-requirements requirements.txt uvicorn main:app --reload --port 8000
pause
