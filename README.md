# Playwright CrewAI Agents

AI-powered Playwright test automation using CrewAI multi-agent framework.

> 🧭 **New here?** Check out [NAVIGATION.md](NAVIGATION.md) for quick links to everything you need!

## 🤖 Agents

1. **Planner Agent** - Explores application and creates comprehensive test plans
2. **Generator Agent** - Generates executable Playwright test scripts from plans
3. **Healer Agent** - Automatically debugs and fixes failing tests

## 🚀 Features

- **Automated Test Planning** - AI explores your app and creates detailed test scenarios
- **Code Generation** - Generates production-ready Playwright TypeScript tests
- **Self-Healing Tests** - Automatically fixes common test failures
- **RAG-Powered Learning** - Learns from past explorations and fixes, improving speed over time
- **Context Management** - Optimized to stay within LLM token limits
- **Multiple LLM Support** - Works with OpenAI GPT-4o-mini, Gemini, and local models

## 📋 Prerequisites

- Python 3.13+
- Node.js 18+
- Playwright
- OpenAI API key (or Gemini/local LLM)

## 🔧 Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd playwright_agents
```

2. Install Python dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Install Node dependencies:
```bash
npm install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys and set mode
```

**⚠️ Important**: Set `API_MODE=demo` for simulated agents (no API key needed) or `API_MODE=real` for actual AI agents (requires API key). See [Demo vs Real Mode Guide](docs/guides/DEMO_VS_REAL_MODE.md).

5. Install Playwright browsers:
```bash
npx playwright install chromium
```

## 🎯 Usage

### 🎭 Demo Mode (No API Key Needed)

Perfect for testing, demos, and development:

```bash
# Set demo mode in .env
echo "API_MODE=demo" > .env

# Start everything with one command!
./start_all.sh
```

Visit http://localhost:3000 to see the UI with simulated agents.

### 🚀 Real Mode (Requires API Key)

For actual test automation:

```bash
# Set real mode and API key in .env
echo "API_MODE=real" > .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# Start everything with one command!
./start_all.sh
```

**📖 For detailed mode comparison**, see [DEMO_VS_REAL_MODE.md](docs/guides/DEMO_VS_REAL_MODE.md)

### Run Individual Agents (CLI)

**Planner** - Create test plan:
```bash
python -m src.test_ai_assistant.main planner
```

**Generator** - Generate tests from plan:
```bash
python -m src.test_ai_assistant.main generator
```

**Healer** - Fix failing tests:
```bash
python -m src.test_ai_assistant.main healer
```

### Run Full Workflow

```bash
python -m src.test_ai_assistant.main full
```

### 🧠 RAG Commands

**Check RAG Knowledge Base:**
```bash
python << 'EOF'
from src.test_ai_assistant.rag.retriever import RAGRetriever

retriever = RAGRetriever()
stats = retriever.get_stats()
print('📊 RAG Knowledge Base Statistics:')
for collection, count in stats.items():
    print(f'  - {collection}: {count} items')
EOF
```

**Search Application Knowledge:**
```bash
python << 'EOF'
from src.test_ai_assistant.rag.retriever import RAGRetriever

retriever = RAGRetriever()
results = retriever.search_application_knowledge("create account", n_results=3)
for i, result in enumerate(results, 1):
    print(f"\n{i}. {result['metadata']['scenario']}")
    print(f"   Action: {result['metadata']['action']}")
    print(f"   Module: {result['metadata']['module']}")
    print(f"   Similarity: {result['similarity']}%")
EOF
```

**Clear RAG Storage (start fresh):**
```bash
rm -rf rag_storage/
# RAG will reinitialize on next run
```

## 📁 Project Structure

```
playwright_agents/
├── api/                         # Backend API server
│   └── server.py               # FastAPI application with SSE
├── ui/                          # Frontend React dashboard
│   ├── src/
│   │   ├── App.tsx             # Main UI component
│   │   └── App.css             # Styling
│   └── package.json
├── src/                         # Core agent system
│   └── test_ai_assistant/
│       ├── config/
│       │   ├── agents.yaml     # Agent configurations
│       │   └── tasks.yaml      # Task workflows
│       ├── rag/                # RAG System
│       │   ├── knowledge_base.py  # Seed knowledge
│       │   ├── vector_store.py    # ChromaDB integration
│       │   └── retriever.py       # Query interface
│       ├── tools/              # Agent tools
│       │   ├── rag_tools.py       # RAG tools
│       │   ├── playwright_mcp.py  # Browser automation
│       │   └── filesystem_mcp.py  # File operations
│       ├── crew.py             # Crew orchestration
│       └── main.py             # CLI entry point
├── docs/                        # Documentation
│   ├── api/                    # API documentation
│   ├── guides/                 # User guides
│   └── rag/                    # RAG documentation
├── examples/                    # Example scripts and tests
│   ├── scripts/                # Utility scripts
│   ├── test_plans/             # Sample test plans
│   └── sample_tests/           # Sample Playwright tests
├── tests/                       # Generated test files
├── rag_storage/                # RAG learned knowledge (gitignored)
└── playwright.config.ts        # Playwright configuration
```

## ⚙️ Configuration

### Agent Settings

Edit `src/test_ai_assistant/config/agents.yaml` to customize agent behavior.

### Task Workflows

Edit `src/test_ai_assistant/config/tasks.yaml` to modify task execution steps.

### LLM Selection

Edit `src/test_ai_assistant/crew.py` to change LLM models:

```python
# OpenAI GPT-4o-mini (default)
model="gpt-4o-mini"

# Google Gemini
model="gemini/gemini-1.5-flash"

# Local Ollama
model="ollama/qwen2.5-coder:7b"
```

## 🎓 How It Works

1. **Planner** searches RAG for cached application knowledge
   - If found: Uses existing UI flows (saves 5+ minutes)
   - If not found: Explores application and stores discoveries in RAG
2. Creates detailed test plans with step-by-step scenarios
3. **Generator** reads the plan and executes each step in a browser
4. Captures actions and generates Playwright TypeScript code
5. **Healer** searches RAG for proven fixes to similar errors
   - Applies highest success rate fixes first
   - Stores successful fixes back to RAG for future use

### 🧠 RAG Learning System

The system maintains 4 knowledge collections:
- **Application Knowledge**: UI flows, locators, navigation paths (cached explorations)
- **Test Fixes**: Proven solutions to test failures with success rates
- **Code Patterns**: Best practices and reusable patterns
- **Test Plans**: Historical test plans for reference

**Learning Loop:**
```
1st Run: Explores app → Stores in RAG (slow)
2nd Run: Finds in RAG → Skips exploration (fast!)
```

## 📊 Performance

### First Run (Cold Start - No RAG):
- **Planner**: ~5 minutes (full exploration)
- **Generator**: ~10-15 minutes per scenario
- **Healer**: ~3-5 minutes per test
- **Cost**: ~$0.01 per test (with GPT-4o-mini)

### Subsequent Runs (With RAG):
- **Planner**: ~17 seconds (RAG hit, exact match) 🚀
- **Planner**: ~3-4 minutes (RAG hit, partial match - reuses navigation)
- **Healer**: ~1-2 minutes (applies proven fixes from RAG)
- **Speedup**: 15-20x faster with RAG! ⚡

### RAG Statistics:
- Initial knowledge: 25 items (12 fixes, 5 patterns, 4 plans, 4 app flows)
- Grows with each run
- Search time: <1 second per query

## 🔒 Security

- API keys stored in `.env` (not committed)
- Auth state stored in `auth_state.json` (not committed)
- No sensitive data in logs

## 🎨 Web Dashboard (NEW!)

Launch the interactive UI to visualize agents working in real-time:

### Start Backend API Server
```bash
cd playwright_agents
source venv/bin/activate
python api/server.py
# Running on http://localhost:8000
```

### Start Frontend Dashboard
```bash
cd ui
npm start
# Running on http://localhost:3000
```

### Features
- 🤖 **3 Animated Robot Agents** - Watch Planner, Generator, and Healer work
- 📊 **Live Progress Tracking** - Real-time progress bars and status updates
- 🧠 **RAG Stats Display** - View knowledge base statistics
- ⚙️ **Agent Selection** - Run full workflow or individual agents
- 📡 **Activity Log** - See all agent events in real-time
- 🎯 **Workflow Management** - Start, monitor, and track workflows

**API Documentation:** http://localhost:8000/docs

See [UI & Backend Guide](docs/api/UI_BACKEND_GUIDE.md) for detailed instructions.

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](docs/guides/CONTRIBUTING.md) first.

## 📝 License

MIT License - see LICENSE file for details.

## 🐛 Known Issues

- Healer limited to 10 iterations to prevent context overflow
- Works best with 1-50 tests (see docs for scaling strategies)
- Local LLMs slower but cost-effective for POC

## 📚 Documentation

### Quick Links
- **[Quickstart Guide](docs/guides/QUICKSTART.md)** - Get started quickly
- **[UI & Backend Guide](docs/api/UI_BACKEND_GUIDE.md)** - Dashboard and API guide
- **[Architecture](docs/guides/ARCHITECTURE.md)** - System design
- **[API Reference](docs/api/API.md)** - Backend endpoints
- **[RAG Tools Guide](docs/rag/RAG_TOOLS_GUIDE.md)** - RAG system reference
- **[Security Guide](docs/guides/SECURITY.md)** - Security best practices

### All Documentation
See the [docs/](docs/) folder for complete documentation.
- [Healer Guide](HEALER_GUIDE.md)
- [Sample Test Plans](sample_test_plans/)

## 💡 Tips

- Start with small modules (3-5 scenarios)
- Review generated tests before running
- Use healer iteratively for complex fixes
- Consider local LLMs for POC/development
- **Let RAG learn**: Run similar scenarios multiple times to build knowledge base
- **RAG benefits compound**: Each run makes the system smarter and faster
- **Check RAG stats**: Monitor what the system has learned over time
