"""
RAG Tool - Knowledge Base Search for Agents

This tool provides agents with access to the RAG system
to search for proven fixes, code patterns, and test plans.

Agents can call these tools when they need help:
- Healer: Search for error fixes
- Generator: Search for code patterns
- Planner: Search for test plan templates
"""

import logging
from crewai.tools import tool
from src.test_ai_assistant.rag import RAGRetriever

logger = logging.getLogger(__name__)

# Initialize RAG retriever once (singleton pattern)
_rag_retriever = None

def get_rag_retriever():
    """Get or initialize the RAG retriever (singleton)."""
    global _rag_retriever
    if _rag_retriever is None:
        try:
            logger.info("Initializing RAG retriever...")
            _rag_retriever = RAGRetriever(persist_directory="./rag_storage")
            _rag_retriever.initialize_knowledge_base()
            
            # Log stats
            stats = _rag_retriever.get_stats()
            logger.info("RAG Knowledge Base initialized:")
            for collection, info in stats.items():
                logger.info(f"  - {collection}: {info['count']} items")
        except Exception as e:
            logger.error(f"Failed to initialize RAG: {e}")
            _rag_retriever = None
    
    return _rag_retriever


@tool("search_error_fixes")
def search_error_fixes(error_message: str) -> str:
    """Search knowledge base for proven fixes for similar errors.
    
    Use this tool when you encounter a test error and need solutions.
    The knowledge base contains patterns from past successful fixes.
    
    Args:
        error_message: The error text from the test failure
        
    Returns:
        Proven fix patterns with success rates, or guidance if none found
        
    Example:
        search_error_fixes("Error: locator 'button' not found")
    """
    try:
        rag = get_rag_retriever()
        if not rag:
            return "RAG system not available. Use standard debugging approach."
        
        logger.info(f"RAG: Searching fixes for: {error_message[:80]}...")
        fixes = rag.search_fixes(error_message, n_results=3)
        
        if not fixes:
            logger.info("RAG: No similar errors found")
            return "No similar errors found in knowledge base. Proceed with standard debugging."
        
        result = "🔍 Found proven fixes for similar errors:\n\n"
        for i, fix in enumerate(fixes, 1):
            similarity = fix.get('similarity', 0)
            metadata = fix.get('metadata', {})
            success_rate = metadata.get('success_rate', 0)
            error_type = metadata.get('error_type', 'unknown')
            
            result += f"{i}. [{error_type.upper()}] Success: {success_rate:.0%} | Match: {similarity:.0%}\n"
            result += f"   {fix['content']}\n\n"
        
        result += "💡 Try applying the highest success rate fix first."
        logger.info(f"RAG: Returned {len(fixes)} relevant fixes")
        return result
        
    except Exception as e:
        logger.error(f"RAG search error: {e}")
        return f"RAG search failed: {str(e)}. Use standard debugging."


@tool("search_code_patterns")
def search_code_patterns(task_description: str, pattern_type: str = None) -> str:
    """Search knowledge base for reusable code patterns.
    
    Use this tool when generating tests to find proven code templates.
    The knowledge base contains Playwright patterns that work well.
    
    Args:
        task_description: What you need to accomplish (e.g., "fill a form")
        pattern_type: Optional filter (navigation, form, wait, assertion, locator)
        
    Returns:
        Relevant code patterns with examples
        
    Example:
        search_code_patterns("fill a form and submit", pattern_type="form")
    """
    try:
        rag = get_rag_retriever()
        if not rag:
            return "RAG system not available. Generate code from scratch."
        
        logger.info(f"RAG: Searching patterns for: {task_description[:80]}...")
        patterns = rag.search_patterns(task_description, n_results=2, pattern_type=pattern_type)
        
        if not patterns:
            logger.info("RAG: No matching patterns found")
            return "No matching code patterns found. Create new code following best practices."
        
        result = "🔍 Found relevant code patterns:\n\n"
        for i, pattern in enumerate(patterns, 1):
            similarity = pattern.get('similarity', 0)
            metadata = pattern.get('metadata', {})
            pattern_type_meta = metadata.get('pattern_type', 'unknown')
            complexity = metadata.get('complexity', 'unknown')
            
            result += f"Pattern {i}: {pattern_type_meta.upper()} (Complexity: {complexity} | Match: {similarity:.0%})\n"
            result += f"{pattern['content']}\n\n"
            result += "-" * 60 + "\n\n"
        
        result += "💡 Adapt these patterns to your specific requirements."
        logger.info(f"RAG: Returned {len(patterns)} patterns")
        return result
        
    except Exception as e:
        logger.error(f"RAG pattern search error: {e}")
        return f"RAG search failed: {str(e)}. Generate code from scratch."


@tool("search_test_plans")
def search_test_plans(scenario_description: str, plan_type: str = None) -> str:
    """Search knowledge base for test plan templates and structures.
    
    Use this tool when planning tests to find proven test structures.
    The knowledge base contains templates for different test types.
    
    Args:
        scenario_description: What you need to test (e.g., "user login workflow")
        plan_type: Optional filter (smoke, e2e, crud, navigation)
        
    Returns:
        Relevant test plan templates with structure guidance
        
    Example:
        search_test_plans("test user workflow", plan_type="e2e")
    """
    try:
        rag = get_rag_retriever()
        if not rag:
            return "RAG system not available. Create test plan from scratch."
        
        logger.info(f"RAG: Searching test plans for: {scenario_description[:80]}...")
        plans = rag.search_test_plans(scenario_description, n_results=2, plan_type=plan_type)
        
        if not plans:
            logger.info("RAG: No matching test plans found")
            return "No matching test plans found. Create plan using standard structure."
        
        result = "🔍 Found relevant test plan templates:\n\n"
        for i, plan in enumerate(plans, 1):
            similarity = plan.get('similarity', 0)
            metadata = plan.get('metadata', {})
            plan_type_meta = metadata.get('plan_type', 'unknown')
            test_level = metadata.get('test_level', 'unknown')
            
            result += f"Template {i}: {plan_type_meta.upper()} (Level: {test_level} | Match: {similarity:.0%})\n"
            result += f"{plan['content']}\n\n"
            result += "-" * 60 + "\n\n"
        
        result += "💡 Use these templates as a starting point for your test plan."
        logger.info(f"RAG: Returned {len(plans)} test plans")
        return result
        
    except Exception as e:
        logger.error(f"RAG test plan search error: {e}")
        return f"RAG search failed: {str(e)}. Create plan from scratch."


@tool("store_successful_fix")
def store_successful_fix(error_message: str, fix_applied: str, error_type: str, test_file: str) -> str:
    """Store a successful fix in the knowledge base for future use.
    
    Call this AFTER successfully fixing a test to help future healing.
    This is how the system learns from experience.
    
    Args:
        error_message: The original error text (brief description)
        fix_applied: What you did to fix it (the solution)
        error_type: Category (locator, timeout, assertion, interaction, etc.)
        test_file: Which test file was fixed
        
    Returns:
        Confirmation message
        
    Example:
        store_successful_fix(
            error_message="locator 'button' not found",
            fix_applied="Added waitForSelector with 10s timeout",
            error_type="locator",
            test_file="login.spec.ts"
        )
    """
    try:
        rag = get_rag_retriever()
        if not rag:
            return "RAG system not available. Fix not stored (but test is fixed!)."
        
        logger.info(f"RAG: Storing successful fix for {test_file}")
        rag.add_successful_fix(
            error_message=error_message,
            fix_applied=fix_applied,
            error_type=error_type,
            test_file=test_file
        )
        
        logger.info("RAG: Successfully stored fix in knowledge base")
        return f"✅ Fix stored in knowledge base! This solution will help with similar errors in the future."
        
    except Exception as e:
        logger.error(f"RAG store error: {e}")
        return f"⚠️ Could not store fix: {str(e)}. Fix still works, just not saved for future."


@tool("get_rag_stats")
def get_rag_stats(query: str = "") -> str:
    """Get statistics about the RAG knowledge base.
    
    Use this to see how much knowledge has been accumulated.
    
    Args:
        query: Optional (not used, for compatibility)
    
    Returns:
        Knowledge base statistics
    """
    try:
        rag = get_rag_retriever()
        if not rag:
            return "RAG system not available."
        
        stats = rag.get_stats()
        
        result = "📊 RAG Knowledge Base Statistics:\n\n"
        total = 0
        for collection, info in stats.items():
            count = info.get('count', 0)
            total += count
            result += f"- {collection}: {count} items\n"
        
        result += f"\n**Total Knowledge Items: {total}**\n"
        result += "\nThis knowledge grows as agents successfully fix tests and generate good code!"
        
        return result
        
    except Exception as e:
        logger.error(f"RAG stats error: {e}")
        return f"Could not get RAG stats: {str(e)}"


@tool("search_application_knowledge")
def search_application_knowledge(scenario_description: str) -> str:
    """Search for previously discovered application flows and UI elements.
    
    Use this BEFORE exploring the application to check if we've
    already mapped out this scenario. Saves time by reusing discoveries.
    
    Args:
        scenario_description: What you need to test (e.g., "create account salesforce")
        
    Returns:
        Previously discovered UI flows, element locators, and navigation paths
        
    Example:
        search_application_knowledge("create new account in salesforce")
    """
    try:
        rag = get_rag_retriever()
        if not rag:
            return "RAG system not available. Proceed with live exploration."
        
        logger.info(f"RAG: Searching application knowledge for: {scenario_description[:80]}...")
        knowledge = rag.search_application_knowledge(scenario_description, n_results=2)
        
        if not knowledge:
            logger.info("RAG: No previous exploration found")
            return "❌ No previous exploration found for this scenario. Proceed with live browser exploration."
        
        result = "✅ Found previous explorations of similar scenarios:\n\n"
        for i, item in enumerate(knowledge, 1):
            similarity = item.get('similarity', 0)
            metadata = item.get('metadata', {})
            application = metadata.get('application', 'unknown')
            module = metadata.get('module', 'unknown')
            action = metadata.get('action', 'unknown')
            
            result += f"{i}. [{application.upper()} - {module} - {action}] Match: {similarity:.0%}\n"
            result += f"{item['content']}\n\n"
        
        result += "💡 Use this cached knowledge to speed up test planning!"
        return result
        
    except Exception as e:
        logger.error(f"RAG search_application_knowledge error: {e}")
        return f"⚠️ Search failed: {str(e)}. Proceed with live exploration."


@tool("store_application_knowledge")
def store_application_knowledge(
    scenario: str,
    navigation_path: str,
    elements_discovered: str,
    application: str = "unknown",
    module: str = "unknown",
    action: str = "unknown"
) -> str:
    """Store discovered application structure for future reuse.
    
    Use this AFTER exploring the application to cache what you learned.
    This builds up the "application memory" over time.
    
    Args:
        scenario: High-level description (e.g., "Create Account in Salesforce")
        navigation_path: How to reach feature (e.g., "Home → Accounts → New")
        elements_discovered: UI elements and locators found (detailed text)
        application: App name (e.g., "salesforce")
        module: Module/section (e.g., "accounts")
        action: Action type (e.g., "create")
        
    Returns:
        Confirmation message
        
    Example:
        store_application_knowledge(
            scenario="Create new account with minimum data",
            navigation_path="Home → Accounts → New button",
            elements_discovered="Account Name: getByRole('textbox', { name: 'Account Name' })",
            application="salesforce",
            module="accounts",
            action="create"
        )
    """
    try:
        rag = get_rag_retriever()
        if not rag:
            return "⚠️ RAG system not available. Exploration was successful but not cached."
        
        logger.info(f"RAG: Storing application knowledge for {application}/{module}/{action}")
        
        rag.add_application_knowledge(
            scenario=scenario,
            navigation_path=navigation_path,
            elements_discovered=elements_discovered,
            application=application,
            module=module,
            action=action
        )
        
        logger.info("RAG: Successfully stored application knowledge")
        return "✅ Application knowledge stored! This will speed up similar tests in the future."
        
    except Exception as e:
        logger.error(f"RAG store_application_knowledge error: {e}")
        return f"⚠️ Could not store knowledge: {str(e)}. Exploration still succeeded."


# Export all tools as a list for easy importing
RAG_TOOLS = [
    search_error_fixes,
    search_code_patterns,
    search_test_plans,
    store_successful_fix,
    get_rag_stats,
    search_application_knowledge,
    store_application_knowledge
]
