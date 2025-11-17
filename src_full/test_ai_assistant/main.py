import os
import json
import glob
import tempfile
from typing import Dict, Any, Optional

from src_full.test_ai_assistant.crew import PlaywrightAutomationCrew


def read_context_files(uploaded_files) -> Dict[str, str]:
    """
    Reads uploaded file contents into a dictionary.
    Works with file-like objects (e.g., from Streamlit uploads).
    """
    context_data = {}
    if not uploaded_files:
        return context_data

    for file in uploaded_files:
        try:
            file_bytes = file.read()
            context_data[file.name] = file_bytes.decode("utf-8", errors="ignore")
        except Exception as e:
            context_data[file.name] = f"Error reading file: {e}"
    return context_data


def read_latest_test_plan() -> Optional[str]:
    """
    Reads the most recently generated test plan from test_plan directory.
    Returns the content as a string.
    """
    try:
        test_plan_files = glob.glob("test_plan/*_test-plan.md")
        if not test_plan_files:
            print("⚠️  No test plan files found in test_plan directory")
            return None
        
        latest_test_plan = max(test_plan_files, key=os.path.getctime)
        print(f"📄 Reading test plan: {latest_test_plan}")
        
        with open(latest_test_plan, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    except Exception as e:
        print(f"❌ Error reading test plan: {e}")
        return None


def prepare_inputs(
    user_input: str,
    uploaded_files: Optional[list] = None,
    extra_inputs: Optional[Dict[str, Any]] = None,
    use_latest_test_plan: bool = False,
) -> Dict[str, Any]:
    """
    Prepare the complete input dictionary for the crew or agent.
    
    Args:
        user_input: The user's instruction/query
        uploaded_files: Optional list of uploaded files
        extra_inputs: Optional dictionary of additional inputs
        use_latest_test_plan: If True, reads and includes the latest test plan
    """
    # Read uploaded files context
    context = read_context_files(uploaded_files) if uploaded_files else {}
    
    # If we need to use the latest test plan, read it
    if use_latest_test_plan:
        test_plan_content = read_latest_test_plan()
        if test_plan_content:
            # Store test plan content as a string, not dict
            context = test_plan_content
        else:
            print("⚠️  No test plan found, proceeding without context")
            context = ""
    
    inputs = {
        "user_input": user_input,
        "context": context,
    }
    
    if extra_inputs:
        inputs.update(extra_inputs)
    
    return inputs


def run_agent(
    agent_name: str,
    user_input: str,
    uploaded_files: Optional[list] = None,
    extra_inputs: Optional[Dict[str, Any]] = None,
    use_latest_test_plan: bool = False,
) -> Dict[str, Any]:
    """
    Runs a specific agent (planner, generator, or healer).
    Returns structured output for downstream use or UI rendering.
    
    Args:
        agent_name: Name of the agent to run (test_planner_agent, test_generator_agent, test_healer_agent)
        user_input: The user's instruction/query
        uploaded_files: Optional list of uploaded files
        extra_inputs: Optional dictionary of additional inputs
        use_latest_test_plan: If True, includes the latest test plan as context (useful for generator)
    """
    print(f"🚀 Running agent: {agent_name}")

    inputs = prepare_inputs(user_input, uploaded_files, extra_inputs, use_latest_test_plan)
    
    print(f"📝 User Input: {user_input[:100]}...")
    if use_latest_test_plan and inputs.get('context'):
        print(f"📋 Context: Using test plan ({len(str(inputs['context']))} chars)")
    
    # Build and run single-agent crew
    crew_builder = PlaywrightAutomationCrew()
    crew = crew_builder.build_crew(agent_name)

    try:
        result = crew.kickoff(inputs=inputs)
        print(f"✅ {agent_name} completed successfully")
    except Exception as e:
        print(f"❌ Error during {agent_name} execution: {e}")
        result = str(e)

    return {
        "agent": agent_name,
        "inputs": inputs,
        "result": result,
    }


def run_planner_then_generator(
    planner_input: str,
    generator_input: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Sequential execution: Run planner first, then generator with planner's output.
    
    Args:
        planner_input: Input for the planner agent
        generator_input: Input for the generator agent (defaults to generic instruction)
    """
    print("🔄 Running sequential workflow: Planner → Generator")
    
    # Step 1: Run Planner
    print("\n" + "="*80)
    print("STEP 1: Running Test Planner Agent")
    print("="*80)
    planner_result = run_agent(
        agent_name="test_planner_agent",
        user_input=planner_input,
    )
    
    # Step 2: Run Generator with planner's output
    print("\n" + "="*80)
    print("STEP 2: Running Test Generator Agent")
    print("="*80)
    
    if not generator_input:
        generator_input = """
        Generate Playwright test scripts based on the test plan.
        Create complete, executable tests for the key scenarios identified in the plan.
        Follow Playwright best practices and include proper assertions.
        """
    
    generator_result = run_agent(
        agent_name="test_generator_agent",
        user_input=generator_input,
        use_latest_test_plan=True,  # This will read the planner's output
    )
    
    return {
        "workflow": "planner_then_generator",
        "planner_result": planner_result,
        "generator_result": generator_result,
    }


def run_full_crew(
    user_input: str,
    uploaded_files: Optional[list] = None,
    extra_inputs: Optional[Dict[str, Any]] = None,
    save_output: bool = True,
) -> Dict[str, Any]:
    """
    Runs the full sequential pipeline: Planner → Generator → Healer.
    Optionally saves the output to a temp file for inspection.
    """
    print("🧩 Starting full Playwright automation pipeline (Planner → Generator → Healer)...")

    inputs = prepare_inputs(user_input, uploaded_files, extra_inputs)

    # Initialize the full crew
    crew_builder = PlaywrightAutomationCrew()
    crew = crew_builder.full_crew()

    try:
        result = crew.kickoff(inputs=inputs)
        print("✅ Full crew completed successfully")
    except Exception as e:
        print(f"❌ Full crew execution failed: {e}")
        return {"error": str(e)}

    # Optionally save result for later review
    saved_file = None
    if save_output:
        tmp_dir = tempfile.gettempdir()
        saved_file = os.path.join(tmp_dir, "crew_full_result.json")
        with open(saved_file, "w", encoding="utf-8") as f:
            json.dump(str(result), f, indent=2)
        print(f"📂 Full crew result saved to: {saved_file}")

    return {
        "pipeline": "full_crew",
        "inputs": inputs,
        "result": result,
        "saved_output": saved_file,
    }


# -------------------------------
# Example CLI / Local execution
# -------------------------------
if __name__ == "__main__":
    import sys
    
    # Example 1: Run only planner
    if len(sys.argv) > 1 and sys.argv[1] == "planner":
        print("\n📋 Running Test Planner Agent Only\n")
        result = run_agent(
            agent_name="test_planner_agent",
            user_input="Navigate to Salesforce accounts module and create a new account with minimum required data.",
        )
        print("\n✅ Planner Output:\n", json.dumps(result, indent=2, default=str))
    
    # Example 2: Run only generator (with latest test plan)
    elif len(sys.argv) > 1 and sys.argv[1] == "generator":
        print("\n🔧 Running Test Generator Agent Only (using latest test plan)\n")
        result = run_agent(
            agent_name="test_generator_agent",
            user_input="Generate Playwright test scripts for the key scenarios in the test plan.",
            use_latest_test_plan=True,  # This reads the planner's output
        )
        print("\n✅ Generator Output:\n", json.dumps(result, indent=2, default=str))
    
    # Example 3: Run planner then generator sequentially
    elif len(sys.argv) > 1 and sys.argv[1] == "sequential":
        print("\n🔄 Running Sequential Workflow: Planner → Generator\n")
        result = run_planner_then_generator(
            planner_input="Navigate to Salesforce accounts and create account with minimum data.",
            generator_input="Generate complete Playwright tests for the scenarios in the test plan.",
        )
        print("\n✅ Sequential Workflow Complete")
        print(f"Planner Status: {'✅ Success' if result['planner_result'] else '❌ Failed'}")
        print(f"Generator Status: {'✅ Success' if result['generator_result'] else '❌ Failed'}")
    
    # Example 4: Run full crew pipeline
    else:
        print("\n🚀 Running Full Crew Pipeline (Planner → Generator → Healer)\n")
        result = run_full_crew(
            user_input="Create and test Salesforce account creation workflow with minimum data.",
        )
        print("\n✅ Full Crew Output:\n", json.dumps(result, indent=2, default=str))