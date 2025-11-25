"""
FastAPI server for Playwright CrewAI Agents
Provides REST API and Server-Sent Events for real-time agent updates
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, AsyncGenerator
import asyncio
import json
import logging
import os
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.test_ai_assistant.rag.retriever import RAGRetriever

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get API mode from environment
API_MODE = os.getenv('API_MODE', 'demo').lower()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Playwright AI Agents API",
    description="AI-powered test automation with real-time updates",
    version="2.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class WorkflowRequest(BaseModel):
    scenario: str
    agent: Optional[str] = "planner"  # planner, generator, healer, or full
    test_file: Optional[str] = None  # For healer: which test file to fix
    test_plan: Optional[str] = None  # For generator: which test plan to use

class WorkflowResponse(BaseModel):
    workflow_id: str
    status: str
    message: str

class RAGStatsResponse(BaseModel):
    total_items: int
    test_fixes: int
    code_patterns: int
    test_plans: int
    application_knowledge: int
    cache_hit_rate: Optional[float] = None

# In-memory storage for active workflows (use Redis in production)
active_workflows = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Playwright AI Agents API",
        "version": "2.0.0",
        "mode": API_MODE,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    try:
        # Check if RAG is accessible
        retriever = RAGRetriever()
        stats = retriever.get_stats()
        
        # Check API mode and key configuration
        api_key_configured = bool(os.getenv('OPENAI_API_KEY')) or bool(os.getenv('GEMINI_API_KEY')) or bool(os.getenv('GROQ_API_KEY'))
        
        # Calculate total items (stats contains dict with "count" key)
        total_items = 0
        if stats:
            for value in stats.values():
                if isinstance(value, dict) and 'count' in value:
                    total_items += value['count']
                elif isinstance(value, int):
                    total_items += value
        
        return {
            "status": "healthy",
            "mode": API_MODE,
            "api_key_configured": api_key_configured if API_MODE == 'real' else None,
            "rag_status": "connected",
            "rag_items": total_items,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/rag/stats")
async def get_rag_stats() -> RAGStatsResponse:
    """Get RAG knowledge base statistics"""
    try:
        retriever = RAGRetriever()
        stats = retriever.get_stats()
        
        # Extract counts from the dict structure
        test_fixes = stats.get('test_fixes', {}).get('count', 0) if isinstance(stats.get('test_fixes'), dict) else stats.get('test_fixes', 0)
        code_patterns = stats.get('code_patterns', {}).get('count', 0) if isinstance(stats.get('code_patterns'), dict) else stats.get('code_patterns', 0)
        test_plans = stats.get('test_plans', {}).get('count', 0) if isinstance(stats.get('test_plans'), dict) else stats.get('test_plans', 0)
        application_knowledge = stats.get('application_knowledge', {}).get('count', 0) if isinstance(stats.get('application_knowledge'), dict) else stats.get('application_knowledge', 0)
        
        total = test_fixes + code_patterns + test_plans + application_knowledge
        
        return RAGStatsResponse(
            total_items=total,
            test_fixes=test_fixes,
            code_patterns=code_patterns,
            test_plans=test_plans,
            application_knowledge=application_knowledge,
            cache_hit_rate=None  # TODO: Calculate from recent runs
        )
    except Exception as e:
        logger.error(f"Error getting RAG stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test-plans")
async def get_test_plans():
    """Get list of available test plan files"""
    try:
        test_plan_dir = Path("test_plan")
        if not test_plan_dir.exists():
            return {"test_plans": []}
        
        test_plans = []
        for file in sorted(test_plan_dir.glob("*.md"), reverse=True):  # Most recent first
            stat = file.stat()
            test_plans.append({
                "filename": file.name,
                "path": str(file),
                "relative_path": f"test_plan/{file.name}",
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "size": stat.st_size
            })
        
        return {"test_plans": test_plans}
    except Exception as e:
        logger.error(f"Error getting test plans: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test-files")
async def get_test_files():
    """Get list of available test spec files for healing"""
    try:
        test_files = []
        # Search in tests/ directory
        for directory in ["tests", "sample_tests"]:
            test_dir = Path(directory)
            if test_dir.exists():
                for file in sorted(test_dir.glob("*.spec.ts")):
                    stat = file.stat()
                    test_files.append({
                        "filename": file.name,
                        "path": str(file),
                        "relative_path": f"{directory}/{file.name}",
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "size": stat.st_size
                    })
        
        return {"test_files": test_files}
    except Exception as e:
        logger.error(f"Error getting test files: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workflow/start")
async def start_workflow(request: WorkflowRequest) -> WorkflowResponse:
    """Start a new workflow (planner, generator, healer, or full)"""
    workflow_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # Store workflow info
        active_workflows[workflow_id] = {
            "scenario": request.scenario,
            "agent": request.agent,
            "test_file": request.test_file,  # Store test plan file for generator or test files for healer
            "status": "queued",
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None,
            "events": []
        }
        
        logger.info(f"Started workflow {workflow_id} for agent: {request.agent}, scenario: {request.scenario}")
        if request.test_file:
            logger.info(f"  📁 test_file parameter: {request.test_file}")
        
        return WorkflowResponse(
            workflow_id=workflow_id,
            status="queued",
            message=f"Workflow {workflow_id} started successfully"
        )
    except Exception as e:
        logger.error(f"Error starting workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def run_real_agent_sync(workflow_id: str, agent_type: str, scenario: str, test_file: Optional[str] = None):
    """Run actual AI agent using CrewAI (synchronous)"""
    try:
        from src.test_ai_assistant.crew import PlaywrightAutomationCrew
        
        # Load context from test_file if provided
        context = ''
        if test_file:
            if agent_type == 'generator':
                # For generator: Load test plan file content
                try:
                    logger.info(f"📖 Loading test plan from: {test_file}")
                    with open(test_file, 'r') as f:
                        context = f.read()
                    logger.info(f"✅ Loaded test plan ({len(context)} chars)")
                except Exception as e:
                    logger.warning(f"⚠️  Could not load test plan file {test_file}: {e}")
            elif agent_type == 'healer':
                # For healer: Pass test file paths as context
                logger.info(f"📝 Setting test file paths for healer: {test_file}")
                context = test_file  # This can be comma-separated list of paths
                logger.info(f"✅ Test file paths set: {context}")
        
        # Create crew instance with proper input variable name
        inputs = {
            'user_input': scenario,
            'scenario': scenario,  # Include both for compatibility
            'context': context  # Context from test plan file or empty
        }
        
        workflow = active_workflows.get(workflow_id)
        
        # Build and run the crew
        crew_builder = PlaywrightAutomationCrew()
        
        if agent_type == 'full':
            # Run all three agents in sequence: Planner → Generator → Healer
            logger.info("Building full crew workflow: Planner → Generator → Healer")
            crew = crew_builder.full_crew()
            logger.info("Starting full crew execution...")
            result = crew.kickoff(inputs=inputs)
        else:
            # Run single agent
            agent_map = {
                'planner': 'test_planner_agent',
                'generator': 'test_generator_agent', 
                'healer': 'test_healer_agent',
            }
            
            agent_name = agent_map.get(agent_type, 'test_planner_agent')
            logger.info(f"Building crew for agent: {agent_name}")
            crew = crew_builder.build_crew(agent_name)
            logger.info(f"Starting {agent_name} execution...")
            result = crew.kickoff(inputs=inputs)
        
        if workflow:
            workflow['result'] = str(result)
            if agent_type == 'planner':
                workflow['test_plan'] = str(result)
        
        # Validate and auto-store knowledge in RAG for all agent types
        try:
            import glob
            log_files = glob.glob('logs/crew_execution_*.log')
            if log_files:
                latest_log = max(log_files, key=os.path.getmtime)
                with open(latest_log, 'r') as f:
                    log_content = f.read()
                
                # Check for planner exploration
                if agent_type in ['planner', 'full']:
                    if 'Using Tool: planner_setup_page' in log_content or 'Using Tool: browser_snapshot' in log_content:
                        if 'Using Tool: store_application_knowledge' not in log_content:
                            logger.warning("⚠️  Planner explored but didn't store knowledge in RAG!")
                            logger.info("📚 Attempting to extract and store knowledge from test plan...")
                            
                            from src.test_ai_assistant.tools.rag_tools import store_application_knowledge
                            
                            try:
                                store_result = store_application_knowledge(
                                    scenario=f"{scenario} - Auto-stored from planner output",
                                    navigation_path="See test plan for details",
                                    elements_discovered="See test plan file",
                                    application="salesforce",
                                    module="accounts",
                                    action="mixed"
                                )
                                logger.info(f"✅ Auto-stored basic exploration metadata: {store_result}")
                            except Exception as store_err:
                                logger.warning(f"Could not auto-store: {store_err}")
                        else:
                            logger.info("✅ Planner correctly stored knowledge in RAG")
                
                # Check for healer fixes
                if agent_type in ['healer', 'full']:
                    if 'Using Tool: playwright_test_run_test' in log_content:
                        # Healer ran tests - check if fixes were stored
                        fix_count = log_content.count('Using Tool: store_successful_fix')
                        if fix_count > 0:
                            logger.info(f"✅ Healer stored {fix_count} fix(es) in RAG")
                        else:
                            logger.warning("⚠️  Healer ran tests but didn't store any fixes in RAG")
                
                # Check for generator test patterns
                if agent_type in ['generator', 'full']:
                    if 'Using Tool: generator_write_test' in log_content:
                        logger.info("✅ Generator created test file")
                        # Generator primarily creates files, RAG storage is optional
        except Exception as e:
            logger.warning(f"Error checking RAG storage: {e}")
        
        logger.info(f"✅ {agent_name} completed")
        return str(result)
            
    except Exception as e:
        logger.error(f"Error running real agent: {e}", exc_info=True)
        raise e

async def generate_agent_events(workflow_id: str) -> AsyncGenerator[str, None]:
    """
    Generate Server-Sent Events for agent updates
    Supports both demo mode (mock events) and real mode (actual agents)
    """
    try:
        workflow = active_workflows.get(workflow_id)
        if not workflow:
            yield f"data: {json.dumps({'error': 'Workflow not found'})}\n\n"
            return
        
        # Update status
        workflow["status"] = "running"
        workflow["started_at"] = datetime.now().isoformat()
        
        agent_type = workflow.get("agent", "planner")
        scenario = workflow.get("scenario", "")
        test_file = workflow.get("test_file")  # Get test plan file for generator
        
        # Check if we should use real agents
        if API_MODE == 'real':
            # Validate API key
            if not (os.getenv('OPENAI_API_KEY') or os.getenv('GEMINI_API_KEY') or os.getenv('GROQ_API_KEY')):
                yield f"data: {json.dumps({'agent': agent_type, 'status': 'error', 'message': '❌ No API key configured. Set API_MODE=demo or add API key to .env'})}\n\n"
                workflow["status"] = "failed"
                return
            
            # Use real agents
            try:
                yield f"data: {json.dumps({'agent': agent_type, 'status': 'started', 'message': f'🚀 Starting real {agent_type} agent...', 'progress': 0})}\n\n"
                await asyncio.sleep(1)
                
                yield f"data: {json.dumps({'agent': agent_type, 'status': 'thinking', 'message': 'Initializing CrewAI agents and tools...', 'progress': 10})}\n\n"
                await asyncio.sleep(1)
                
                yield f"data: {json.dumps({'agent': agent_type, 'status': 'thinking', 'message': f'Loading {agent_type} agent configuration...', 'progress': 20})}\n\n"
                await asyncio.sleep(1)
                
                # Run the agent in a thread and provide periodic updates
                import threading
                result_holder = {'result': None, 'error': None, 'done': False}
                
                def run_agent():
                    try:
                        result_holder['result'] = run_real_agent_sync(workflow_id, agent_type, scenario, test_file)
                    except Exception as e:
                        result_holder['error'] = e
                    finally:
                        result_holder['done'] = True
                
                agent_thread = threading.Thread(target=run_agent)
                agent_thread.start()
                
                # Monitor the crew execution log for real activity
                import glob
                
                progress = 25
                last_log_position = 0
                check_count = 0
                
                while not result_holder['done']:
                    await asyncio.sleep(2)  # Check every 2 seconds
                    
                    if result_holder['done']:
                        break
                    
                    # Find the most recent crew execution log
                    log_files = glob.glob('logs/crew_execution_*.log')
                    if log_files:
                        latest_log = max(log_files, key=os.path.getmtime)
                        
                        try:
                            with open(latest_log, 'r') as f:
                                f.seek(last_log_position)
                                new_lines = f.readlines()
                                last_log_position = f.tell()
                                
                                # Parse log lines for interesting activity
                                for line in new_lines:
                                    if any(keyword in line for keyword in ['Using Tool:', 'Task:', 'Agent:', 'Thought:', '✅', '🔍', '📝', '🧠']):
                                        # Extract meaningful message
                                        if 'Using Tool:' in line:
                                            tool_name = line.split('Using Tool:')[-1].strip()
                                            message = f"🔧 Using tool: {tool_name}"
                                        elif 'Thought:' in line and 'need to' in line.lower():
                                            thought = line.split('Thought:')[-1].strip()[:100]
                                            message = f"💭 {thought}"
                                        elif '✅' in line:
                                            message = line.split('✅')[-1].strip()[:100]
                                            message = f"✅ {message}"
                                        elif 'RAG' in line and ('search' in line.lower() or 'found' in line.lower()):
                                            message = line.split('INFO - ')[-1].strip()[:100]
                                            message = f"🔍 {message}"
                                        else:
                                            continue
                                        
                                        progress = min(progress + 3, 90)
                                        yield f"data: {json.dumps({'agent': agent_type, 'status': 'thinking', 'message': message, 'progress': progress})}\n\n"
                        except Exception as e:
                            logger.debug(f"Error reading log: {e}")
                    
                    # Fallback progress update if no log activity
                    check_count += 1
                    if check_count % 5 == 0:  # Every 10 seconds
                        progress = min(progress + 2, 90)
                        yield f"data: {json.dumps({'agent': agent_type, 'status': 'thinking', 'message': f'⚙️ {agent_type.title()} agent working...', 'progress': progress})}\n\n"
                
                # Wait for thread to complete
                agent_thread.join()
                
                # Check for errors
                if result_holder['error']:
                    raise result_holder['error']
                
                result = result_holder['result']
                
                yield f"data: {json.dumps({'agent': agent_type, 'status': 'completed', 'progress': 100, 'message': f'✅ {agent_type.title()} completed successfully!', 'result': result[:200] if result else 'Success'})}\n\n"
                workflow["status"] = "completed"
                workflow["completed_at"] = datetime.now().isoformat()
                workflow["result"] = result
                return
                
            except Exception as e:
                logger.error(f"Real agent execution failed: {e}", exc_info=True)
                yield f"data: {json.dumps({'agent': agent_type, 'status': 'error', 'message': f'❌ Error: {str(e)[:100]}'})}\n\n"
                workflow["status"] = "failed"
                workflow["error"] = str(e)
                return
        
        # Demo mode - use mock events
        # Define events for each agent type
        agent_events = {
            "planner": [
                {"agent": "planner", "status": "started", "message": "🧠 Planner agent initialized"},
                {"agent": "planner", "status": "thinking", "message": "Searching RAG for similar scenarios..."},
                {"agent": "planner", "status": "progress", "progress": 25, "message": "Found partial match in RAG"},
                {"agent": "planner", "status": "progress", "progress": 50, "message": "Reusing cached navigation path"},
                {"agent": "planner", "status": "progress", "progress": 75, "message": "Exploring new action..."},
                {"agent": "planner", "status": "progress", "progress": 90, "message": "Storing discoveries in RAG"},
                {"agent": "planner", "status": "completed", "progress": 100, "message": "Test plan created successfully"},
            ],
            "generator": [
                {"agent": "generator", "status": "started", "message": "⚙️ Generator agent initialized"},
                {"agent": "generator", "status": "thinking", "message": "Loading test plan..."},
                {"agent": "generator", "status": "progress", "progress": 20, "message": "Searching RAG for code patterns..."},
                {"agent": "generator", "status": "progress", "progress": 40, "message": "Generating Playwright test code"},
                {"agent": "generator", "status": "progress", "progress": 60, "message": "Adding locators and actions"},
                {"agent": "generator", "status": "progress", "progress": 80, "message": "Adding assertions and validations"},
                {"agent": "generator", "status": "progress", "progress": 95, "message": "Storing code patterns in RAG"},
                {"agent": "generator", "status": "completed", "progress": 100, "message": "Test code generated successfully"},
            ],
            "healer": [
                {"agent": "healer", "status": "started", "message": "🔧 Healer agent initialized"},
                {"agent": "healer", "status": "thinking", "message": "Analyzing test failure..."},
                {"agent": "healer", "status": "progress", "progress": 25, "message": "Searching RAG for similar fixes..."},
                {"agent": "healer", "status": "progress", "progress": 50, "message": "Found 3 potential solutions"},
                {"agent": "healer", "status": "progress", "progress": 75, "message": "Applying fix to test file"},
                {"agent": "healer", "status": "progress", "progress": 90, "message": "Storing fix in RAG"},
                {"agent": "healer", "status": "completed", "progress": 100, "message": "Test fixed successfully"},
            ],
            "full": [
                {"agent": "planner", "status": "started", "message": "🧠 Starting Planner..."},
                {"agent": "planner", "status": "progress", "progress": 30, "message": "Creating test plan..."},
                {"agent": "planner", "status": "completed", "progress": 100, "message": "Test plan ready"},
                {"agent": "generator", "status": "started", "message": "⚙️ Starting Generator..."},
                {"agent": "generator", "status": "progress", "progress": 50, "message": "Generating test code..."},
                {"agent": "generator", "status": "completed", "progress": 100, "message": "Test code generated"},
                {"agent": "healer", "status": "started", "message": "🔧 Running & validating tests..."},
                {"agent": "healer", "status": "progress", "progress": 75, "message": "Tests passing!"},
                {"agent": "healer", "status": "completed", "progress": 100, "message": "All tests validated"},
            ]
        }
        
        events = agent_events.get(agent_type, agent_events["planner"])
        
        for event in events:
            # Add to workflow history
            workflow["events"].append({
                "timestamp": datetime.now().isoformat(),
                **event
            })
            
            # Send SSE event
            yield f"data: {json.dumps(event)}\n\n"
            await asyncio.sleep(1)  # Simulate work
        
        # Mark workflow as complete
        workflow["status"] = "completed"
        workflow["completed_at"] = datetime.now().isoformat()
        
        # Send completion event
        final_event = {
            "agent": "workflow",
            "status": "completed",
            "message": "Workflow completed successfully",
            "workflow_id": workflow_id
        }
        yield f"data: {json.dumps(final_event)}\n\n"
        
    except Exception as e:
        logger.error(f"Error in event stream: {e}")
        error_event = {
            "agent": "system",
            "status": "error",
            "message": str(e)
        }
        yield f"data: {json.dumps(error_event)}\n\n"

@app.get("/api/workflow/{workflow_id}/stream")
async def stream_workflow_events(workflow_id: str):
    """Stream real-time workflow events via Server-Sent Events"""
    if workflow_id not in active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return StreamingResponse(
        generate_agent_events(workflow_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.get("/api/workflow/{workflow_id}/status")
async def get_workflow_status(workflow_id: str):
    """Get current workflow status"""
    workflow = active_workflows.get(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return {
        "workflow_id": workflow_id,
        "status": workflow["status"],
        "scenario": workflow["scenario"],
        "agent": workflow["agent"],
        "created_at": workflow["created_at"],
        "started_at": workflow["started_at"],
        "completed_at": workflow["completed_at"],
        "total_events": len(workflow["events"])
    }

@app.get("/api/workflows")
async def list_workflows():
    """List all workflows (last 50)"""
    workflows = [
        {
            "workflow_id": wf_id,
            "status": wf["status"],
            "scenario": wf["scenario"],
            "created_at": wf["created_at"]
        }
        for wf_id, wf in sorted(
            active_workflows.items(),
            key=lambda x: x[1]["created_at"],
            reverse=True
        )[:50]
    ]
    return {"workflows": workflows, "total": len(workflows)}

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Playwright AI Agents API Server...")
    print("📊 Dashboard will be available at: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🧠 RAG Stats: http://localhost:8000/api/rag/stats")
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
