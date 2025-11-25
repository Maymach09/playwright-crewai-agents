# UI & Backend Development Guide

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Demo vs Real Mode](#demo-vs-real-mode)
3. [Architecture](#architecture)
4. [Backend (FastAPI)](#backend-fastapi)
5. [Frontend (React + TypeScript)](#frontend-react--typescript)
6. [How to Start/Stop Servers](#how-to-startstop-servers)
7. [API Documentation](#api-documentation)
8. [How to Make Changes](#how-to-make-changes)
9. [Troubleshooting](#troubleshooting)
10. [Development Workflow](#development-workflow)

---

## Project Overview

This project has two main components:
- **Backend API** (FastAPI) - Handles agent execution and data
- **Frontend UI** (React) - Visual interface for users

They communicate via:
- **REST API** - For requests/responses
- **Server-Sent Events (SSE)** - For real-time streaming updates

### 🎭 Important: Demo vs Real Mode

The system supports **two modes**:

- **🎭 Demo Mode** (default): Simulated agents, no API key needed, instant results
- **🚀 Real Mode**: Actual AI agents, requires LLM API key, 5-15 minute execution

**For detailed information**, see [DEMO_VS_REAL_MODE.md](../guides/DEMO_VS_REAL_MODE.md)

**Quick Setup:**
```bash
# Demo mode (no API key needed)
echo "API_MODE=demo" > .env
python api/server.py

# Real mode (requires API key)
echo "API_MODE=real" > .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
python api/server.py
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                       │
│                   http://localhost:3000                     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Planner    │  │  Generator   │  │    Healer    │    │
│  │   Robot 🧠   │  │   Robot ⚙️   │  │   Robot 🔧   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│  [Scenario Input] [Agent Select] [Start Button]           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP + SSE
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                       │
│                   http://localhost:8000                     │
│                                                             │
│  API Endpoints:                                            │
│  • GET  /api/health          - Health check               │
│  • GET  /api/rag/stats       - RAG statistics             │
│  • POST /api/workflow/start  - Start workflow             │
│  • GET  /api/workflow/{id}/stream - SSE stream            │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │           CrewAI Agents + RAG System                 │ │
│  │   Planner → Generator → Healer                       │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Backend (FastAPI)

### 📁 Location
```
api/
└── server.py          # Main FastAPI application
```

### 🔧 What It Does
- Exposes REST API endpoints
- Runs AI agents (Planner, Generator, Healer)
- Streams real-time updates via Server-Sent Events (SSE)
- Manages RAG knowledge base
- Handles workflow orchestration

### 📝 Key Files
- **api/server.py** (276 lines)
  - FastAPI app configuration
  - API endpoints definition
  - SSE streaming logic
  - Workflow management

### 🔌 API Endpoints

| Method | Endpoint | Purpose | Example |
|--------|----------|---------|---------|
| GET | `/` | Root health check | Returns service info |
| GET | `/api/health` | Detailed health + RAG status | Check if backend is working |
| GET | `/api/rag/stats` | RAG knowledge base stats | Get count of stored items |
| POST | `/api/workflow/start` | Start new workflow | Begin planner/generator/healer |
| GET | `/api/workflow/{id}/stream` | SSE stream of updates | Real-time agent events |
| GET | `/api/workflow/{id}/status` | Get workflow status | Check if complete/running |
| GET | `/api/workflows` | List recent workflows | View history |

### 📦 Dependencies
```python
fastapi>=0.104.0      # Web framework
uvicorn[standard]     # ASGI server
pydantic>=2.0.0       # Data validation
```

---

## Frontend (React + TypeScript)

### 📁 Location
```
ui/
├── src/
│   ├── App.tsx        # Main React component (300+ lines)
│   ├── App.css        # Styling with animations
│   └── index.tsx      # Entry point
├── public/
│   └── index.html
└── package.json       # Dependencies
```

### 🎨 What It Does
- Displays 3 animated robot cards (Planner, Generator, Healer)
- Shows RAG knowledge base statistics
- Allows selecting agent type (Full Workflow, or individual agents)
- Real-time progress updates via SSE
- Activity log of all agent events
- Responsive, animated UI

### 📝 Key Files

#### **ui/src/App.tsx** (Main Component)
Contains:
- State management (useState hooks)
- API calls (axios)
- SSE connection (EventSource)
- Robot animations and progress bars
- Agent selection logic

Key state variables:
```typescript
scenario          // Test scenario input
selectedAgent     // full, planner, generator, healer
testFile          // For healer/generator context
isRunning         // Workflow status
ragStats          // Knowledge base stats
agentStates       // Progress for each robot
events            // Activity log
```

#### **ui/src/App.css** (Styling)
Contains:
- Robot card styles
- Bounce animation (`@keyframes bounce`)
- Progress bar styling
- Responsive grid layout
- Color schemes for each agent

### 📦 Dependencies
```json
react              // UI library
react-dom          // DOM rendering
typescript         // Type safety
axios              // HTTP client
react-scripts      // Build tooling
```

---

## How to Start/Stop Servers

### ▶️ Starting Backend (Port 8000)

**Option 1: Foreground (see logs)**
```bash
cd /Users/maymach09/Documents/GenAI09/MacOS/Playwright/playwright_agents
source venv/bin/activate
python api/server.py
```

**Option 2: Background**
```bash
cd /Users/maymach09/Documents/GenAI09/MacOS/Playwright/playwright_agents
source venv/bin/activate
python api/server.py &
```

**You'll see:**
```
🚀 Starting Playwright AI Agents API Server...
📊 Dashboard will be available at: http://localhost:8000
📖 API Docs: http://localhost:8000/docs
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete.
```

### ▶️ Starting Frontend (Port 3000)

```bash
cd /Users/maymach09/Documents/GenAI09/MacOS/Playwright/playwright_agents/ui
npm start
```

**You'll see:**
```
Compiled successfully!
You can now view ui in the browser.
  Local:            http://localhost:3000
webpack compiled successfully
```

### 🛑 Stopping Servers

**Kill by port:**
```bash
# Kill backend (port 8000)
lsof -ti :8000 | xargs kill -9

# Kill frontend (port 3000)
lsof -ti :3000 | xargs kill -9
```

**Kill by process name:**
```bash
# Kill backend
pkill -f "python api/server.py"

# Kill frontend
pkill -f "react-scripts start"
```

**Check if running:**
```bash
# Check both ports
lsof -i :8000 -i :3000

# Or check processes
ps aux | grep -E "(python api/server|react-scripts)" | grep -v grep
```

---

## API Documentation

### 🔍 Where to Find It

**Interactive Swagger UI:**
```
http://localhost:8000/docs
```

**Alternative ReDoc:**
```
http://localhost:8000/redoc
```

### 📖 How to Use Swagger UI

1. **Start backend** server (must be running)
2. **Open browser** to http://localhost:8000/docs
3. **You'll see** all endpoints listed
4. **Click any endpoint** to expand it
5. **Click "Try it out"** button
6. **Fill parameters** in the form
7. **Click "Execute"** to test
8. **See response** below

### 🧪 Testing Endpoints

**Example: Get RAG Stats**
```bash
curl http://localhost:8000/api/rag/stats
```

**Response:**
```json
{
  "total_items": 25,
  "test_fixes": 12,
  "code_patterns": 5,
  "test_plans": 4,
  "application_knowledge": 4
}
```

**Example: Start Workflow**
```bash
curl -X POST http://localhost:8000/api/workflow/start \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "Create new account",
    "agent": "planner"
  }'
```

**Response:**
```json
{
  "workflow_id": "wf_20251120_163456",
  "status": "queued",
  "message": "Workflow wf_20251120_163456 started successfully"
}
```

**Example: Stream Events (SSE)**
```bash
curl -N http://localhost:8000/api/workflow/wf_20251120_163456/stream
```

**Response (streaming):**
```
data: {"agent": "planner", "status": "started", "message": "🧠 Planner agent initialized"}

data: {"agent": "planner", "status": "progress", "progress": 25, "message": "Found partial match in RAG"}

data: {"agent": "planner", "status": "completed", "progress": 100, "message": "Test plan created successfully"}
```

---

## How to Make Changes

### 🔧 Backend Changes (api/server.py)

**1. Add a new endpoint:**
```python
@app.get("/api/new-endpoint")
async def new_endpoint():
    return {"message": "Hello!"}
```

**2. Modify agent behavior:**
- Find `generate_agent_events()` function
- Update the `agent_events` dictionary
- Add new events or change messages

**3. Add request parameters:**
```python
class WorkflowRequest(BaseModel):
    scenario: str
    agent: str
    new_param: Optional[str] = None  # Add this
```

**4. Restart backend** to apply changes:
```bash
# Kill old process
lsof -ti :8000 | xargs kill -9

# Start new one
python api/server.py
```

**Note:** Backend has auto-reload enabled, so it should restart automatically when you save changes!

---

### 🎨 Frontend Changes

#### **Modify UI Layout (App.tsx)**

**Change text:**
```tsx
<h1>🤖 Test Automation Agents</h1>
// Change to:
<h1>🤖 My Custom Title</h1>
```

**Add new input field:**
```tsx
<input
  type="text"
  value={newState}
  onChange={(e) => setNewState(e.target.value)}
  placeholder="New field..."
  className="scenario-input"
/>
```

**Add new state:**
```tsx
const [newState, setNewState] = useState('default');
```

#### **Modify Styling (App.css)**

**Change robot colors:**
```css
.robot-progress-fill {
  background-color: #ff5733;  /* New color */
}
```

**Change animation speed:**
```css
@keyframes bounce {
  /* ... existing ... */
}
/* Add to .robot-icon.working: */
animation: bounce 2s infinite;  /* Change from 1s to 2s */
```

**Modify card sizes:**
```css
.robot-card {
  padding: 48px 32px;  /* Increase from 32px 24px */
}
```

#### **Frontend Auto-Reloads!**
- Save your changes
- Browser automatically reloads
- No need to restart `npm start`

---

### 🔗 Connecting Backend to Frontend

**Frontend calls backend:**
```typescript
// In App.tsx
const response = await axios.post(`${API_BASE}/api/workflow/start`, {
  scenario: scenario,
  agent: selectedAgent
});
```

**`API_BASE` is defined as:**
```typescript
const API_BASE = 'http://localhost:8000';
```

**To change backend URL** (e.g., for production):
```typescript
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

Then set environment variable:
```bash
export REACT_APP_API_URL=https://your-api.com
```

---

## Troubleshooting

### ❌ "Address already in use" Error

**Problem:** Port 8000 or 3000 is already in use

**Solution:**
```bash
# Kill the process using the port
lsof -ti :8000 | xargs kill -9  # Backend
lsof -ti :3000 | xargs kill -9  # Frontend

# Then restart
python api/server.py  # Backend
npm start             # Frontend
```

### ❌ Frontend Can't Connect to Backend

**Problem:** Network error, CORS error, or timeout

**Check:**
1. **Is backend running?**
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **Is CORS enabled?** (Check api/server.py)
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Should be "*" for local dev
   )
   ```

3. **Check browser console** (F12 in Chrome/Edge)
   - Look for red error messages
   - Check Network tab for failed requests

### ❌ "Module not found" Error

**Backend:**
```bash
# Activate virtual environment first
source venv/bin/activate

# Then check if installed
pip list | grep fastapi

# If missing, install
pip install -r requirements.txt
```

**Frontend:**
```bash
cd ui
npm install  # Reinstall all packages
```

### ❌ Backend Returns 500 Error

**Check backend logs:**
- Look at terminal where `python api/server.py` is running
- Error messages will show there
- Common issues:
  - RAG database not initialized
  - Missing environment variables
  - Python dependencies not installed

### ❌ UI Shows Blank Page

**Check:**
1. **Browser console** (F12) for JavaScript errors
2. **Is npm start still running?**
3. **Clear browser cache** (Ctrl+Shift+R or Cmd+Shift+R)
4. **Check ui/src/App.tsx** for syntax errors

---

## Development Workflow

### 🔄 Typical Development Session

**1. Start both servers:**
```bash
# Terminal 1: Backend
cd /path/to/playwright_agents
source venv/bin/activate
python api/server.py

# Terminal 2: Frontend
cd /path/to/playwright_agents/ui
npm start
```

**2. Open in browser:**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

**3. Make changes:**
- Edit `api/server.py` → Backend auto-reloads
- Edit `ui/src/App.tsx` → Frontend auto-reloads
- Edit `ui/src/App.css` → Frontend auto-reloads

**4. Test:**
- Try in browser UI
- Or use Swagger UI (http://localhost:8000/docs)
- Or use curl commands

**5. Debug:**
- Backend logs in Terminal 1
- Frontend logs in browser console (F12)

---

### 🎯 Common Tasks

#### Add a New Agent Type

**Backend (api/server.py):**
```python
agent_events = {
    "planner": [...],
    "generator": [...],
    "healer": [...],
    "newagent": [  # Add this
        {"agent": "newagent", "status": "started", "message": "New agent started"},
        {"agent": "newagent", "status": "completed", "progress": 100, "message": "Done"}
    ]
}
```

**Frontend (ui/src/App.tsx):**
```tsx
// Add to dropdown
<option value="newagent">🆕 New Agent</option>

// Add to agentStates
const [agentStates, setAgentStates] = useState({
    planner: { status: 'idle', progress: 0, message: '' },
    generator: { status: 'idle', progress: 0, message: '' },
    healer: { status: 'idle', progress: 0, message: '' },
    newagent: { status: 'idle', progress: 0, message: '' }  // Add this
});

// Add robot card in JSX
<div className={`robot-card ${agentStates.newagent.status !== 'idle' ? 'active' : ''}`}>
  <div className="robot-icon">🆕</div>
  <h4>New Agent</h4>
  {/* ... progress bar ... */}
</div>
```

#### Change Agent Colors

**Frontend (ui/src/App.tsx):**
```tsx
const getAgentColor = (agent: string) => {
  switch (agent) {
    case 'planner': return '#8b5cf6';    // purple
    case 'generator': return '#3b82f6';  // blue
    case 'healer': return '#10b981';     // green
    case 'newagent': return '#f59e0b';   // orange (add this)
    default: return '#6b7280';
  }
};
```

#### Add New API Endpoint

**Backend (api/server.py):**
```python
@app.get("/api/tests/list")
async def list_tests():
    """List all test files"""
    test_files = []
    # Your logic here
    return {"tests": test_files}
```

**Frontend (ui/src/App.tsx):**
```tsx
const fetchTests = async () => {
  try {
    const response = await axios.get(`${API_BASE}/api/tests/list`);
    console.log(response.data);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

---

## 📚 Key Concepts

### What is REST API?
- **RE**presentational **S**tate **T**ransfer
- Client sends HTTP request → Server responds with data
- Like ordering at a restaurant: you ask for something, they bring it

### What is Server-Sent Events (SSE)?
- Server pushes updates to client in real-time
- One-way: Server → Client (no client response needed)
- Like a news ticker: server keeps sending updates
- Used for our progress updates

### What is CORS?
- **C**ross-**O**rigin **R**esource **S**haring
- Security feature in browsers
- Allows frontend (port 3000) to talk to backend (port 8000)
- We enable it in backend with `CORSMiddleware`

### What is TypeScript?
- JavaScript with types
- Catches errors before running
- Better autocomplete in editor
- Used in our React frontend

### What is React Hook?
- Functions like `useState`, `useEffect`
- Manage component state and side effects
- `useState` = store data
- `useEffect` = run code on mount/update

---

## 🚀 Quick Reference

### Essential Commands

```bash
# Check if servers are running
lsof -i :8000 :3000

# Kill servers
lsof -ti :8000 | xargs kill -9
lsof -ti :3000 | xargs kill -9

# Start backend
cd /path/to/playwright_agents
source venv/bin/activate
python api/server.py

# Start frontend
cd /path/to/playwright_agents/ui
npm start

# Test backend
curl http://localhost:8000/api/health

# View API docs
open http://localhost:8000/docs

# View frontend
open http://localhost:3000
```

### Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend UI | http://localhost:3000 | Main user interface |
| Backend API | http://localhost:8000 | API server |
| API Docs (Swagger) | http://localhost:8000/docs | Interactive API documentation |
| API Docs (ReDoc) | http://localhost:8000/redoc | Alternative API docs |
| Health Check | http://localhost:8000/api/health | Check if backend is working |
| RAG Stats | http://localhost:8000/api/rag/stats | Knowledge base statistics |

### File Structure Quick Reference

```
playwright_agents/
├── api/
│   └── server.py              # Backend API (EDIT HERE for backend changes)
├── ui/
│   ├── src/
│   │   ├── App.tsx            # Main UI component (EDIT HERE for UI logic)
│   │   ├── App.css            # Styling (EDIT HERE for colors/animations)
│   │   └── index.tsx          # Entry point (rarely edit)
│   ├── public/
│   │   └── index.html         # HTML template (rarely edit)
│   └── package.json           # Frontend dependencies
├── requirements.txt           # Backend dependencies
├── venv/                      # Python virtual environment
└── UI_BACKEND_GUIDE.md        # This guide!
```

---

## 💡 Tips

1. **Keep both terminals visible** - One for backend logs, one for frontend
2. **Use browser DevTools** (F12) - Check console for JavaScript errors
3. **Check Swagger UI first** - Test backend endpoints before UI changes
4. **Git commit often** - Save your progress frequently
5. **Read error messages** - They usually tell you exactly what's wrong
6. **Auto-reload is your friend** - Both servers reload on file changes
7. **Backend logs are valuable** - Check Terminal 1 for detailed errors
8. **Use curl for API testing** - Faster than clicking through UI

---

## 📞 Help Resources

**FastAPI Documentation:**
- https://fastapi.tiangolo.com/

**React Documentation:**
- https://react.dev/

**TypeScript Handbook:**
- https://www.typescriptlang.org/docs/

**Axios (HTTP client):**
- https://axios-http.com/

**Server-Sent Events:**
- https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events

---

**Last Updated:** November 20, 2025
**Project:** Playwright AI Agents with RAG
**Version:** 2.0.0
