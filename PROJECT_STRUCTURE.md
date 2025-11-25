# Project Structure

Complete directory structure of Playwright CrewAI Agents.

## 📁 Root Directory

```
playwright_agents/
├── README.md                    # Main project documentation
├── CHANGELOG.md                 # Version history and changes
├── LICENSE                      # MIT License
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies (Playwright)
├── playwright.config.ts         # Playwright test configuration
├── Dockerfile                   # Docker container configuration
├── docker-compose.yml           # Docker compose setup
├── Makefile                     # Build and development commands
├── setup.py                     # Python package setup
└── pyproject.toml              # Python project metadata
```

## 🔧 Core Application (`src/`)

```
src/
└── test_ai_assistant/
    ├── __init__.py
    ├── main.py                  # CLI entry point
    ├── crew.py                  # CrewAI orchestration
    │
    ├── config/                  # Agent & Task Configuration
    │   ├── agents.yaml          # Agent definitions (Planner, Generator, Healer)
    │   └── tasks.yaml           # Task workflows and dependencies
    │
    ├── rag/                     # RAG System (Knowledge Management)
    │   ├── __init__.py
    │   ├── knowledge_base.py    # Seed knowledge and data
    │   ├── vector_store.py      # ChromaDB vector storage
    │   └── retriever.py         # Query and retrieval interface
    │
    └── tools/                   # Agent Tools
        ├── __init__.py
        ├── rag_tools.py         # RAG search and store tools
        ├── playwright_mcp.py    # Browser automation tools
        ├── playwright_test_mcp.py  # Playwright test tools
        └── filesystem_mcp.py    # File operation tools
```

## 🌐 Backend API (`api/`)

```
api/
└── server.py                    # FastAPI server
                                 # - REST API endpoints
                                 # - Server-Sent Events (SSE)
                                 # - Workflow management
                                 # - RAG statistics
```

**Endpoints:**
- `GET /` - Health check
- `GET /api/health` - Detailed health + RAG status
- `GET /api/rag/stats` - RAG knowledge base statistics
- `POST /api/workflow/start` - Start new workflow
- `GET /api/workflow/{id}/stream` - SSE stream of updates
- `GET /api/workflow/{id}/status` - Get workflow status
- `GET /api/workflows` - List recent workflows

## 🎨 Frontend Dashboard (`ui/`)

```
ui/
├── package.json                 # React dependencies
├── tsconfig.json               # TypeScript configuration
├── public/
│   ├── index.html              # HTML template
│   └── ...                     # Static assets
│
└── src/
    ├── index.tsx               # React entry point
    ├── App.tsx                 # Main UI component (300+ lines)
    │                           # - Robot agent cards
    │                           # - RAG stats display
    │                           # - Agent selection
    │                           # - Progress tracking
    │                           # - Activity log
    │                           # - Workflow management
    │
    ├── App.css                 # Styling and animations
    │                           # - Robot card styles
    │                           # - Bounce animations
    │                           # - Progress bars
    │                           # - Responsive layout
    │
    └── ...                     # Other React files
```

## 📚 Documentation (`docs/`)

```
docs/
├── README.md                   # Documentation index
│
├── api/                        # API and Backend
│   ├── API.md                  # FastAPI endpoints reference
│   └── UI_BACKEND_GUIDE.md     # Complete UI & backend guide
│
├── guides/                     # User Guides
│   ├── QUICKSTART.md           # Getting started
│   ├── CONTRIBUTING.md         # Contribution guidelines
│   ├── ARCHITECTURE.md         # System architecture
│   └── SECURITY.md             # Security best practices
│
└── rag/                        # RAG System
    ├── RAG_TOOLS_GUIDE.md      # RAG tools documentation
    ├── RAG_FILES_SUMMARY.md    # RAG implementation summary
    └── ...                     # Other RAG documentation
```

## 📝 Examples (`examples/`)

```
examples/
├── README.md                   # Examples index
│
├── scripts/                    # Utility Scripts
│   ├── save-auth.ts            # Save Playwright authentication
│   ├── run_healer_with_rag.py  # Run healer with RAG
│   ├── test_rag.py             # Test RAG functionality
│   ├── test_rag_integration.py # RAG integration tests
│   ├── test_rag_tools.py       # RAG tools tests
│   └── scenarios_test_accounts.txt  # Test scenarios (gitignored)
│
├── test_plans/                 # Generated Test Plans
│   └── *.md                    # Markdown test plans
│
└── sample_tests/               # Sample Playwright Tests
    └── *.spec.ts               # TypeScript test files
```

## 🧪 Tests (`tests/`)

```
tests/
└── *.spec.ts                   # Generated Playwright tests
                                # Created by Generator agent
```

## 💾 Data & Storage

```
rag_storage/                    # RAG Vector Database (gitignored)
└── chroma/                     # ChromaDB storage
    ├── test_fixes/             # Stored test fixes
    ├── code_patterns/          # Code patterns
    ├── test_plans/             # Test plans
    └── application_knowledge/  # App exploration data
```

```
logs/                           # Application Logs (gitignored)
└── crew_execution_*.log        # CrewAI execution logs
```

```
playwright-report/              # Test Reports (gitignored)
└── index.html                  # HTML test report
```

```
test-results/                   # Test Results (gitignored)
└── */                          # Individual test results
```

## 🐳 Docker

```
Dockerfile                      # Docker image definition
docker-compose.yml              # Multi-container setup
                                # - API server
                                # - Frontend
                                # - ChromaDB (optional)
```

## 🔧 Configuration Files

```
.env.example                    # Environment template
.env                            # Actual environment (gitignored)
.gitignore                      # Git ignore rules
.vscode/                        # VS Code settings (gitignored)
playwright.config.ts            # Playwright configuration
tsconfig.json                   # TypeScript config (UI)
pyproject.toml                  # Python project metadata
setup.py                        # Python package setup
Makefile                        # Build commands
uv.lock                         # UV package lock file
```

## 📦 Dependencies

### Python (`requirements.txt`)
- `crewai` - Multi-agent orchestration
- `fastapi` - Web API framework
- `uvicorn` - ASGI server
- `chromadb` - Vector database
- `playwright` - Browser automation
- `pydantic` - Data validation
- `langchain` - LLM framework
- Other utilities

### Node.js (`package.json`)
- `@playwright/test` - Playwright testing
- `typescript` - TypeScript compiler

### Node.js UI (`ui/package.json`)
- `react` - UI framework
- `react-dom` - DOM rendering
- `typescript` - Type safety
- `axios` - HTTP client
- `react-scripts` - Build tooling

## 🚫 Excluded from Git

**Environment & Secrets:**
- `.env`
- `auth_state.json`
- `examples/scripts/save-auth.ts`
- `examples/scripts/scenarios_test_accounts.txt`

**Generated Data:**
- `rag_storage/` - Learned knowledge
- `logs/` - Execution logs
- `test-results/` - Test results
- `playwright-report/` - Test reports
- `examples/test_plans/*.md` - Generated plans

**Dependencies:**
- `venv/` - Python virtual environment
- `node_modules/` - Node packages
- `__pycache__/` - Python cache

**IDE & OS:**
- `.vscode/`
- `.idea/`
- `.DS_Store`

## 📊 File Count Summary

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `src/` | Core agents & tools | 15+ Python files |
| `api/` | Backend server | 1 Python file (272 lines) |
| `ui/` | Frontend dashboard | React app (~1,328 packages) |
| `docs/` | Documentation | 10+ Markdown files |
| `examples/` | Scripts & samples | 5+ scripts, sample tests |
| `tests/` | Generated tests | Variable (user-generated) |

## 🔗 Key Files

### Most Important Files to Know

1. **`README.md`** - Start here for project overview
2. **`src/test_ai_assistant/main.py`** - CLI entry point
3. **`src/test_ai_assistant/crew.py`** - Agent orchestration
4. **`api/server.py`** - Backend API server
5. **`ui/src/App.tsx`** - Frontend UI component
6. **`docs/api/UI_BACKEND_GUIDE.md`** - Complete UI/backend guide
7. **`src/test_ai_assistant/config/agents.yaml`** - Agent definitions
8. **`src/test_ai_assistant/config/tasks.yaml`** - Task workflows
9. **`requirements.txt`** - Python dependencies
10. **`.env.example`** - Environment template

---

**Last Updated:** November 20, 2025
