# Playwright CrewAI Agents

AI-powered Playwright test automation using CrewAI multi-agent framework.

## 🤖 Agents

1. **Planner Agent** - Explores application and creates comprehensive test plans
2. **Generator Agent** - Generates executable Playwright test scripts from plans
3. **Healer Agent** - Automatically debugs and fixes failing tests

## 🚀 Features

- **Automated Test Planning** - AI explores your app and creates detailed test scenarios
- **Code Generation** - Generates production-ready Playwright TypeScript tests
- **Self-Healing Tests** - Automatically fixes common test failures
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
# Edit .env and add your API keys
```

5. Install Playwright browsers:
```bash
npx playwright install chromium
```

## 🎯 Usage

### Run Individual Agents

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

## 📁 Project Structure

```
playwright_agents/
├── src/
│   └── test_ai_assistant/
│       ├── config/
│       │   ├── agents.yaml      # Agent configurations
│       │   └── tasks.yaml       # Task workflows
│       ├── tools/
│       │   ├── playwright_mcp.py
│       │   └── filesystem_mcp.py
│       ├── crew.py              # Crew orchestration
│       └── main.py              # Entry point
├── tests/                       # Generated test files
├── test_plan/                   # Generated test plans
├── sample_tests/                # Example tests
└── playwright.config.ts         # Playwright configuration
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

1. **Planner** explores your application using browser automation
2. Creates detailed test plans with step-by-step scenarios
3. **Generator** reads the plan and executes each step in a browser
4. Captures actions and generates Playwright TypeScript code
5. **Healer** runs tests, analyzes failures, and applies fixes automatically

## 📊 Performance

- **Planner**: ~2-5 minutes per module
- **Generator**: ~10-15 minutes per scenario
- **Healer**: ~3-5 minutes per test
- **Cost**: ~$0.01 per test (with GPT-4o-mini)

## 🔒 Security

- API keys stored in `.env` (not committed)
- Auth state stored in `auth_state.json` (not committed)
- No sensitive data in logs

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## 📝 License

MIT License - see LICENSE file for details.

## 🐛 Known Issues

- Healer limited to 10 iterations to prevent context overflow
- Works best with 1-50 tests (see docs for scaling strategies)
- Local LLMs slower but cost-effective for POC

## 📚 Documentation

- [Context Management](CONTEXT_MANAGEMENT.md)
- [Healer Guide](HEALER_GUIDE.md)
- [Sample Test Plans](sample_test_plans/)

## 💡 Tips

- Start with small modules (3-5 scenarios)
- Review generated tests before running
- Use healer iteratively for complex fixes
- Consider local LLMs for POC/development
