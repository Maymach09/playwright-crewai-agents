# 🎯 Quick Navigation Guide

Your one-stop reference for navigating the Playwright CrewAI Agents repository.

## 🚀 I Want To...

### Get Started
- **"I'm new here"** → [README.md](README.md)
- **"Quick setup"** → [docs/guides/QUICKSTART.md](docs/guides/QUICKSTART.md)
- **"Start the UI"** → [docs/api/UI_BACKEND_GUIDE.md](docs/api/UI_BACKEND_GUIDE.md)

### Use the Dashboard
- **"Launch UI"** → `cd ui && npm start` (see [UI Guide](docs/api/UI_BACKEND_GUIDE.md))
- **"Start backend"** → `python api/server.py` (see [UI Guide](docs/api/UI_BACKEND_GUIDE.md))
- **"API endpoints"** → http://localhost:8000/docs or [docs/api/API.md](docs/api/API.md)

### Run Agents (CLI)
- **"Run planner"** → `python src/test_ai_assistant/main.py --agent planner`
- **"Run generator"** → `python src/test_ai_assistant/main.py --agent generator`
- **"Run healer"** → `python src/test_ai_assistant/main.py --agent healer`
- **"Full workflow"** → `python src/test_ai_assistant/main.py`

### Work with RAG
- **"RAG guide"** → [docs/rag/RAG_TOOLS_GUIDE.md](docs/rag/RAG_TOOLS_GUIDE.md)
- **"Check RAG stats"** → http://localhost:8000/api/rag/stats
- **"Test RAG"** → `python examples/scripts/test_rag.py`
- **"Clear RAG"** → `rm -rf rag_storage/`

### Development
- **"Architecture"** → [docs/guides/ARCHITECTURE.md](docs/guides/ARCHITECTURE.md)
- **"Contribute"** → [docs/guides/CONTRIBUTING.md](docs/guides/CONTRIBUTING.md)
- **"Project structure"** → [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **"API reference"** → [docs/api/API.md](docs/api/API.md)

### Examples
- **"Sample scripts"** → [examples/scripts/](examples/scripts/)
- **"Test plans"** → [examples/test_plans/](examples/test_plans/)
- **"Sample tests"** → [examples/sample_tests/](examples/sample_tests/)

### Troubleshooting
- **"Servers not starting"** → [docs/api/UI_BACKEND_GUIDE.md#troubleshooting](docs/api/UI_BACKEND_GUIDE.md)
- **"Port in use"** → `lsof -ti :8000 | xargs kill -9`
- **"Module not found"** → `pip install -r requirements.txt`
- **"Security"** → [docs/guides/SECURITY.md](docs/guides/SECURITY.md)

---

## 📁 Directory Quick Reference

| Directory | What's There | Go There If... |
|-----------|-------------|----------------|
| `api/` | Backend server | You want to modify API endpoints |
| `ui/` | React dashboard | You want to change the UI |
| `src/` | Core agents | You want to modify agent behavior |
| `docs/` | All documentation | You need guides or references |
| `examples/` | Scripts & samples | You want example code |
| `tests/` | Generated tests | You want to see generated tests |

---

## 🔧 Essential Commands

### Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install

# Install UI dependencies
cd ui && npm install
```

### Run Servers
```bash
# Backend (Terminal 1)
python api/server.py

# Frontend (Terminal 2)
cd ui && npm start
```

### Check Status
```bash
# Are servers running?
lsof -i :8000 :3000

# Backend health check
curl http://localhost:8000/api/health

# Frontend
open http://localhost:3000
```

### Kill Servers
```bash
# Kill backend
lsof -ti :8000 | xargs kill -9

# Kill frontend
lsof -ti :3000 | xargs kill -9
```

---

## 📖 Documentation Map

```
docs/
├── README.md                    # Documentation index
│
├── api/                         # Backend & API
│   ├── API.md                   # REST endpoints
│   └── UI_BACKEND_GUIDE.md      # Complete UI guide ⭐
│
├── guides/                      # User guides
│   ├── QUICKSTART.md            # Start here! ⭐
│   ├── ARCHITECTURE.md          # System design
│   ├── CONTRIBUTING.md          # How to help
│   └── SECURITY.md              # Stay safe
│
└── rag/                         # RAG system
    └── RAG_TOOLS_GUIDE.md       # RAG reference
```

**⭐ = Most important for beginners**

---

## 🎯 By Role

### I'm a User
1. [README.md](README.md) - Overview
2. [docs/guides/QUICKSTART.md](docs/guides/QUICKSTART.md) - Setup
3. [docs/api/UI_BACKEND_GUIDE.md](docs/api/UI_BACKEND_GUIDE.md) - Use the dashboard

### I'm a Developer
1. [docs/guides/ARCHITECTURE.md](docs/guides/ARCHITECTURE.md) - How it works
2. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Code organization
3. [docs/api/API.md](docs/api/API.md) - API reference
4. [docs/guides/CONTRIBUTING.md](docs/guides/CONTRIBUTING.md) - How to contribute

### I'm an Administrator
1. [docs/guides/SECURITY.md](docs/guides/SECURITY.md) - Security
2. [Dockerfile](Dockerfile) - Deployment
3. [docker-compose.yml](docker-compose.yml) - Container setup

---

## 🔍 Finding Specific Things

### "Where is the [X] agent code?"
→ `src/test_ai_assistant/config/agents.yaml` (definitions)
→ `src/test_ai_assistant/crew.py` (orchestration)
→ `src/test_ai_assistant/tools/` (tools they use)

### "Where are the [X] tests?"
→ `tests/` (generated Playwright tests)
→ `examples/sample_tests/` (sample tests)

### "Where is the [X] configuration?"
→ `playwright.config.ts` (Playwright)
→ `src/test_ai_assistant/config/` (agents & tasks)
→ `.env` (environment variables)

### "Where are generated [X]?"
→ `examples/test_plans/` (test plans)
→ `tests/` (test files)
→ `rag_storage/` (RAG knowledge)

### "Where are the [X] docs?"
→ `docs/api/` (API & backend)
→ `docs/guides/` (user guides)
→ `docs/rag/` (RAG system)

---

## 💡 Pro Tips

1. **Always start servers before using UI**
   ```bash
   python api/server.py &  # Backend
   cd ui && npm start      # Frontend
   ```

2. **Check Swagger for API testing**
   ```
   http://localhost:8000/docs
   ```

3. **Use browser DevTools for UI debugging**
   - Press F12 in Chrome/Edge
   - Check Console tab for errors
   - Check Network tab for API calls

4. **RAG stores learned knowledge**
   - First run is slow (explores app)
   - Second run is fast (uses RAG)
   - Clear with `rm -rf rag_storage/`

5. **Generated files go to**
   - Test plans: `examples/test_plans/`
   - Test files: `tests/`
   - Logs: `logs/`

---

## 🆘 Help!

### "Nothing works!"
1. Check both servers are running: `lsof -i :8000 :3000`
2. Check backend logs: Terminal where `python api/server.py` runs
3. Check browser console: F12 → Console tab
4. Read error messages carefully
5. Check [UI_BACKEND_GUIDE.md](docs/api/UI_BACKEND_GUIDE.md) troubleshooting

### "Port already in use"
```bash
lsof -ti :8000 | xargs kill -9  # Kill backend
lsof -ti :3000 | xargs kill -9  # Kill frontend
```

### "Module not found"
```bash
# Python
source venv/bin/activate
pip install -r requirements.txt

# Node (root)
npm install

# Node (UI)
cd ui && npm install
```

### "Can't find file"
- Use [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- Check if it moved during cleanup (see [CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md))

---

## 📞 More Help

- **Full project structure**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **What was cleaned**: [CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)
- **Version history**: [CHANGELOG.md](CHANGELOG.md)
- **Main README**: [README.md](README.md)

---

**Last Updated:** November 20, 2025
**Quick Tip:** Bookmark this page for easy navigation! 🚀
