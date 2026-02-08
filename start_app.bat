@echo off
echo Starting PC Part Picker AI...

echo Starting Backend Server on port 8000...
start "Backend Server" cmd /k "uvicorn app:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server on port 3000...
cd frontend
start "Frontend App" cmd /k "npm run dev"

echo.
echo Both servers are starting up!
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo (It may take a few seconds for the frontend to compile)
pause
