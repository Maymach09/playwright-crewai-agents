# Quick Start Guide

Get up and running with Playwright CrewAI Agents in 5 minutes.

## Prerequisites

- Python 3.13+
- Node.js 18+
- OpenAI API key
- Git

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/Maymach09/playwright-crewai-agents.git
cd playwright-crewai-agents
```

### 2. Quick Setup (Using Make)
```bash
make setup
```

Or manual setup:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install

# Install Playwright browsers
npx playwright install --with-deps chromium

# Setup environment
cp .env.example .env
```

### 3. Configure API Key
Edit `.env` and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-key-here
```

### 4. Save Authentication (For Salesforce)
```bash
npm run save-auth
```
- Browser will open
- Log into your Salesforce account
- Close browser when done
- Session saved to `auth_state.json`

## Usage

### Run Individual Agents

#### Planner Agent
Creates test plan by exploring the application:
```bash
make run-planner
# or
python src/test_ai_assistant/main.py planner
```

Output: `test_plan/{timestamp}_test-plan.md`

#### Generator Agent
Generates test code from plan:
```bash
make run-generator
# or
python src/test_ai_assistant/main.py generator
```

Output: `tests/*.spec.ts` files

#### Healer Agent
Fixes failing tests automatically:
```bash
make run-healer
# or
python src/test_ai_assistant/main.py healer
```

Output: Fixed test files

### Run Sequential Workflows

#### Planner → Generator
```bash
make run-sequential
# or
python src/test_ai_assistant/main.py sequential
```

#### Full Pipeline (Planner → Generator → Healer)
```bash
make run-full
# or
python src/test_ai_assistant/main.py full
```

## Example Workflow

### 1. Plan Tests
```bash
python src/test_ai_assistant/main.py planner
```

The planner will:
- Open browser
- Navigate to your application
- Explore features
- Create detailed test plan

**Output**: `test_plan/20251118_120000_test-plan.md`

### 2. Generate Tests
```bash
python src/test_ai_assistant/main.py generator
```

The generator will:
- Read the test plan
- Execute steps in browser
- Record Playwright code
- Save test files

**Output**: `tests/scenario-name.spec.ts`

### 3. Run Tests
```bash
npm test
```

Playwright runs your generated tests.

### 4. Fix Failures (if any)
```bash
python src/test_ai_assistant/main.py healer
```

The healer will:
- Run all tests
- Identify failures
- Apply fixes automatically
- Verify fixes work

**Output**: Fixed test files

### 5. Verify
```bash
npm test
```

Tests should now pass! ✅

## Customization

### Modify Test Scenarios

Edit the user input in `main.py`:

```python
# Example 1: Different module
result = run_planner(
    user_input="Navigate to Opportunities module and create a new opportunity"
)

# Example 2: Specific scenario
result = run_generator(
    user_input="Generate test for scenario 2.1 only"
)

# Example 3: Specific test file
result = run_healer(
    user_input="Fix tests/opportunity.spec.ts only"
)
```

### Adjust Agent Behavior

Edit configuration files:

- `src/test_ai_assistant/config/agents.yaml` - Agent personalities
- `src/test_ai_assistant/config/tasks.yaml` - Step-by-step workflows

## Troubleshooting

### "Module not found" Error
```bash
# Make sure you're in the venv
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "API key not found" Error
```bash
# Check .env file exists
ls -la .env

# Verify key is set
cat .env | grep OPENAI_API_KEY

# Make sure no spaces around =
OPENAI_API_KEY=sk-your-key-here
```

### "Browser not installed" Error
```bash
# Install Playwright browsers
npx playwright install --with-deps chromium
```

### "Auth state not found" Error
```bash
# Create auth_state.json
npm run save-auth

# Or create empty file
echo '{}' > auth_state.json
```

### Tests Fail
```bash
# Run healer to auto-fix
python src/test_ai_assistant/main.py healer

# Or check logs
tail -f logs/crew_execution_*.log
```

### Context Overflow Error
This means the task is too complex. Try:

1. Break into smaller scenarios
2. Run agents one at a time
3. Use healer on specific files only

## Viewing Logs

```bash
# Follow live logs
make logs

# Or manually
tail -f logs/crew_execution_*.log
```

## Running Tests

```bash
# Run all tests
npm test

# Run specific browser
npm run test:chromium

# Run in headed mode (see browser)
npm run test:headed

# Debug mode
npm run test:debug

# View report
npm run report
```

## Docker (Alternative)

```bash
# Build image
make docker-build

# Run container
make docker-run

# Stop container
make docker-stop
```

## Next Steps

1. **Explore Examples**: Check `sample_test_plans/` and `sample_tests/`
2. **Read Architecture**: See `ARCHITECTURE.md` for deep dive
3. **Customize**: Modify YAML configs for your needs
4. **Scale**: Use batch processing for large test suites
5. **Contribute**: See `CONTRIBUTING.md`

## Getting Help

- **Issues**: https://github.com/Maymach09/playwright-crewai-agents/issues
- **Logs**: Check `logs/` directory for detailed execution logs
- **Documentation**: See README.md and ARCHITECTURE.md

## Cost Estimate

- Planner: ~$0.002 per run
- Generator: ~$0.003-0.005 per scenario
- Healer: ~$0.009 per test
- **Total**: ~$0.02 per complete test scenario

Very affordable for development and CI/CD! 💰

Happy testing! 🎭✨
