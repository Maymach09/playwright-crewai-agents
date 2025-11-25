"""
Test Healer with RAG

Run the healer agent on the failing test to see RAG in action.
"""

from src.test_ai_assistant.main import run_healer

print("\n" + "="*70)
print("🏥 Running Healer Agent with RAG Support")
print("="*70 + "\n")

print("Watch for RAG tool usage in the logs below...")
print("Look for: 'search_error_fixes' or 'store_successful_fix'\n")

result = run_healer(
    user_input='Fix the failing test. The test has a strict mode violation where getByText resolves to multiple elements. Search RAG for proven fixes first.',
    test_location='tests/test.spec.ts'
)

print("\n" + "="*70)
print("✅ Healing Complete!")
print("="*70)
print("\nCheck if RAG tools were used in the logs above!")
