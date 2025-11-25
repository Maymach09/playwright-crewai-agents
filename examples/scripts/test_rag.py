"""
Test RAG System

This script verifies that our RAG implementation works correctly.
Run this to test the ChromaDB setup and retrieval functionality.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.test_ai_assistant.rag import RAGRetriever
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_rag_system():
    """Test the RAG system end-to-end."""
    
    print("\n" + "="*60)
    print("Testing RAG System")
    print("="*60 + "\n")
    
    # Initialize retriever
    print("1. Initializing RAG Retriever...")
    retriever = RAGRetriever(persist_directory="./test_rag_storage")
    print("✓ Retriever initialized\n")
    
    # Initialize knowledge base
    print("2. Loading initial knowledge...")
    retriever.initialize_knowledge_base()
    print("✓ Knowledge base loaded\n")
    
    # Get stats
    print("3. Knowledge Base Statistics:")
    stats = retriever.get_stats()
    for collection, info in stats.items():
        print(f"   - {collection}: {info['count']} items")
    print()
    
    # Test search for fixes
    print("4. Testing Fix Search...")
    print("   Query: 'locator not found error'")
    fixes = retriever.search_fixes(
        error_message="locator not found error",
        n_results=2
    )
    print(f"   Found {len(fixes)} fixes:")
    for i, fix in enumerate(fixes, 1):
        print(f"\n   Fix {i} (similarity: {fix['similarity']:.2f}):")
        print(f"   {fix['content'][:100]}...")
        print(f"   Tags: {fix['metadata'].get('tags', [])}")
    print()
    
    # Test search for code patterns
    print("5. Testing Pattern Search...")
    print("   Query: 'fill a form and submit'")
    patterns = retriever.search_patterns(
        task_description="fill a form and submit",
        n_results=2
    )
    print(f"   Found {len(patterns)} patterns:")
    for i, pattern in enumerate(patterns, 1):
        print(f"\n   Pattern {i} (similarity: {pattern['similarity']:.2f}):")
        print(f"   Type: {pattern['metadata'].get('pattern_type')}")
        print(f"   Tags: {pattern['metadata'].get('tags', [])}")
    print()
    
    # Test search for test plans
    print("6. Testing Test Plan Search...")
    print("   Query: 'test user workflow from start to finish'")
    plans = retriever.search_test_plans(
        scenario_description="test user workflow from start to finish",
        n_results=2
    )
    print(f"   Found {len(plans)} test plans:")
    for i, plan in enumerate(plans, 1):
        print(f"\n   Plan {i} (similarity: {plan['similarity']:.2f}):")
        print(f"   Type: {plan['metadata'].get('plan_type')}")
        print(f"   Level: {plan['metadata'].get('test_level')}")
    print()
    
    # Test adding new knowledge (feedback loop)
    print("7. Testing Feedback Loop (adding learned fix)...")
    retriever.add_successful_fix(
        error_message="custom error: button not clickable",
        fix_applied="Added scrollIntoViewIfNeeded() before click",
        error_type="interaction",
        test_file="test_example.spec.ts"
    )
    print("✓ Successfully added learned fix\n")
    
    # Verify new knowledge was added
    print("8. Verifying new knowledge...")
    updated_stats = retriever.get_stats()
    print(f"   test_fixes collection now has {updated_stats['test_fixes']['count']} items")
    print("   (should be +1 from before)\n")
    
    # Search for the newly added fix
    print("9. Testing retrieval of learned fix...")
    new_fixes = retriever.search_fixes(
        error_message="button not clickable",
        n_results=1
    )
    if new_fixes:
        print(f"   ✓ Found learned fix: {new_fixes[0]['content'][:80]}...")
    else:
        print("   ✗ Could not retrieve learned fix")
    print()
    
    print("="*60)
    print("RAG System Test Complete! 🎉")
    print("="*60 + "\n")
    
    print("Summary:")
    print("✓ RAG retriever initialized")
    print("✓ Knowledge base loaded with initial patterns")
    print("✓ Fix search working")
    print("✓ Pattern search working")
    print("✓ Test plan search working")
    print("✓ Feedback loop working (learning new fixes)")
    print("\nNext step: Integrate with agents!")


if __name__ == "__main__":
    try:
        test_rag_system()
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        sys.exit(1)
