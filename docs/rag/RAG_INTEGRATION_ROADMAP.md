# RAG Integration Roadmap

## Overview

This document outlines how to integrate our RAG system with the existing 3 agents.
We'll do it step-by-step, testing each integration before moving to the next.

## Integration Order (By Impact)

1. **Healer Agent** (BIGGEST win - 5-10x improvement)
2. **Generator Agent** (Reuse patterns, faster generation)
3. **Planner Agent** (Learn from history, better structure)

---

## Step 1: Integrate RAG with Healer Agent

### Expected Impact:
- **Speed**: 210s → 35s (6x faster)
- **Cost**: $0.009 → $0.0018 (5x cheaper)
- **Success Rate**: 65% → 90% (35% improvement)

### Changes Needed:

#### A. Update `tasks.yaml` (healing task)

**Current flow:**
```
Healer gets error → Tries to fix → 10 iterations max
```

**New flow with RAG:**
```
Healer gets error → Search RAG for similar fixes → Apply proven solution → If success, store it
```

#### B. Modify `crew.py` (healer agent setup)

Add RAG retriever as a custom tool for the Healer agent:

```python
from src.test_ai_assistant.rag import RAGRetriever

# Initialize RAG
rag_retriever = RAGRetriever()
rag_retriever.initialize_knowledge_base()

# Create custom tool for RAG search
@tool
def search_error_fixes(error_message: str) -> str:
    """Search for proven fixes for this error."""
    fixes = rag_retriever.search_fixes(error_message, n_results=3)
    
    if not fixes:
        return "No similar errors found in knowledge base."
    
    result = "Found similar error fixes:\n\n"
    for i, fix in enumerate(fixes, 1):
        result += f"{i}. {fix['content']}\n"
        result += f"   Success Rate: {fix['metadata']['success_rate']:.0%}\n"
        result += f"   Error Type: {fix['metadata']['error_type']}\n\n"
    
    return result

# Add to healer's tools
healer_tools = [
    search_error_fixes,  # NEW!
    # ... existing 75 Playwright tools
]
```

#### C. Update healing task instructions

Add RAG step to the healing workflow:

```yaml
healing:
  description: >
    1. FIRST: Search knowledge base for similar errors using search_error_fixes tool
    2. If relevant fixes found, apply the highest success rate solution
    3. If no relevant fixes or solution doesn't work, proceed with standard debugging
    4. If fix works, it will be automatically stored for future use
    
  expected_output: >
    - Error analysis
    - Solution applied (from RAG or discovered)
    - Test file status (fixed/still failing)
```

#### D. Add feedback loop

After successful heal, store the solution:

```python
# In main.py or crew.py after successful healing
if test_passed:
    rag_retriever.add_successful_fix(
        error_message=error_text,
        fix_applied=solution_description,
        error_type=classify_error(error_text),  # Simple classification
        test_file=test_file_path
    )
```

### Testing Step 1:

1. Run healer on a test with known error (e.g., locator not found)
2. Verify RAG search happens first
3. Check if proven fix is applied
4. Confirm faster healing (should be < 50s vs 210s)
5. Verify learned fix is stored

---

## Step 2: Integrate RAG with Generator Agent

### Expected Impact:
- **Speed**: 60s → 20s (3x faster code generation)
- **Quality**: More consistent, following proven patterns
- **Learning**: Stores particularly good generated code

### Changes Needed:

#### A. Add RAG pattern search to Generator

```python
@tool
def search_code_patterns(task_description: str, pattern_type: str = None) -> str:
    """Search for reusable code patterns for this task."""
    patterns = rag_retriever.search_patterns(
        task_description=task_description,
        pattern_type=pattern_type,
        n_results=2
    )
    
    if not patterns:
        return "No matching patterns found."
    
    result = "Found relevant code patterns:\n\n"
    for i, pattern in enumerate(patterns, 1):
        result += f"Pattern {i}: {pattern['metadata']['pattern_type']}\n"
        result += f"{pattern['content']}\n\n"
    
    return result
```

#### B. Update generation task

```yaml
generation:
  description: >
    1. FIRST: Search for relevant code patterns using search_code_patterns tool
    2. Use patterns as templates, adapting to specific requirements
    3. Generate complete test following Playwright best practices
    4. If patterns don't match exactly, create new code and it will be evaluated for storage
```

#### C. Store high-quality patterns

After successful generation:

```python
# Evaluate generated code quality (simple heuristics)
def should_store_pattern(code: str, test_result: dict) -> bool:
    return (
        len(code) > 50 and  # Not trivial
        test_result.get('passed', False) and  # Works
        'data-testid' in code  # Follows best practices
    )

if should_store_pattern(generated_code, test_result):
    rag_retriever.add_code_pattern(
        pattern_code=generated_code,
        pattern_type=detect_pattern_type(generated_code),
        description=test_scenario,
        tags=extract_tags(generated_code)
    )
```

### Testing Step 2:

1. Generate test for "fill form and submit"
2. Verify RAG finds form pattern
3. Check generated code uses pattern as template
4. Confirm faster generation
5. Verify good patterns are stored

---

## Step 3: Integrate RAG with Planner Agent

### Expected Impact:
- **Structure**: More consistent test plans
- **Coverage**: Better test coverage from historical learnings
- **Speed**: 30s → 15s (faster planning)

### Changes Needed:

#### A. Add test plan search

```python
@tool
def search_test_plans(scenario: str, plan_type: str = None) -> str:
    """Search for test plan templates for this scenario."""
    plans = rag_retriever.search_test_plans(
        scenario_description=scenario,
        plan_type=plan_type,
        n_results=2
    )
    
    if not plans:
        return "No matching test plans found."
    
    result = "Found relevant test plan structures:\n\n"
    for i, plan in enumerate(plans, 1):
        result += f"Plan {i}: {plan['metadata']['plan_type']}\n"
        result += f"{plan['content']}\n\n"
    
    return result
```

#### B. Update planning task

```yaml
planning:
  description: >
    1. Analyze test scenario requirements
    2. SEARCH for similar test plan structures using search_test_plans tool
    3. Use found structures as templates
    4. Create comprehensive test plan with steps
    5. Ensure all edge cases covered
```

### Testing Step 3:

1. Plan test for "user login and dashboard"
2. Verify RAG finds e2e plan structure
3. Check plan follows template
4. Confirm faster planning

---

## Implementation Timeline

### Week 1: Healer Integration
- Day 1-2: Add RAG search to healer
- Day 3-4: Test with multiple error types
- Day 5: Add feedback loop
- Day 6-7: Measure improvements

### Week 2: Generator Integration
- Day 1-2: Add pattern search to generator
- Day 3-4: Test with various scenarios
- Day 5: Add pattern storage
- Day 6-7: Measure improvements

### Week 3: Planner Integration
- Day 1-2: Add plan search to planner
- Day 3-4: Test with different test types
- Day 5-7: Full end-to-end testing

### Week 4: Optimization
- Monitor RAG growth
- Tune similarity thresholds
- Add more initial patterns
- Document findings

---

## Success Metrics

Track these metrics before and after RAG integration:

### Healer:
- ✅ Time to fix (target: 6x reduction)
- ✅ Cost per fix (target: 5x reduction)
- ✅ Success rate (target: 90%+)
- ✅ Knowledge base growth (fixes per week)

### Generator:
- ✅ Time to generate (target: 3x reduction)
- ✅ Code quality (fewer healer iterations)
- ✅ Pattern reuse rate (% using RAG patterns)
- ✅ Knowledge base growth (patterns per week)

### Planner:
- ✅ Time to plan (target: 2x reduction)
- ✅ Test coverage (edge cases found)
- ✅ Plan consistency

### Overall:
- ✅ Full pipeline time (target: 4-5x faster)
- ✅ Total cost per test (target: 4x cheaper)
- ✅ End-to-end success rate (target: 85%+)
- ✅ Total knowledge items (track growth)

---

## Code Examples

### Complete Healer Integration Example:

```python
# In crew.py

from crewai import Agent, Crew, Task
from src.test_ai_assistant.rag import RAGRetriever
from crewai.tools import tool

# Initialize RAG once
rag = RAGRetriever()
rag.initialize_knowledge_base()

# Create RAG tool for healer
@tool
def search_fixes(error: str) -> str:
    """Find proven fixes for this error."""
    fixes = rag.search_fixes(error, n_results=3)
    if not fixes:
        return "No similar errors found."
    
    return "\n".join([
        f"Fix {i}: {f['content']}\nSuccess rate: {f['metadata']['success_rate']:.0%}"
        for i, f in enumerate(fixes, 1)
    ])

# Add to healer agent
healer_agent = Agent(
    role="Test Healer",
    tools=[search_fixes, *playwright_tools],  # RAG tool + existing tools
    # ... rest of config
)

# After healing succeeds
def store_fix(error_msg: str, fix: str, test_file: str):
    error_type = "locator" if "locator" in error_msg.lower() else "timeout"
    rag.add_successful_fix(error_msg, fix, error_type, test_file)
```

---

## Monitoring RAG Growth

Add a simple monitoring script:

```python
# monitor_rag.py
from src.test_ai_assistant.rag import RAGRetriever

retriever = RAGRetriever()
stats = retriever.get_stats()

print("RAG Knowledge Base Growth:")
print(f"Test Fixes: {stats['test_fixes']['count']}")
print(f"Code Patterns: {stats['code_patterns']['count']}")
print(f"Test Plans: {stats['test_plans']['count']}")
print(f"Total Knowledge Items: {sum(s['count'] for s in stats.values())}")
```

Run weekly to track growth!

---

## Next Phase: New Agents

After RAG proven with 3 existing agents, add:

1. **Requirements Analyst**: Parse user stories
   - Uses RAG to understand common requirements patterns
   
2. **Test Strategist**: Enhanced planner
   - Uses RAG for risk analysis and prioritization
   
3. **Test Executor**: Run tests and capture results
   - Uses RAG to predict likely failures
   
4. **Reporter**: Generate reports
   - Uses RAG for report templates and insights

All will benefit from accumulated knowledge!

---

## Conclusion

✅ Clear integration roadmap
✅ Step-by-step approach
✅ Testable at each stage
✅ Measurable improvements
✅ Foundation for future agents

**Start with Healer integration for immediate 5-10x impact!** 🚀
