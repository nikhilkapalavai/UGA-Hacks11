@echo off
REM BuildBuddy Multi-Agent PC Builder - Startup Script
REM This script starts both the FastAPI backend and Next.js frontend

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║              BuildBuddy AI - Multi-Agent PC Builder                   ║
echo ║                 Starting Backend & Frontend...                        ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  WARNING: .env file not found!
    echo.
    echo Required environment variables:
    echo   - GOOGLE_CLOUD_PROJECT_ID
    echo   - GOOGLE_CLOUD_LOCATION (default: us-central1)
    echo   - VERTEX_SEARCH_DATA_STORE_ID
    echo.
    echo Please create a .env file with these variables.
    echo.
)

REM Start backend
echo [1/2] Starting FastAPI Backend on port 8000...
echo.
start "BuildBuddy Backend" cmd /k "python app.py"

timeout /t 3 /nobreak

REM Start frontend
echo [2/2] Starting Next.js Frontend on port 3000...
echo.
cd frontend

if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

start "BuildBuddy Frontend" cmd /k "npm run dev"

cd ..

timeout /t 3 /nobreak

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                         STARTUP COMPLETE!                             ║
echo ╠═══════════════════════════════════════════════════════════════════════╣
echo ║                                                                       ║
echo ║  🚀 Frontend:  http://localhost:3000                                  ║
echo ║  ⚙️  Backend:   http://localhost:8000                                  ║
echo ║  📚 API Docs:  http://localhost:8000/docs                             ║
echo ║                                                                       ║
echo ║  Open your browser and navigate to:                                   ║
echo ║  👉 http://localhost:3000                                             ║
echo ║                                                                       ║
echo ║  You'll see two modes:                                                ║
echo ║  1️⃣  Reasoning Mode - Full Build→Critique→Improve pipeline           ║
echo ║  2️⃣  Chat Mode - Simple Q&A about PC components                      ║
echo ║                                                                       ║
echo ║  Try this in Reasoning Mode:                                          ║
echo ║  "Build me a $1200 gaming PC for 1440p 120fps"                       ║
echo ║                                                                       ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.
pause
