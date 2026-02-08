#!/bin/bash

# BuildBuddy Multi-Agent PC Builder - Startup Script (Linux/Mac)
# This script starts both the FastAPI backend and Next.js frontend

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║              BuildBuddy AI - Multi-Agent PC Builder                   ║"
echo "║                 Starting Backend & Frontend...                        ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  WARNING: .env file not found!"
    echo ""
    echo "Required environment variables:"
    echo "  - GOOGLE_CLOUD_PROJECT_ID"
    echo "  - GOOGLE_CLOUD_LOCATION (default: us-central1)"
    echo "  - VERTEX_SEARCH_DATA_STORE_ID"
    echo ""
    echo "Please create a .env file with these variables."
    echo ""
fi

# Start backend
echo "[1/2] Starting FastAPI Backend on port 8000..."
echo ""
python app.py &
BACKEND_PID=$!

sleep 3

# Start frontend
echo "[2/2] Starting Next.js Frontend on port 3000..."
echo ""
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!

cd ..

sleep 3

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                         STARTUP COMPLETE!                             ║"
echo "╠═══════════════════════════════════════════════════════════════════════╣"
echo "║                                                                       ║"
echo "║  🚀 Frontend:  http://localhost:3000                                  ║"
echo "║  ⚙️  Backend:   http://localhost:8000                                  ║"
echo "║  📚 API Docs:  http://localhost:8000/docs                             ║"
echo "║                                                                       ║"
echo "║  Open your browser and navigate to:                                   ║"
echo "║  👉 http://localhost:3000                                             ║"
echo "║                                                                       ║"
echo "║  You'll see two modes:                                                ║"
echo "║  1️⃣  Reasoning Mode - Full Build→Critique→Improve pipeline           ║"
echo "║  2️⃣  Chat Mode - Simple Q&A about PC components                      ║"
echo "║                                                                       ║"
echo "║  Try this in Reasoning Mode:                                          ║"
echo "║  \"Build me a \$1200 gaming PC for 1440p 120fps\"                      ║"
echo "║                                                                       ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
