# Examples

This folder contains example scripts, test plans, and sample code.

## 📁 Structure

```
examples/
├── scripts/                      # Utility scripts
│   ├── save-auth.ts             # Save authentication state
│   ├── run_healer_with_rag.py   # Run healer agent with RAG
│   ├── test_rag.py              # Test RAG functionality
│   ├── test_rag_integration.py  # Integration tests for RAG
│   ├── test_rag_tools.py        # Test RAG tools
│   └── scenarios_test_accounts.txt  # Test account scenarios (gitignored)
│
├── test_plans/                  # Generated test plans (examples)
│   └── *.md                     # Markdown test plan files
│
└── sample_tests/                # Sample Playwright tests
    └── *.spec.ts                # TypeScript test files
```

## 🔧 Scripts

### Authentication
```bash
# Save authentication state for tests
npx ts-node examples/scripts/save-auth.ts
```

### RAG Testing
```bash
# Test basic RAG functionality
python examples/scripts/test_rag.py

# Test RAG integration with agents
python examples/scripts/test_rag_integration.py

# Run healer with RAG
python examples/scripts/run_healer_with_rag.py
```

## 📄 Test Plans

Generated test plans are stored in `test_plans/` directory. These are created by the Planner agent and serve as input for the Generator agent.

## 🧪 Sample Tests

Sample Playwright tests can be found in the main `tests/` directory or in `sample_tests/` for reference implementations.

## ⚠️ Note

Files in `scenarios_test_accounts.txt` contain sensitive test data and are excluded from version control.
