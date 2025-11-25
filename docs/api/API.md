# API Documentation

Complete reference for using Playwright CrewAI Agents programmatically.

## Installation

```bash
pip install -e .
```

## Basic Usage

```python
from src.test_ai_assistant.main import (
    run_planner,
    run_generator,
    run_healer,
    run_planner_then_generator,
    run_full_pipeline
)

# Run planner
result = run_planner("Navigate to Accounts and create new account")

# Run generator
result = run_generator("Generate tests for scenario 1.1")

# Run healer
result = run_healer("Fix all failing tests")

# Run pipeline
result = run_full_pipeline("Create account workflow tests")
```

## API Reference

### run_planner()

Creates test plan by exploring the application.

**Signature:**
```python
def run_planner(user_input: str) -> Dict[str, Any]
```

**Parameters:**
- `user_input` (str): Description of what to test

**Returns:**
Dictionary with:
- `agent` (str): "test_planner_agent"
- `status` (str): "success" or "error"
- `duration_seconds` (float): Execution time
- `inputs` (dict): Input parameters used
- `result` (CrewOutput): Test plan content

**Example:**
```python
result = run_planner(
    user_input="Navigate to Salesforce Opportunities module and verify key features"
)

if result["status"] == "success":
    print(f"Test plan created in {result['duration_seconds']}s")
    print(f"Plan: {result['result']}")
```

**Output File:**
`test_plan/{timestamp}_test-plan.md`

### run_generator()

Generates Playwright test code from test plan.

**Signature:**
```python
def run_generator(
    user_input: str,
    use_latest_test_plan: bool = True,
    context: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `user_input` (str): Which scenarios to generate
- `use_latest_test_plan` (bool): Auto-load latest plan. Default: True
- `context` (str, optional): Manual test plan content

**Returns:**
Dictionary with:
- `agent` (str): "test_generator_agent"
- `status` (str): "success" or "error"
- `duration_seconds` (float): Execution time
- `inputs` (dict): Input parameters used
- `result` (CrewOutput): Generation result

**Example:**
```python
# Use latest test plan
result = run_generator(
    user_input="Generate tests for scenarios 1.1 and 1.2"
)

# Provide manual context
with open("my_test_plan.md") as f:
    plan = f.read()

result = run_generator(
    user_input="Generate all tests",
    use_latest_test_plan=False,
    context=plan
)
```

**Output Files:**
`tests/*.spec.ts` files

### run_healer()

Automatically fixes failing tests.

**Signature:**
```python
def run_healer(
    user_input: str,
    test_location: str = "tests/"
) -> Dict[str, Any]
```

**Parameters:**
- `user_input` (str): Instructions for healer
- `test_location` (str): Path to tests. Default: "tests/"

**Returns:**
Dictionary with:
- `agent` (str): "test_healer_agent"
- `status` (str): "success" or "error"
- `duration_seconds` (float): Execution time
- `inputs` (dict): Input parameters used
- `result` (CrewOutput): Healing result

**Example:**
```python
# Fix all tests
result = run_healer(
    user_input="Fix all failing tests in the tests directory"
)

# Fix specific test
result = run_healer(
    user_input="Fix tests/account.spec.ts only",
    test_location="tests/account.spec.ts"
)

# Fix tests in subdirectory
result = run_healer(
    user_input="Fix all account tests",
    test_location="tests/accounts/"
)
```

**Output:**
Modified test files with fixes applied

### run_planner_then_generator()

Sequential execution: Planner → Generator.

**Signature:**
```python
def run_planner_then_generator(
    planner_input: str,
    generator_input: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `planner_input` (str): Input for planner
- `generator_input` (str, optional): Input for generator. Default: "Generate all scenarios"

**Returns:**
Dictionary with:
- `workflow` (str): "planner_then_generator"
- `status` (str): "success", "failed_at_planner", or "failed_at_generator"
- `planner_result` (dict): Planner execution result
- `generator_result` (dict): Generator execution result or None

**Example:**
```python
result = run_planner_then_generator(
    planner_input="Navigate to Leads module",
    generator_input="Generate tests for all lead scenarios"
)

if result["status"] == "success":
    print("✅ Planner and Generator completed")
    print(f"Planner took: {result['planner_result']['duration_seconds']}s")
    print(f"Generator took: {result['generator_result']['duration_seconds']}s")
```

### run_full_pipeline()

Full workflow: Planner → Generator → Healer.

**Signature:**
```python
def run_full_pipeline(user_input: str) -> Dict[str, Any]
```

**Parameters:**
- `user_input` (str): Description of full workflow

**Returns:**
Dictionary with:
- `pipeline` (str): "full"
- `status` (str): "success" or "error"
- `duration_seconds` (float): Total execution time
- `inputs` (dict): Input parameters used
- `result` (CrewOutput): Pipeline result

**Example:**
```python
result = run_full_pipeline(
    user_input="Create comprehensive tests for account creation workflow"
)

if result["status"] == "success":
    print(f"Full pipeline completed in {result['duration_seconds']}s")
    print(f"Tests created and verified")
```

## Advanced Usage

### Direct Crew Access

```python
from src.test_ai_assistant.crew import PlaywrightAutomationCrew

# Initialize crew
crew_builder = PlaywrightAutomationCrew()

# Build specific agent crew
planner_crew = crew_builder.build_crew("test_planner_agent")

# Execute
inputs = {"user_input": "Test login flow", "context": ""}
result = planner_crew.kickoff(inputs=inputs)
```

### Custom Agent Configuration

```python
import yaml

# Load and modify config
with open("src/test_ai_assistant/config/agents.yaml") as f:
    agents = yaml.safe_load(f)

# Modify agent
agents["test_planner_agent"]["role"] = "Custom Test Planner"
agents["test_planner_agent"]["goal"] = "Custom goal"

# Save
with open("src/test_ai_assistant/config/agents.yaml", "w") as f:
    yaml.dump(agents, f)

# Use modified config
from src.test_ai_assistant.crew import PlaywrightAutomationCrew
crew = PlaywrightAutomationCrew()  # Loads modified config
```

### Custom Task Workflows

```python
import yaml

# Load and modify tasks
with open("src/test_ai_assistant/config/tasks.yaml") as f:
    tasks = yaml.safe_load(f)

# Modify task description
tasks["plan_test_task"]["description"] = """
Custom workflow:
1. Custom step 1
2. Custom step 2
"""

# Save
with open("src/test_ai_assistant/config/tasks.yaml", "w") as f:
    yaml.dump(tasks, f)
```

## Error Handling

```python
from src.test_ai_assistant.main import run_healer

try:
    result = run_healer("Fix all tests")
    
    if result["status"] == "error":
        print(f"Error: {result.get('error')}")
        # Handle error
    else:
        print(f"Success! Duration: {result['duration_seconds']}s")
        
except Exception as e:
    print(f"Unexpected error: {e}")
    # Log, retry, or handle
```

## Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('my_custom.log'),
        logging.StreamHandler()
    ]
)

# Run agent (logs will be captured)
result = run_planner("Test workflow")
```

## Integration Examples

### CI/CD Pipeline

```python
#!/usr/bin/env python
"""CI/CD integration script"""

from src.test_ai_assistant.main import run_full_pipeline
import sys

def main():
    # Run full pipeline
    result = run_full_pipeline(
        user_input="Generate and validate all critical path tests"
    )
    
    # Check result
    if result["status"] == "success":
        print("✅ Test generation and validation complete")
        sys.exit(0)
    else:
        print("❌ Pipeline failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Web API

```python
from flask import Flask, request, jsonify
from src.test_ai_assistant.main import run_planner, run_generator, run_healer

app = Flask(__name__)

@app.route('/api/plan', methods=['POST'])
def plan_tests():
    data = request.json
    result = run_planner(data['scenario'])
    return jsonify(result)

@app.route('/api/generate', methods=['POST'])
def generate_tests():
    data = request.json
    result = run_generator(data['scenario'])
    return jsonify(result)

@app.route('/api/heal', methods=['POST'])
def heal_tests():
    result = run_healer("Fix all failing tests")
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)
```

### Batch Processing

```python
from src.test_ai_assistant.main import run_planner_then_generator
from concurrent.futures import ThreadPoolExecutor
import json

# Define scenarios
scenarios = [
    "Account creation workflow",
    "Lead conversion workflow",
    "Opportunity management",
    "Contact management"
]

def process_scenario(scenario):
    result = run_planner_then_generator(
        planner_input=scenario,
        generator_input=f"Generate all tests for {scenario}"
    )
    return {
        "scenario": scenario,
        "status": result["status"],
        "duration": result.get("planner_result", {}).get("duration_seconds", 0) +
                   result.get("generator_result", {}).get("duration_seconds", 0)
    }

# Process in parallel (be mindful of API rate limits)
with ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(process_scenario, scenarios))

# Save results
with open("batch_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Processed {len(scenarios)} scenarios")
```

## Configuration

### Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Access configuration
openai_key = os.getenv("OPENAI_API_KEY")
log_level = os.getenv("LOG_LEVEL", "INFO")
max_iter = int(os.getenv("MAX_ITERATIONS", "10"))
```

### Runtime Configuration

```python
from src.test_ai_assistant.crew import PlaywrightAutomationCrew

crew = PlaywrightAutomationCrew()

# Access agents
planner = crew.test_planner_agent()
generator = crew.test_generator_agent()
healer = crew.test_healer_agent()

# Access tasks
plan_task = crew.plan_test_task()
generate_task = crew.generate_test_task()
heal_task = crew.heal_test_task()

# Access tools
print(f"Total tools: {len(crew.test_tools)}")
print(f"Playwright Test tools: {len(crew.playwright_test_tools)}")
print(f"Browser tools: {len(crew.playwright_tools)}")
print(f"Filesystem tools: {len(crew.fs_tools)}")
```

## Type Hints

```python
from typing import Dict, Any, Optional

def my_test_function(
    scenario: str,
    use_healer: bool = True
) -> Dict[str, Any]:
    """
    Custom test generation function.
    
    Args:
        scenario: Test scenario description
        use_healer: Whether to run healer after generation
    
    Returns:
        Result dictionary with status and details
    """
    from src.test_ai_assistant.main import (
        run_planner_then_generator,
        run_healer
    )
    
    # Generate tests
    result = run_planner_then_generator(scenario)
    
    if use_healer and result["status"] == "success":
        # Fix any issues
        heal_result = run_healer("Fix all tests")
        result["heal_result"] = heal_result
    
    return result
```

## Best Practices

1. **Error Handling**: Always check `result["status"]`
2. **Logging**: Enable logging for debugging
3. **Rate Limits**: Be mindful of OpenAI API limits (15 RPM)
4. **Context Size**: Keep scenarios focused to avoid token limits
5. **Batch Processing**: Use `max_workers=2` to avoid rate limits
6. **Testing**: Test in development before production use
7. **Monitoring**: Log execution times and costs

## Performance Tips

1. **Use Sequential Workflows**: Better than separate calls
2. **Reuse Test Plans**: Generate multiple tests from one plan
3. **Specific Healing**: Target specific files instead of all tests
4. **Parallel Execution**: Use ThreadPoolExecutor for independent scenarios
5. **Cache Results**: Store generated tests for reuse

## Troubleshooting

See [QUICKSTART.md](QUICKSTART.md) for common issues and solutions.

## Support

- Issues: https://github.com/Maymach09/playwright-crewai-agents/issues
- Documentation: See README.md and ARCHITECTURE.md
