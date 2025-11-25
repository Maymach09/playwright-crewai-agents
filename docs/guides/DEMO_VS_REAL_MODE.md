# Demo Mode vs Real Mode

## Overview

The Playwright AI Agents system supports two modes of operation:

- **🎭 Demo Mode**: Simulated agent execution (no API key required)
- **🚀 Real Mode**: Actual AI agent execution (requires LLM API key)

## Demo Mode

### What It Does

Demo mode runs a **simulated workflow** that demonstrates how the UI works without making any actual API calls to LLMs (OpenAI, Gemini, or Groq).

### Features

✅ **Simulated Progress**: Shows animated robots working through steps
✅ **Mock Events**: Displays realistic status messages and progress bars
✅ **No Cost**: Completely free to run, no API usage
✅ **Fast Execution**: Completes in ~20-30 seconds
✅ **No Setup**: Works immediately after starting the servers

### What It CANNOT Do

❌ Create actual test plans
❌ Generate real Playwright test code
❌ Fix actual test failures
❌ Use RAG knowledge for intelligent decision-making
❌ Learn from previous test runs

### How to Use

1. **Set mode in `.env`** (or leave default):
   ```env
   API_MODE=demo
   ```

2. **Start all services** (backend + frontend):
   ```bash
   # One command starts everything!
   ./start_all.sh
   ```
   
   Or manually:
   ```bash
   # Start backend
   python api/server.py
   
   # Start frontend (in new terminal)
   cd ui && npm start
   ```

4. **Use the UI**:
   - Enter any scenario
   - Select any agent type
   - Click "Start Workflow"
   - Watch the robots animate with simulated progress

### Use Cases

- **Testing the UI**: Verify the frontend works correctly
- **Demonstrations**: Show stakeholders how the system looks
- **Development**: Build new UI features without API costs
- **Onboarding**: Help new team members understand the workflow
- **CI/CD Testing**: Test the application in automated pipelines

---

## Real Mode

### What It Does

Real mode runs **actual AI agents** using CrewAI and your configured LLM provider. This performs real test automation work.

### Features

✅ **Actual Planning**: Creates real, usable test plans
✅ **Code Generation**: Generates working Playwright test code
✅ **Test Healing**: Analyzes and fixes real test failures
✅ **RAG Integration**: Uses knowledge base for intelligent decisions
✅ **Learning**: Stores discoveries and patterns for future use

### Requirements

⚠️ **API Key Required**: Must have at least one of:
- OpenAI API key (`OPENAI_API_KEY`)
- Google Gemini API key (`GEMINI_API_KEY`)
- Groq API key (`GROQ_API_KEY`)

⏱️ **Time**: Agents take 5-15 minutes to complete (real LLM processing)

💰 **Cost**: Incurs API usage costs from your LLM provider

### How to Use

1. **Get an API key**:
   - OpenAI: https://platform.openai.com/api-keys
   - Google Gemini: https://makersuite.google.com/app/apikey
   - Groq: https://console.groq.com/keys

2. **Create `.env` file** (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

3. **Configure your API key**:
   ```env
   # Set mode to real
   API_MODE=real
   
   # Add your API key (choose one)
   OPENAI_API_KEY=sk-...your-key-here...
   # OR
   GEMINI_API_KEY=...your-key-here...
   # OR
   GROQ_API_KEY=...your-key-here...
   ```

4. **Start all services**:
   ```bash
   ./start_all.sh
   ```

5. **Use the UI**:
   - Enter a real test scenario
   - Select agent type
   - Click "Start Workflow"
   - Wait for real agent execution (5-15 minutes)

### What Happens

When you run agents in real mode:

1. **Planner Agent**:
   - Analyzes your scenario
   - Searches RAG for similar tests
   - Creates a detailed test plan
   - Stores plan in RAG for future reuse

2. **Generator Agent**:
   - Takes the test plan
   - Searches RAG for code patterns
   - Generates Playwright TypeScript code
   - Stores patterns in RAG

3. **Healer Agent**:
   - Analyzes test failures
   - Searches RAG for similar fixes
   - Applies fixes to broken tests
   - Stores solutions in RAG

4. **Full Workflow**:
   - Runs all three agents in sequence
   - Produces complete, working test code

---

## Comparison Table

| Feature | Demo Mode | Real Mode |
|---------|-----------|-----------|
| **API Key Required** | ❌ No | ✅ Yes |
| **Execution Time** | ~30 seconds | 5-15 minutes |
| **Cost** | Free | API usage fees |
| **Real Test Plans** | ❌ No | ✅ Yes |
| **Real Code Generation** | ❌ No | ✅ Yes |
| **RAG Usage** | Display only | ✅ Full integration |
| **Learning** | ❌ No | ✅ Yes |
| **Good For** | Demos, testing, development | Production use |

---

## Switching Between Modes

### To Switch to Demo Mode

1. Edit `.env`:
   ```env
   API_MODE=demo
   ```

2. Start all services:
   ```bash
   ./start_all.sh
   ```

3. UI will open automatically at http://localhost:3000

### To Switch to Real Mode

1. Edit `.env`:
   ```env
   API_MODE=real
   OPENAI_API_KEY=sk-your-key-here
   ```

2. Start all services:
   ```bash
   ./start_all.sh
   ```

3. UI will open automatically at http://localhost:3000

### Check Current Mode

The UI shows a badge at the top:
- **🎭 DEMO MODE**: Running simulated agents
- **🚀 LIVE MODE**: Running real agents

You can also check via API:
```bash
curl http://localhost:8000/api/health
```

Response:
```json
{
  "status": "healthy",
  "mode": "demo",  // or "real"
  "api_key_configured": null,  // or true/false in real mode
  ...
}
```

---

## Troubleshooting

### Mode Not Changing

**Problem**: UI still shows old mode after changing `.env`

**Solution**: 
1. Use the restart script: `./restart_backend.sh`
2. Hard refresh browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)

### Servers Won't Start

**Problem**: `pkill` or manual start commands fail

**Solution**: Use the provided start script:
```bash
./start_all.sh
```

This script:
- Kills all processes on ports 8000 and 3000
- Waits for ports to be released
- Starts backend and frontend automatically
- Verifies both are running
- Shows current mode (demo or real)

If still having issues:
```bash
# Check what's using the ports
lsof -i :8000
lsof -i :3000

# Force kill everything
lsof -ti :8000 | xargs kill -9
lsof -ti :3000 | xargs kill -9

# Wait and restart
sleep 2
./start_all.sh
```

### Real Mode Shows "API Key Not Configured"

**Problem**: Badge shows "⚠️ API key not configured" in real mode

**Solution**:
1. Check `.env` file has valid API key
2. Restart backend server
3. Verify key is not expired/invalid

### Agents Stuck in Real Mode

**Problem**: Workflow doesn't complete after 15+ minutes

**Solution**:
1. Check backend logs for errors
2. Verify API key has credits/quota
3. Check internet connection
4. Try switching to demo mode to verify system works

### Demo Mode Boring?

**Problem**: Demo mode completes too fast, want more realistic timing

**Solution**: Demo mode is intentionally fast for development. For realistic demos to stakeholders, consider:
1. Adding slide deck before demo
2. Explaining workflow during execution
3. Using real mode with simple scenarios (faster than complex ones)

---

## Best Practices

### For Development

- **Use Demo Mode**: Fast iteration, no costs
- **Test UI changes**: Verify layouts and animations
- **Mock new features**: Simulate before implementing

### For Testing

- **Use Demo Mode**: In CI/CD pipelines
- **Verify deployments**: Check servers start correctly
- **Integration tests**: Test API endpoints without LLM calls

### For Production

- **Use Real Mode**: Get actual results
- **Monitor costs**: Track API usage
- **Set timeouts**: Handle long-running agents
- **Cache results**: Store in RAG to reduce repeated work

### For Demonstrations

- **Demo Mode for UI**: Show how it looks
- **Real Mode for Results**: Show actual capabilities
- **Prepare scenarios**: Have examples ready
- **Explain the difference**: Help audience understand modes

---

## Technical Implementation

### Backend Detection

The backend checks `API_MODE` environment variable:

```python
# api/server.py
API_MODE = os.getenv('API_MODE', 'demo').lower()

if API_MODE == 'real':
    # Use actual CrewAI agents
    result = await run_real_agent(...)
else:
    # Use mock events
    for event in mock_events:
        yield event
```

### Frontend Display

The UI fetches mode from health endpoint:

```typescript
// ui/src/App.tsx
const response = await axios.get('/api/health');
setApiMode(response.data.mode);  // 'demo' or 'real'
```

### Mock Event Generation

Demo mode uses predefined event sequences:

```python
agent_events = {
    "planner": [
        {"status": "started", "message": "🧠 Planner initialized"},
        {"status": "progress", "progress": 50, "message": "Creating plan..."},
        {"status": "completed", "progress": 100, "message": "Plan ready"}
    ],
    # ... more events
}
```

### Real Agent Execution

Real mode instantiates CrewAI:

```python
from src.test_ai_assistant.crew import TestAIAssistantCrew

crew = TestAIAssistantCrew()
result = crew.crew().kickoff(inputs={'scenario': scenario})
```

---

## Future Enhancements

Planned improvements:

- [ ] **UI Toggle**: Switch modes from UI without editing files
- [ ] **Hybrid Mode**: Use demo for some agents, real for others
- [ ] **Recording Mode**: Record real executions as demo scenarios
- [ ] **Custom Mock Events**: Define your own demo sequences
- [ ] **Cost Estimator**: Show estimated API costs before running
- [ ] **Progress Streaming**: Stream real agent thoughts in real-time

---

## Questions?

- **Can I use demo mode in production?** No, it doesn't do real work
- **Do I need both API keys?** No, just one (OpenAI, Gemini, or Groq)
- **Can I switch modes without restarting?** Not currently, restart required
- **Is demo mode data saved?** No, it's simulated and discarded
- **Do real agents use RAG?** Yes, fully integrated with knowledge base

For more help, see:
- [QUICKSTART.md](QUICKSTART.md) - Getting started guide
- [UI_BACKEND_GUIDE.md](../api/UI_BACKEND_GUIDE.md) - API documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
