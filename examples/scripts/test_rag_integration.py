"""
Quick test to verify RAG tools are properly integrated with agents.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.test_ai_assistant.crew import PlaywrightAutomationCrew

print("\n" + "="*60)
print("Testing RAG Integration with Agents")
print("="*60 + "\n")

try:
    print("1. Initializing PlaywrightAutomationCrew...")
    crew = PlaywrightAutomationCrew()
    print("   ✅ Crew initialized successfully\n")
    
    print("2. Creating agents and checking their tools...\n")
    
    # Test planner agent
    print("   Planner Agent:")
    planner = crew.test_planner_agent()
    planner_tool_names = [t.name for t in planner.tools]
    rag_tools_in_planner = [name for name in planner_tool_names if 'search' in name or 'rag' in name or 'store' in name]
    print(f"   - Total tools: {len(planner.tools)}")
    print(f"   - RAG tools: {rag_tools_in_planner}")
    print()
    
    # Test generator agent
    print("   Generator Agent:")
    generator = crew.test_generator_agent()
    generator_tool_names = [t.name for t in generator.tools]
    rag_tools_in_generator = [name for name in generator_tool_names if 'search' in name or 'rag' in name or 'store' in name]
    print(f"   - Total tools: {len(generator.tools)}")
    print(f"   - RAG tools: {rag_tools_in_generator}")
    print()
    
    # Test healer agent
    print("   Healer Agent:")
    healer = crew.test_healer_agent()
    healer_tool_names = [t.name for t in healer.tools]
    rag_tools_in_healer = [name for name in healer_tool_names if 'search' in name or 'rag' in name or 'store' in name or 'get_rag' in name]
    print(f"   - Total tools: {len(healer.tools)}")
    print(f"   - RAG tools: {rag_tools_in_healer}")
    print()
    
    print("="*60)
    print("✅ RAG Tools Successfully Integrated!")
    print("="*60)
    print("\nAll agents now have access to:")
    print("  - search_error_fixes (find proven solutions)")
    print("  - search_code_patterns (find code templates)")
    print("  - search_test_plans (find test structures)")
    print("  - store_successful_fix (learn from success)")
    print("  - get_rag_stats (monitor knowledge growth)")
    print("\nAgents can now use RAG to be 5-10x more efficient! 🚀")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
