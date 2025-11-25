"""
Test RAG Tools

Verify that RAG tools can be imported and used by agents.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.test_ai_assistant.tools.rag_tools import (
    search_error_fixes,
    search_code_patterns,
    search_test_plans,
    store_successful_fix,
    get_rag_stats,
    RAG_TOOLS
)

print("\n" + "="*60)
print("Testing RAG Tools")
print("="*60 + "\n")

print("1. Available Tools:")
print(f"   Total RAG tools: {len(RAG_TOOLS)}")
for tool in RAG_TOOLS:
    print(f"   - {tool.name}")
print()

print("2. Test search_error_fixes:")
result = search_error_fixes.run("locator not found error")
print(result[:200] + "..." if len(result) > 200 else result)
print()

print("3. Test search_code_patterns:")
result = search_code_patterns.run("fill a form and submit")
print(result[:200] + "..." if len(result) > 200 else result)
print()

print("4. Test search_test_plans:")
result = search_test_plans.run("test user workflow from start to finish")
print(result[:200] + "..." if len(result) > 200 else result)
print()

print("5. Test get_rag_stats:")
result = get_rag_stats.run("")
print(result)
print()

print("6. Test store_successful_fix:")
result = store_successful_fix.run(
    "test error for demo",
    "applied test fix for demo",
    "test",
    "demo.spec.ts"
)
print(result)
print()

print("7. Verify stored fix (check stats again):")
result = get_rag_stats.run("")
print(result)
print()

print("="*60)
print("RAG Tools Test Complete! ✅")
print("="*60)
print("\nNext: Agents can now use these tools by importing:")
print("  from src.test_ai_assistant.tools import RAG_TOOLS")
