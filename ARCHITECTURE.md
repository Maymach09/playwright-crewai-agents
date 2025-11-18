# Architecture Documentation

## Overview

Playwright CrewAI Agents is a multi-agent system that automates Playwright test creation and maintenance using AI. The system uses three specialized agents that work sequentially to plan, generate, and heal tests.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input / CLI                          │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   Main Controller                            │
│              (src/test_ai_assistant/main.py)                │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              PlaywrightAutomationCrew                        │
│             (src/test_ai_assistant/crew.py)                 │
│                                                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Planner   │→ │ Generator  │→ │   Healer   │            │
│  │   Agent    │  │   Agent    │  │   Agent    │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP Tools Layer                           │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Playwright   │  │ Playwright   │  │  Filesystem  │      │
│  │  Test MCP    │  │  Browser MCP │  │     MCP      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              External Systems                                │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ OpenAI   │  │  Browser │  │   File   │  │   Logs   │   │
│  │   API    │  │(Chromium)│  │  System  │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Agents Layer

#### Planner Agent
- **Purpose**: Explores the application and creates comprehensive test plans
- **Tools**: 6 essential tools (planner_setup_page, browser_navigate, browser_click, browser_type, browser_snapshot, browser_wait_for)
- **LLM**: GPT-4o-mini (temperature: 0.0 for deterministic output)
- **Output**: Markdown test plan with scenarios, steps, and expected results
- **Location**: `test_plan/{timestamp}_test-plan.md`

#### Generator Agent
- **Purpose**: Generates executable Playwright test code from test plans
- **Tools**: 12 tools including generator-specific tools and browser interaction
- **LLM**: GPT-4o-mini (temperature: 0.1 for slight creativity)
- **Output**: TypeScript test files in `tests/` directory
- **Key Feature**: Takes fresh browser snapshots before each action to avoid stale elements

#### Healer Agent
- **Purpose**: Automatically debugs and fixes failing tests
- **Tools**: All 75 tools available for maximum flexibility
- **LLM**: GPT-4o-mini (temperature: 0.1)
- **Strategy**: Error-message-only approach to prevent context overflow
- **Constraints**: Max 10 iterations, 600s timeout

### 2. Tools Layer (MCP)

#### Playwright Test MCP (39 tools)
- Test generation tools: `generator_setup_page`, `generator_read_log`, `generator_write_test`
- Test planning tools: `planner_setup_page`
- Test running tools: `playwright_test_run_test`
- Test debugging tools: Various verification and inspection tools

#### Playwright Browser MCP (22 tools)
- Navigation: `browser_navigate`, `browser_go_back`, `browser_go_forward`
- Interaction: `browser_click`, `browser_type`, `browser_fill_form`
- Verification: `browser_verify_element_visible`, `browser_verify_text_visible`
- Inspection: `browser_snapshot`, `browser_wait_for`

#### Filesystem MCP (14 tools)
- File operations: `fs_read_file`, `fs_write_file`, `fs_move_file`
- Directory operations: `fs_list_directory`, `fs_directory_tree`
- File search: `fs_search_files`
- File info: `fs_get_file_info`

### 3. Configuration Layer

#### agents.yaml
Defines agent personalities:
- Role (who they are)
- Goal (what they achieve)
- Backstory (context and expertise)

#### tasks.yaml
Defines workflows:
- Step-by-step instructions
- Tool usage guidelines
- Expected outputs
- Error handling rules

### 4. Orchestration Layer

#### CrewAI Framework
- **Process**: Sequential execution (Planner → Generator → Healer)
- **Memory**: Disabled to prevent stale scenario usage
- **Cache**: Disabled for fresh execution
- **Rate Limiting**: 15 RPM to avoid API limits
- **Iteration Limits**: Agent-specific (Planner: 50, Generator: 50, Healer: 10)

### 5. LLM Integration

#### OpenAI GPT-4o-mini
- **Cost**: $0.15/1M input tokens, $0.60/1M output tokens
- **Per-test cost**: ~$0.009 (healer), less for planner/generator
- **Context window**: 128K tokens
- **Speed**: 2-5s per response
- **Reliability**: High (proven in production)

#### Retry Logic
- Uses `tenacity` library
- 3 attempts with exponential backoff
- Handles transient failures gracefully

## Data Flow

### Planning Workflow
```
1. User provides scenario description
   ↓
2. Planner agent receives input
   ↓
3. Planner calls planner_setup_page (opens browser)
   ↓
4. Planner explores application:
   - Navigates pages
   - Clicks elements
   - Takes snapshots
   - Records observations
   ↓
5. Planner generates test plan (Markdown)
   ↓
6. Test plan saved to test_plan/{timestamp}_test-plan.md
```

### Generation Workflow
```
1. Generator receives test plan as context
   ↓
2. Generator calls generator_setup_page
   ↓
3. For each test scenario:
   - Takes browser snapshot (fresh element refs)
   - Executes test steps in browser
   - Clicks, types, verifies actions
   ↓
4. Generator calls generator_read_log (gets recorded code)
   ↓
5. Generator calls generator_write_test (saves .spec.ts file)
   ↓
6. Test file created in tests/ directory
```

### Healing Workflow
```
1. Healer receives test location
   ↓
2. Healer runs tests with playwright_test_run_test
   ↓
3. If test fails:
   - Extracts error message
   - Matches against COMMON FIXES patterns
   - Identifies root cause (strict mode, timeout, etc.)
   ↓
4. Healer reads test file with fs_read_file
   ↓
5. Healer applies targeted fix:
   - Updates locator (add exact: true)
   - Fixes regex pattern
   - Adjusts selector
   ↓
6. Healer writes fixed file with fs_write_file
   ↓
7. Healer re-runs test to verify fix
   ↓
8. Success or move to next failing test
```

## Context Management

### Problem
LLMs have token limits (128K for GPT-4o-mini). Complex workflows can exceed this.

### Solutions Implemented

1. **Error-Message-Only Healing**
   - Don't use browser snapshots for debugging
   - Work only from Playwright error messages
   - Reduces context from 133K to <20K tokens

2. **Strict Iteration Limits**
   - Planner: 50 iterations (needs exploration)
   - Generator: 50 iterations (needs code creation)
   - Healer: 10 iterations (strict to prevent overflow)
   - Crew level: 10 iterations global limit

3. **Tool Reduction**
   - Planner: 6 tools (focused exploration)
   - Generator: 12 tools (code generation)
   - Healer: 75 tools (needs flexibility)

4. **Fresh Snapshots**
   - Generator takes new snapshot before EACH action
   - Prevents stale element references
   - Avoids accumulating old snapshot data

5. **Disabled Memory/Cache**
   - Prevents using old scenarios
   - Forces fresh execution each time
   - Reduces context accumulation

## Error Handling

### Common Test Errors

1. **Strict Mode Violations**
   - Pattern: Multiple elements match selector
   - Fix: Add `exact: true` or use more specific selector

2. **URL Regex Patterns**
   - Pattern: Regex special chars not escaped
   - Fix: Escape dots, slashes in URL patterns

3. **Element Not Found**
   - Pattern: Element selector changed
   - Fix: Update selector based on error message

4. **Timeout Errors**
   - Pattern: Element takes too long to appear
   - Fix: Increase timeout or add explicit wait

### Recovery Strategy

- **Max 2 attempts per test**
- **Pattern matching** from COMMON FIXES library
- **Mark as fixme** if still fails after 2 attempts
- **Move to next test** to avoid getting stuck

## Performance Metrics

### Typical Execution Times
- **Planner**: 60-120s (depends on exploration depth)
- **Generator**: 30-90s per scenario
- **Healer**: 180-300s (depends on number of failures)
- **Full Pipeline**: 5-15 minutes for complete workflow

### Token Usage
- **Planner**: 10-30K tokens
- **Generator**: 15-40K tokens per scenario
- **Healer**: 15-60K tokens (optimized from 133K)

### Cost Analysis
- **Per Test (Healer)**: $0.009
- **Per Scenario (Full Pipeline)**: $0.02-0.05
- **100 Tests**: ~$0.90-2.00

## Security Considerations

1. **API Keys**: Stored in `.env`, never committed
2. **Auth State**: `auth_state.json` contains session cookies, in .gitignore
3. **Logs**: May contain URLs and element info, not committed
4. **File Access**: MCP tools have filesystem access, use in trusted environments

## Scalability

### Current Limits
- **Sweet Spot**: 1-50 tests
- **Token Window**: 128K max
- **Rate Limits**: OpenAI 15 RPM

### Scaling Strategies
1. **Batch Processing**: Run multiple agents in parallel
2. **Hybrid Approach**: LLM pattern detection + regex bulk fixes
3. **Caching**: Store common fix patterns
4. **Traditional Tools**: Use for 100+ tests

## Extension Points

### Adding New Agents
1. Define in `agents.yaml`
2. Create task in `tasks.yaml`
3. Add agent method in `crew.py`
4. Add task method in `crew.py`
5. Update `build_crew()` method

### Adding New Tools
1. Create MCP adapter in `tools/`
2. Register in `PlaywrightAutomationCrew.__init__`
3. Add to agent's tool list
4. Document in task descriptions

### Supporting New LLMs
1. Update LLM config in `crew.py`
2. Adjust temperature/parameters
3. Test with sample scenarios
4. Update documentation

## Deployment

### Local Development
```bash
python src/test_ai_assistant/main.py planner
```

### Docker Container
```bash
docker-compose up
```

### CI/CD Pipeline
- GitHub Actions workflow in `.github/workflows/ci.yml`
- Linting, testing, security checks
- Automated on push/PR

## Monitoring & Debugging

### Logs
- Location: `logs/crew_execution_{timestamp}.log`
- Level: INFO (configurable)
- Contents: Agent actions, tool calls, LLM responses

### Test Results
- Playwright reports: `playwright-report/`
- Test results: `test-results/`
- Error context: Saved in test result directories

## Future Enhancements

1. **Visual Regression Testing**: Compare screenshots
2. **API Testing**: Add API test generation
3. **Performance Testing**: Load/stress test scenarios
4. **CI Integration**: Seamless GitHub Actions integration
5. **Multi-App Support**: Beyond Salesforce
6. **Local LLM Support**: When models become capable enough
