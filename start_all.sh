#!/bin/bash
# Start All Services Script - Backend API + Frontend UI

echo "════════════════════════════════════════════════════"
echo "  🚀 Starting Playwright AI Agents System"
echo "════════════════════════════════════════════════════"
echo ""

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Create logs directory if it doesn't exist
mkdir -p logs

# ============================================
# STEP 1: Stop any existing servers
# ============================================
echo "🛑 Stopping existing servers..."

# Stop backend (port 8000)
lsof -ti :8000 | xargs kill -9 2>/dev/null
pkill -9 -f "python api/server.py" 2>/dev/null
pkill -9 -f "uvicorn" 2>/dev/null

# Stop frontend (port 3000)
lsof -ti :3000 | xargs kill -9 2>/dev/null
pkill -9 -f "react-scripts start" 2>/dev/null
pkill -9 -f "npm start" 2>/dev/null

# Wait a bit for ports to be released
sleep 2

# Verify ports are free
if lsof -i :8000 >/dev/null 2>&1; then
    echo "⚠️  Port 8000 still in use. Trying harder..."
    lsof -ti :8000 | xargs kill -9 2>/dev/null
    sleep 2
fi

if lsof -i :3000 >/dev/null 2>&1; then
    echo "⚠️  Port 3000 still in use. Trying harder..."
    lsof -ti :3000 | xargs kill -9 2>/dev/null
    sleep 2
fi

echo "✅ Ports cleared"
echo ""

# ============================================
# STEP 2: Start Backend Server
# ============================================
echo "🔧 Starting backend API server..."

# Activate virtual environment and start server
source venv/bin/activate

# Start in background with nohup
nohup python api/server.py > logs/backend.log 2>&1 &
BACKEND_PID=$!

echo "   📝 Backend PID: $BACKEND_PID"
echo "   ⏳ Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/api/health >/dev/null 2>&1; then
    echo "   ✅ Backend is running!"
    echo "   📊 Health: http://localhost:8000/api/health"
    echo "   📖 API Docs: http://localhost:8000/docs"
    
    # Show current mode
    MODE=$(curl -s http://localhost:8000/api/health | python3 -c "import sys, json; print(json.load(sys.stdin).get('mode', 'unknown'))" 2>/dev/null)
    if [ "$MODE" = "demo" ]; then
        echo "   🎭 Mode: DEMO MODE (simulated agents)"
    elif [ "$MODE" = "real" ]; then
        echo "   🚀 Mode: REAL MODE (actual AI agents)"
    fi
else
    echo "   ❌ Backend failed to start"
    echo "   📋 Check logs: tail -f logs/backend.log"
    exit 1
fi

echo ""

# ============================================
# STEP 3: Start Frontend UI
# ============================================
echo "🎨 Starting frontend UI server..."

cd ui
nohup npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "   📝 Frontend PID: $FRONTEND_PID"
echo "   ⏳ Waiting for frontend to compile..."

# Wait for frontend to be ready (check logs)
for i in {1..30}; do
    if grep -q "webpack compiled successfully" logs/frontend.log 2>/dev/null; then
        echo "   ✅ Frontend is running!"
        break
    fi
    if grep -q "Failed to compile" logs/frontend.log 2>/dev/null; then
        echo "   ❌ Frontend compilation failed"
        echo "   📋 Check logs: tail -f logs/frontend.log"
        exit 1
    fi
    sleep 1
done

echo ""
echo "════════════════════════════════════════════════════"
echo "  ✨ All services are running!"
echo "════════════════════════════════════════════════════"
echo ""
echo "🌐 Frontend UI:    http://localhost:3000"
echo "🔌 Backend API:    http://localhost:8000"
echo "📖 API Docs:       http://localhost:8000/docs"
echo ""
echo "📋 View Logs:"
echo "   Backend:  tail -f logs/backend.log"
echo "   Frontend: tail -f logs/frontend.log"
echo ""
echo "🛑 Stop All:"
echo "   lsof -ti :8000 | xargs kill -9"
echo "   lsof -ti :3000 | xargs kill -9"
echo ""
echo "════════════════════════════════════════════════════"
