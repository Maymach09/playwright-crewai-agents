import os
import json
import glob
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from src.test_ai_assistant.crew import PlaywrightAutomationCrew

# Setup logging
logger = logging.getLogger(__name__)


def read_latest_test_plan() -> Optional[str]:
    """
    Reads the most recently generated test plan from test_plan directory.
    Returns the content as a string.
    """
    try:
        test_plan_files = glob.glob("test_plan/*_test-plan.md")
        if not test_plan_files:
            logger.warning("⚠️  No test plan files found in test_plan directory")
            return None
        
        latest_test_plan = max(test_plan_files, key=os.path.getctime)
        logger.info(f"📄 Reading test plan: {latest_test_plan}")
        
        with open(latest_test_plan, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info(f"✅ Test plan loaded: {len(content)} characters")
        return content
    except Exception as e:
        logger.error(f"❌ Error reading test plan: {e}")
        return None


def prepare_inputs(
    user_input: str,
    context: Optional[str] = None,
    use_latest_test_plan: bool = False,
) -> Dict[str, Any]:
    """
    Prepare the complete input dictionary for the crew or agent.
    
    Args:
        user_input: The user's instruction/query
        context: Optional context string
        use_latest_test_plan: If True, reads and includes the latest test plan
    """
    logger.info("\n--- Preparing Inputs ---")
    logger.info(f"User Input Length: {len(user_input)} chars")
    logger.info(f"User Input Preview: {user_input[:200]}...")
    
    # If we need to use the latest test plan, read it
    if use_latest_test_plan:
        logger.info("Reading latest test plan for context...")
        test_plan_content = read_latest_test_plan()
        if test_plan_content:
            context = test_plan_content
            logger.info(f"✅ Context loaded from test plan: {len(context)} chars")
        else:
            logger.warning("⚠️  No test plan found, proceeding without context")
            context = ""
    
    # Ensure context is string
    if context is None:
        context = ""
    
    inputs = {
        "user_input": user_input,
        "context": context,
    }
    
    logger.info(f"📊 Final inputs prepared:")
    logger.info(f"  - user_input: {len(inputs['user_input'])} chars")
    logger.info(f"  - context: {len(str(inputs['context']))} chars")
    
    return inputs


def run_agent(
    agent_name: str,
    user_input: str,
    context: Optional[str] = None,
    use_latest_test_plan: bool = False,
) -> Dict[str, Any]:
    """
    Runs a specific agent (planner, generator, or healer).
    Returns structured output for downstream use or UI rendering.
    
    Args:
        agent_name: Name of the agent to run (test_planner_agent, test_generator_agent, test_healer_agent)
        user_input: The user's instruction/query
        context: Optional context string
        use_latest_test_plan: If True, includes the latest test plan as context (useful for generator)
    """
    logger.info("\n" + "="*80)
    logger.info(f"🚀 RUNNING AGENT: {agent_name}")
    logger.info("="*80)

    # Prepare inputs
    inputs = prepare_inputs(user_input, context, use_latest_test_plan)
    
    # Build and run single-agent crew
    try:
        logger.info(f"\n--- Building Crew ---")
        crew_builder = PlaywrightAutomationCrew()
        crew = crew_builder.build_crew(agent_name)
        
        logger.info(f"\n--- Starting Execution ---")
        start_time = datetime.now()
        
        result = crew.kickoff(inputs=inputs)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"\n✅ {agent_name} completed successfully in {duration:.2f} seconds")
        
        return {
            "agent": agent_name,
            "status": "success",
            "duration_seconds": duration,
            "inputs": inputs,
            "result": result,
        }
        
    except Exception as e:
        logger.error(f"\n❌ Error during {agent_name} execution: {e}", exc_info=True)
        return {
            "agent": agent_name,
            "status": "error",
            "error": str(e),
            "inputs": inputs,
        }


def run_planner(user_input: str) -> Dict[str, Any]:
    """
    Run only the test planner agent.
    
    Args:
        user_input: Description of what to test (e.g., "Test the login flow")
    
    Returns:
        Dictionary with planner results
    """
    return run_agent(
        agent_name="test_planner_agent",
        user_input=user_input,
    )


def run_generator(
    user_input: str,
    use_latest_test_plan: bool = True,
    context: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run only the test generator agent.
    
    Args:
        user_input: Which scenarios to generate (e.g., "Generate test for scenario 1.1")
        use_latest_test_plan: If True, automatically loads the latest test plan as context
        context: Optional manual context (test plan content)
    
    Returns:
        Dictionary with generator results
    """
    return run_agent(
        agent_name="test_generator_agent",
        user_input=user_input,
        context=context,
        use_latest_test_plan=use_latest_test_plan,
    )


def run_healer(
    user_input: str,
    test_location: str = "tests/",
) -> Dict[str, Any]:
    """
    Run only the test healer agent.
    
    Args:
        user_input: Instructions for healer (e.g., "Fix all failing tests")
        test_location: Path to test files or directory
    
    Returns:
        Dictionary with healer results
    """
    context = f"Test location: {test_location}"
    
    return run_agent(
        agent_name="test_healer_agent",
        user_input=user_input,
        context=context,
    )


def run_planner_then_generator(
    planner_input: str,
    generator_input: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Sequential execution: Run planner first, then generator with planner's output.
    
    Args:
        planner_input: Input for the planner agent (what to test)
        generator_input: Input for the generator agent (which scenarios to generate)
                        If None, generates tests for all scenarios in the plan
    
    Returns:
        Dictionary with both planner and generator results
    """
    logger.info("\n" + "="*80)
    logger.info("🔄 SEQUENTIAL WORKFLOW: Planner → Generator")
    logger.info("="*80)
    
    # Step 1: Run Planner
    logger.info("\n" + "▶"*40)
    logger.info("STEP 1: Running Test Planner Agent")
    logger.info("▶"*40)
    
    planner_result = run_planner(planner_input)
    
    if planner_result["status"] != "success":
        logger.error("❌ Planner failed, stopping workflow")
        return {
            "workflow": "planner_then_generator",
            "status": "failed_at_planner",
            "planner_result": planner_result,
            "generator_result": None,
        }
    
    logger.info("✅ Planner completed successfully")
    
    # Step 2: Run Generator with planner's output
    logger.info("\n" + "▶"*40)
    logger.info("STEP 2: Running Test Generator Agent")
    logger.info("▶"*40)
    
    if not generator_input:
        generator_input = """
        Generate Playwright test scripts for ALL scenarios in the test plan.
        Follow the test plan exactly and create complete, executable tests.
        """
    
    generator_result = run_generator(
        user_input=generator_input,
        use_latest_test_plan=True,  # This will read the planner's output
    )
    
    if generator_result["status"] != "success":
        logger.error("❌ Generator failed")
        return {
            "workflow": "planner_then_generator",
            "status": "failed_at_generator",
            "planner_result": planner_result,
            "generator_result": generator_result,
        }
    
    logger.info("✅ Generator completed successfully")
    
    logger.info("\n" + "="*80)
    logger.info("✅ SEQUENTIAL WORKFLOW COMPLETED SUCCESSFULLY")
    logger.info("="*80)
    
    return {
        "workflow": "planner_then_generator",
        "status": "success",
        "planner_result": planner_result,
        "generator_result": generator_result,
    }


def run_full_pipeline(
    user_input: str,
) -> Dict[str, Any]:
    """
    Runs the full sequential pipeline: Planner → Generator → Healer.
    
    Args:
        user_input: Description of what to test and generate
    
    Returns:
        Dictionary with all results
    """
    logger.info("\n" + "="*80)
    logger.info("🧩 FULL PIPELINE: Planner → Generator → Healer")
    logger.info("="*80)

    inputs = prepare_inputs(user_input)

    try:
        logger.info(f"\n--- Building Full Crew ---")
        crew_builder = PlaywrightAutomationCrew()
        crew = crew_builder.full_crew()
        
        logger.info(f"\n--- Starting Full Pipeline Execution ---")
        start_time = datetime.now()
        
        result = crew.kickoff(inputs=inputs)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"\n✅ Full pipeline completed successfully in {duration:.2f} seconds")
        
        return {
            "pipeline": "full",
            "status": "success",
            "duration_seconds": duration,
            "inputs": inputs,
            "result": result,
        }
        
    except Exception as e:
        logger.error(f"\n❌ Error during full pipeline execution: {e}", exc_info=True)
        return {
            "pipeline": "full",
            "status": "error",
            "error": str(e),
            "inputs": inputs,
        }


# -------------------------------
# CLI / Local execution
# -------------------------------
if __name__ == "__main__":
    import sys
    
    # Setup basic logging for CLI
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "="*80)
    print("Playwright Automation Crew - CLI Runner")
    print("="*80 + "\n")
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main_new.py planner        - Run only planner")
        print("  python main_new.py generator      - Run only generator (with latest test plan)")
        print("  python main_new.py healer         - Run only healer")
        print("  python main_new.py sequential     - Run planner then generator")
        print("  python main_new.py full           - Run full pipeline (all 3 agents)")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # Example 1: Run only planner
    if command == "planner":
        print("📋 Running Test Planner Agent\n")
        result = run_planner(
            user_input="Navigate to Salesforce Accounts module and create a new account with minimum required data.",
        )
        print("\n✅ Planner Result:")
        print(json.dumps(result, indent=2, default=str))
    
    # Example 2: Run only generator (with latest test plan)
    elif command == "generator":
        print("🔧 Running Test Generator Agent (using latest test plan)\n")
        result = run_generator(
             user_input='''
            Generate Playwright tests for these scenarios:
            1. Scenario 1.1: Create Account with Minimum Required Data
                        
            Follow the test plan exactly. Include all steps and proper assertions.
            ''',
            use_latest_test_plan=True,
        )
        print("\n✅ Generator Result:")
        print(json.dumps(result, indent=2, default=str))
    
    # Example 3: Run only healer
    elif command == "healer":
        print("🔧 Running Test Healer Agent\n")
        result = run_healer(
            user_input="Fix all failing tests in the tests directory.",
            test_location="tests/",
        )
        print("\n✅ Healer Result:")
        print(json.dumps(result, indent=2, default=str))
    
    # Example 4: Run planner then generator sequentially
    elif command == "sequential":
        print("🔄 Running Sequential Workflow: Planner → Generator\n")
        result = run_planner_then_generator(
            planner_input="Navigate to Salesforce and create an account with minimum data.",
            generator_input="Generate tests for all scenarios in the test plan.",
        )
        print("\n✅ Sequential Workflow Result:")
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print("✅ Planner: Success")
            print("✅ Generator: Success")
        else:
            print(f"❌ Failed at: {result['status']}")
    
    # Example 5: Run full pipeline
    elif command == "full":
        print("🚀 Running Full Pipeline: Planner → Generator → Healer\n")
        result = run_full_pipeline(
            user_input="Create and test Salesforce account creation workflow with minimum data.",
        )
        print("\n✅ Full Pipeline Result:")
        print(json.dumps(result, indent=2, default=str))
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Use: planner, generator, healer, sequential, or full")
        sys.exit(1)
