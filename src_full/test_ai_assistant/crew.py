import os
import yaml
import logging
from dotenv import load_dotenv
from typing import Dict, Any
from datetime import datetime

from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew

# MCP Server Adapters
from src_full.test_ai_assistant.tools.playwright_test_mcp import PlaywrightTestMCP
from src_full.test_ai_assistant.tools.filesystem_mcp import FilesystemMCP
from src_full.test_ai_assistant.tools.playwright_mcp import PlaywrightMCP
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/crew_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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
    logger.info(f"Initializing LLM: {model}")
    return LLM(model=model, **kwargs)


def load_yaml_config(path: str) -> Dict[str, Any]:
    """Load a YAML configuration file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@CrewBase
class PlaywrightAutomationCrew:
    """Crew definition for Playwright Automation - Planner, Generator, and Healer."""

    def __init__(self):
        logger.info("Initializing PlaywrightAutomationCrew")
        
        # Load YAML agent and task configs
        self.agents_config = load_yaml_config("src/test_ai_assistant/config/agents.yaml")
        self.tasks_config = load_yaml_config("src/test_ai_assistant/config/tasks.yaml")

        # ----------------------------
        # Initialize MCP Tool Adapters
        # ----------------------------
        logger.info("Initializing MCP Tool Adapters")

        # Playwright Test MCP
        self.playwright_test_mcp = PlaywrightTestMCP()
        self.playwright_test_tools = list(self.playwright_test_mcp.connect()) or []

        # Standard Playwright MCP
        self.playwright_mcp = PlaywrightMCP()
        self.playwright_tools = list(self.playwright_mcp.connect()) or []

        self.filesystem_mcp = FilesystemMCP()
        self.fs_tools = list(self.filesystem_mcp.connect()) or []

        # Combine all tools for agents
        self.test_tools = self.playwright_test_tools + self.playwright_tools + self.fs_tools
        logger.info(f"Total tools loaded: {len(self.test_tools)}")

        # ----------------------------
        # Initialize LLMs per role
        # ----------------------------
        logger.info("Initializing LLMs with retry logic")
        
        # CRITICAL: Use temperature 0.0 for planner to ensure deterministic behavior
        planning_llm_kwargs = dict(
            api_key=OPENAI_API_KEY,
            temperature=0.7,   # Deterministic for strict instruction following
            max_tokens=8192,   # Increased token limit
        )
        
        # Lower temperature for generation - more consistent
        generation_llm_kwargs = dict(
            api_key=OPENAI_API_KEY,
            temperature=0.2,   # Reduced from 0.3 for better consistency
            max_tokens=8192,
        )

        # Lower temperature for healing - more consistent
        healing_llm_kwargs = dict(
            api_key=OPENAI_API_KEY,
            temperature=0.2,   # Reduced from 0.3 for better consistency
            max_tokens=8192,
        )

        # Use Gemini 1.5 Pro for planning (better instruction following)
        # Use Gemini 2.5 Flash for generation/healing (faster, still good quality)
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
                model="gpt-4o-mini", 
                **healing_llm_kwargs
            )
            logger.info("LLMs initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLMs: {e}")
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
        logger.info("Creating test_planner_agent")
        
        # REDUCED TOOL SET - Only essential tools for planning
        playwright_test_selected = [t for t in self.playwright_test_tools if t.name in {
            # Core navigation and exploration
            "planner_setup_page",
            "browser_navigate",
            "browser_click",
            "browser_type",
            "browser_snapshot",
            "browser_wait_for",
            # Optional but useful
            "browser_take_screenshot",
            "browser_console_messages",
        }]

        filesystem_selected = [t for t in self.fs_tools if t.name in {
            "fs_write_file"  # Only need to write, not read
        }]

        planning_tools = playwright_test_selected + filesystem_selected
        logger.info(f"[Planning Agent] Loaded {len(planning_tools)} tools: {[t.name for t in planning_tools]}")

        return Agent(
            config=self.agents_config["test_planner_agent"],
            tools=planning_tools,
            llm=self.planning_llm,
            verbose=True,
            memory=True,
            max_iter=50,  # Increased from 25 to allow more exploration
            max_rpm=10,   # Rate limiting to avoid API issues
            max_execution_time=900,  # 15 min timeout
            allow_delegation=False,
        )

    @agent
    def test_generator_agent(self):
        """
        Test Generator Agent - Generates Playwright test scripts.
        Optimized tool selection for code generation.
        """
        logger.info("Creating test_generator_agent")

        playwright_test_selected = [t for t in self.playwright_test_tools if t.name in {
            # Core test generation tools
            "generator_setup_page",
            "generator_read_log",
            "generator_write_test",
            # Browser interaction for manual testing
            "browser_click",
            "browser_type",
            "browser_navigate",
            "browser_snapshot",
            "browser_wait_for",
            # Verification tools
            "browser_verify_element_visible",
            "browser_verify_text_visible",
            "browser_verify_value",
        }]

        filesystem_selected = [t for t in self.fs_tools if t.name in {
            "fs_read_file",
            "fs_write_file",
            "fs_list_directory",
            "fs_search_files",
        }]

        generation_tools = playwright_test_selected + filesystem_selected
        logger.info(f"[Generation Agent] Loaded {len(generation_tools)} tools: {[t.name for t in generation_tools]}")

        return Agent(
            config=self.agents_config["test_generator_agent"],
            tools=generation_tools,
            llm=self.generation_llm,
            verbose=True,
            memory=True,
            max_iter=40,
            max_rpm=10,
            max_execution_time=900,
            allow_delegation=False,
        )

    @agent
    def test_healer_agent(self):
        """
        Test Healer Agent - Debugs and fixes failing tests.
        Has access to all tools for comprehensive debugging.
        """
        logger.info("Creating test_healer_agent")
        logger.info(f"[Healer Agent] Loaded {len(self.test_tools)} tools")
        
        return Agent(
            config=self.agents_config["test_healer_agent"],
            tools=self.test_tools,
            llm=self.healing_llm,
            verbose=True,
            memory=True,
            max_iter=40,
            max_rpm=10,
            max_execution_time=1200,  # 20 min for healing
            allow_delegation=False,
        )

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
        logger.info(f"Creating plan_test_task with output: {output_file}")
        
        return Task(
            config=self.tasks_config["plan_test_task"],
            agent=self.test_planner_agent(),
            output_file=output_file,
        )

    @task
    def generate_test_task(self):
        """
        Generation task - creates Playwright test scripts.
        """
        logger.info("Creating generate_test_task")
        
        return Task(
            config=self.tasks_config["generate_test_task"],
            context=[self.plan_test_task()],  
            agent=self.test_generator_agent(),
        )

    @task
    def heal_test_task(self):
        """
        Healing task - debugs and fixes failing tests.
        """
        logger.info("Creating heal_test_task")
        
        return Task(
            config=self.tasks_config["heal_test_task"],
            context=[self.generate_test_task()],
            agent=self.test_healer_agent(),
        )

    # ----------------------------
    # Build Crews
    # ----------------------------
    def build_crew(self, agent_name: str) -> Crew:
        """
        Return a single-agent Crew instance for debugging individual components.
        """
        logger.info(f"Building crew for agent: {agent_name}")
        
        agent_task_map = {
            "test_planner_agent": (self.test_planner_agent(), self.plan_test_task()),
            "test_generator_agent": (self.test_generator_agent(), self.generate_test_task()),
            "test_healer_agent": (self.test_healer_agent(), self.heal_test_task()),
        }

        if agent_name not in agent_task_map:
            raise ValueError(f"Unknown agent '{agent_name}'. Must be one of {list(agent_task_map.keys())}")

        selected_agent, selected_task = agent_task_map[agent_name]

        return Crew(
            agents=[selected_agent],
            tasks=[selected_task],
            process=Process.sequential,
            verbose=True,
            memory=True,
            cache=True,
            max_rpm=15,
        )

    # ----------------------------
    # Full Multi-Agent Crew
    # ----------------------------
    @crew
    def full_crew(self):
        """
        Run the full sequential Playwright automation workflow:
        Planner → Generator → Healer
        """
        logger.info("Building full crew workflow")
        
        return Crew(
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
            memory=True,
            cache=True,
            max_rpm=15,
        )