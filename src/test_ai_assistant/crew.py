import os
import yaml
import logging
from dotenv import load_dotenv
from typing import Dict, Any
from datetime import datetime

from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew

# MCP Server Adapters
from src.test_ai_assistant.tools.playwright_test_mcp import PlaywrightTestMCP
from src.test_ai_assistant.tools.filesystem_mcp import FilesystemMCP
from src.test_ai_assistant.tools.playwright_mcp import PlaywrightMCP
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


# Setup logging
os.makedirs('logs', exist_ok=True)
log_filename = f'logs/crew_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"Logging to: {log_filename}")

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Retry decorator for LLM initialization
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((Exception,))
)
def create_llm_with_retry(model: str, **kwargs):
    """Create LLM with automatic retry on failure."""
    logger.info(f"Initializing LLM: {model} with kwargs: {kwargs}")
    try:
        llm = LLM(model=model, **kwargs)
        logger.info(f"✅ LLM initialized successfully: {model}")
        return llm
    except Exception as e:
        logger.error(f"❌ Failed to initialize LLM {model}: {e}")
        raise


def load_yaml_config(path: str) -> Dict[str, Any]:
    """Load a YAML configuration file."""
    logger.info(f"Loading config from: {path}")
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    logger.info(f"✅ Config loaded: {list(config.keys())}")
    return config


@CrewBase
class PlaywrightAutomationCrew:
    """Crew definition for Playwright Automation - Planner, Generator, and Healer."""

    def __init__(self):
        logger.info("="*80)
        logger.info("Initializing PlaywrightAutomationCrew")
        logger.info("="*80)
        
        # Load NEW YAML agent and task configs
        self.agents_config = load_yaml_config("src/test_ai_assistant/config/agents.yaml")
        self.tasks_config = load_yaml_config("src/test_ai_assistant/config/tasks.yaml")

        # ----------------------------
        # Initialize MCP Tool Adapters
        # ----------------------------
        logger.info("\n--- Initializing MCP Tool Adapters ---")

        # Playwright Test MCP
        self.playwright_test_mcp = PlaywrightTestMCP()
        self.playwright_test_tools = list(self.playwright_test_mcp.connect()) or []
        logger.info(f"Playwright Test Tools: {len(self.playwright_test_tools)}")

        # Standard Playwright MCP
        self.playwright_mcp = PlaywrightMCP()
        self.playwright_tools = list(self.playwright_mcp.connect()) or []
        logger.info(f"Playwright Browser Tools: {len(self.playwright_tools)}")

        # Filesystem MCP
        self.filesystem_mcp = FilesystemMCP()
        self.fs_tools = list(self.filesystem_mcp.connect()) or []
        logger.info(f"Filesystem Tools: {len(self.fs_tools)}")

        # Combine all tools
        self.test_tools = self.playwright_test_tools + self.playwright_tools + self.fs_tools
        logger.info(f"✅ Total tools loaded: {len(self.test_tools)}")

        # ----------------------------
        # Initialize LLMs per role with Gemini 2.5 Flash
        # ----------------------------
        logger.info("\n--- Initializing LLMs ---")
        
        # OPTIMIZED FOR OPENAI GPT-4O-MINI
        # Planner: Temperature 0.0 for deterministic exploration and documentation
        planning_llm_kwargs = dict(
            api_key=OPENAI_API_KEY,
            temperature=0.0,      # Deterministic - follow instructions exactly
            max_tokens=4096,
        )
        
        # Generator: Temperature 0.1 for consistent code generation
        generation_llm_kwargs = dict(
            api_key=OPENAI_API_KEY,
            temperature=0.1,      # Mostly deterministic, slight creativity for edge cases
            max_tokens=4096,
        )

        # Healer: Temperature 0.1 for consistent debugging
        # Using Gemini for cost savings (large free tier)
        healing_llm_kwargs = dict(
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.1,      # Consistent fixes
            max_tokens=4096,
        )

        try:
            self.planning_llm = create_llm_with_retry(
                model="gpt-4o-mini",
                **planning_llm_kwargs
            )
            self.generation_llm = create_llm_with_retry(
                model="gpt-4o-mini",
                **generation_llm_kwargs
            )
            self.healing_llm = create_llm_with_retry(
                model="gpt-4o-mini",  # Gemini for cost savings
                **healing_llm_kwargs
            )
            logger.info("✅ All LLMs initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize LLMs: {e}")
            raise

    # ----------------------------
    # Agent Definitions
    # ----------------------------
    @agent
    def test_planner_agent(self):
        """
        Test Planner Agent - Explores application and creates test plans.
        Optimized with reduced tool set for better focus.
        """
        logger.info("\n--- Creating test_planner_agent ---")
        
        # REDUCED TOOL SET - Only essential tools for planning
        playwright_test_selected = [t for t in self.playwright_test_tools if t.name in {
            "planner_setup_page",       # Setup environment
            "browser_navigate",          # Navigate pages
            "browser_click",             # Click elements
            "browser_type",              # Type in fields
            "browser_snapshot",          # Capture page state
            "browser_wait_for",          # Wait for elements
        }]

        filesystem_selected = [t for t in self.fs_tools if t.name in {
            "fs_write_file",             # Write test plan
        }]

        planning_tools = playwright_test_selected + filesystem_selected
        logger.info(f"Planning Agent Tools ({len(planning_tools)}): {[t.name for t in planning_tools]}")

        agent = Agent(
            config=self.agents_config["test_planner_agent"],
            tools=planning_tools,
            llm=self.planning_llm,
            verbose=True,
            memory=True,
            max_iter=50,              # Allow thorough exploration
            max_rpm=10,               # Rate limiting
            max_execution_time=900,   # 15 min timeout
            allow_delegation=False,
        )
        
        logger.info("✅ test_planner_agent created")
        return agent

    @agent
    def test_generator_agent(self):
        """
        Test Generator Agent - Generates Playwright test scripts.
        Optimized tool selection for code generation.
        """
        logger.info("\n--- Creating test_generator_agent ---")

        playwright_test_selected = [t for t in self.playwright_test_tools if t.name in {
            # Core test generation tools
            "generator_setup_page",      # Setup test environment
            "generator_read_log",        # Read recorded actions
            "generator_write_test",      # Write test file
            # Browser interaction for executing test steps
            "browser_click",
            "browser_type",
            "browser_fill_form",
            "browser_navigate",
            "browser_snapshot",
            "browser_wait_for",
            # Verification tools
            "browser_verify_element_visible",
            "browser_verify_text_visible",
            "browser_verify_value",
        }]

        filesystem_selected = [t for t in self.fs_tools if t.name in {
            "fs_read_file",              # Read test plan
            "fs_write_file",             # Alternative write method
            "fs_list_directory",         # Check existing tests
        }]

        generation_tools = playwright_test_selected + filesystem_selected
        logger.info(f"Generation Agent Tools ({len(generation_tools)}): {[t.name for t in generation_tools]}")

        agent = Agent(
            config=self.agents_config["test_generator_agent"],
            tools=generation_tools,
            llm=self.generation_llm,
            verbose=True,
            memory=True,
            max_iter=50,              # Enough for complex scenarios
            max_rpm=10,
            max_execution_time=900,   # 15 min timeout
            allow_delegation=False,
        )
        
        logger.info("✅ test_generator_agent created")
        return agent

    @agent
    def test_healer_agent(self):
        """
        Test Healer Agent - Debugs and fixes failing tests.
        Has access to all tools for comprehensive debugging.
        """
        logger.info("\n--- Creating test_healer_agent ---")
        
        # Healer gets ALL tools for maximum debugging capability
        logger.info(f"Healer Agent Tools ({len(self.test_tools)}): All tools available")
        
        agent = Agent(
            config=self.agents_config["test_healer_agent"],
            tools=self.test_tools,
            llm=self.healing_llm,
            verbose=True,
            memory=True,
            max_iter=10,              # Strict limit to prevent context overflow
            max_rpm=10,
            max_execution_time=600,   # 10 min for healing (reduced)
            allow_delegation=False,
        )
        
        logger.info("✅ test_healer_agent created")
        return agent

    # ----------------------------
    # Task Definitions
    # ----------------------------
    @task
    def plan_test_task(self):
        """
        Planning task - creates comprehensive test plan.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"test_plan/{timestamp}_test-plan.md"
        logger.info(f"\n--- Creating plan_test_task ---")
        logger.info(f"Output file: {output_file}")
        
        task_obj = Task(
            config=self.tasks_config["plan_test_task"],
            agent=self.test_planner_agent(),
            output_file=output_file,
        )
        
        logger.info("✅ plan_test_task created")
        return task_obj

    @task
    def generate_test_task(self):
        """
        Generation task - creates Playwright test scripts.
        """
        logger.info("\n--- Creating generate_test_task ---")
        logger.info("Context: Will receive output from plan_test_task")
        
        task_obj = Task(
            config=self.tasks_config["generate_test_task"],
            context=[self.plan_test_task()],  # Receives planner output
            agent=self.test_generator_agent(),
        )
        
        logger.info("✅ generate_test_task created")
        return task_obj

    @task
    def heal_test_task(self):
        """
        Healing task - debugs and fixes failing tests.
        """
        logger.info("\n--- Creating heal_test_task ---")
        logger.info("Context: Will receive output from generate_test_task")
        
        task_obj = Task(
            config=self.tasks_config["heal_test_task"],
            context=[self.generate_test_task()],  # Receives generator output
            agent=self.test_healer_agent(),
        )
        
        logger.info("✅ heal_test_task created")
        return task_obj

    # ----------------------------
    # Build Crews
    # ----------------------------
    def build_crew(self, agent_name: str) -> Crew:
        """
        Return a single-agent Crew instance for running individual agents.
        """
        logger.info("\n" + "="*80)
        logger.info(f"Building crew for agent: {agent_name}")
        logger.info("="*80)
        
        agent_task_map = {
            "test_planner_agent": (self.test_planner_agent(), self.plan_test_task()),
            "test_generator_agent": (self.test_generator_agent(), self.generate_test_task()),
            "test_healer_agent": (self.test_healer_agent(), self.heal_test_task()),
        }

        if agent_name not in agent_task_map:
            raise ValueError(f"Unknown agent '{agent_name}'. Must be one of {list(agent_task_map.keys())}")

        selected_agent, selected_task = agent_task_map[agent_name]

        crew = Crew(
            agents=[selected_agent],
            tasks=[selected_task],
            process=Process.sequential,
            verbose=True,
            memory=False,  # Disable memory to prevent using old scenarios
            cache=False,   # Disable cache to prevent stale data
            max_rpm=15,
            max_iter=10,   # Limit iterations to prevent context overflow
        )
        
        logger.info(f"✅ Crew built successfully for {agent_name}")
        return crew

    # ----------------------------
    # Full Multi-Agent Crew
    # ----------------------------
    @crew
    def full_crew(self):
        """
        Run the full sequential Playwright automation workflow:
        Planner → Generator → Healer
        """
        logger.info("\n" + "="*80)
        logger.info("Building full crew workflow: Planner → Generator → Healer")
        logger.info("="*80)
        
        crew_obj = Crew(
            agents=[
                self.test_planner_agent(),
                self.test_generator_agent(),
                self.test_healer_agent(),
            ],
            tasks=[
                self.plan_test_task(),
                self.generate_test_task(),
                self.heal_test_task(),
            ],
            process=Process.sequential,
            verbose=True,
            memory=False,  # Disable memory to prevent using old scenarios
            cache=False,   # Disable cache to prevent stale data
            max_rpm=15,
            max_iter=10,   # Limit iterations to prevent context overflow
        )
        
        logger.info("✅ Full crew built successfully")
        return crew_obj
