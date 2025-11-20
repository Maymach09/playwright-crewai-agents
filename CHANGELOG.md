# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-19

### 🎉 Major Feature: RAG-Powered Learning System

#### Added
- **RAG (Retrieval-Augmented Generation) System**: Complete knowledge management system using ChromaDB
  - `src/test_ai_assistant/rag/vector_store.py`: ChromaDB vector database integration
  - `src/test_ai_assistant/rag/retriever.py`: High-level query interface with 4 search methods
  - `src/test_ai_assistant/rag/knowledge_base.py`: Seed data and initial knowledge
  - `src/test_ai_assistant/tools/rag_tools.py`: 7 RAG tools for agent use

#### RAG Features
- **4 Knowledge Collections**:
  - `test_fixes`: Stores proven solutions to test failures with success rates
  - `code_patterns`: Best practices and reusable code patterns
  - `test_plans`: Historical test plans for reference
  - `application_knowledge`: UI flows, locators, navigation paths (NEW!)

- **7 RAG Tools for Agents**:
  1. `search_error_fixes`: Find proven fixes for similar errors
  2. `store_successful_fix`: Cache successful fixes with metadata
  3. `search_code_patterns`: Find best practices
  4. `search_test_plans`: Reference historical plans
  5. `get_rag_stats`: View knowledge base statistics
  6. `search_application_knowledge`: Find cached UI explorations (NEW!)
  7. `store_application_knowledge`: Cache discoveries after exploration (NEW!)

#### Performance Improvements
- **Planner Speed**: 15-20x faster on subsequent runs
  - First run: ~5 minutes (full exploration)
  - Exact RAG match: ~17 seconds (skip exploration)
  - Partial RAG match: ~3-4 minutes (reuse navigation)
- **Healer Speed**: 2-3x faster with proven fix patterns
- **Learning System**: Each run makes the system smarter

#### Agent Enhancements
- **Planner Agent**: Now searches RAG before exploring
  - Three-tier matching: EXACT (skip exploration), PARTIAL (reuse navigation), NONE (full exploration)
  - Mandatory storage after exploration to build knowledge base
  - Action-specific matching (create ≠ delete ≠ edit)
- **Healer Agent**: Searches RAG for proven fixes first
  - Applies highest success rate fixes
  - Handles cascading errors intelligently
  - Stores successful fixes back to RAG
- **Generator Agent**: Has access to RAG but uses test plan context primarily

#### Configuration Updates
- Updated `tasks.yaml` with RAG workflow integration
- Added mandatory storage requirements to prevent knowledge loss
- Enhanced error handling for cascading test failures
- Increased retry limits for complex healing scenarios

#### Technical Details
- ChromaDB 0.4.0+ for vector storage
- Semantic search with similarity scoring
- Singleton pattern for RAG retriever (efficient initialization)
- Automatic knowledge base initialization with seed data
- Metadata-rich storage (success rates, timestamps, scenarios)

#### Documentation
- Updated README.md with RAG features and performance metrics
- Added RAG usage examples and commands
- Documented knowledge base statistics
- Added RAG-specific tips and best practices

### Changed
- `.gitignore`: Added `rag_storage/` to exclude learned knowledge from git
- Planner workflow: Now includes RAG search and storage steps
- Healer workflow: Prioritizes RAG fixes before manual analysis
- Performance baselines: Updated with RAG-enhanced metrics

### Fixed
- Task instructions: Made RAG storage mandatory to prevent knowledge loss
- Action matching: Explicit validation that create ≠ delete ≠ edit
- Cascading errors: Healer now searches RAG for each new error type

### Migration Notes
- Existing installations: RAG will initialize automatically on first run
- No breaking changes to existing workflows
- Old test plans remain compatible
- Initial knowledge: 25 items (12 fixes, 5 patterns, 4 plans, 4 app flows)

## [1.0.0] - 2025-11-18

### Added
- Initial release of Playwright CrewAI Agents
- Three AI agents: Planner, Generator, and Healer
- Multi-agent workflow using CrewAI framework
- Support for OpenAI GPT-4o-mini
- Context management optimization for LLM token limits
- Error-message-only healing approach to prevent context overflow
- MCP (Model Context Protocol) integration for Playwright and filesystem tools
- Comprehensive test plan generation
- Automated Playwright test code generation
- Self-healing test capability
- Configuration via YAML files (agents.yaml, tasks.yaml)
- CLI interface for running individual agents or full pipeline
- Logging system with timestamped log files
- Authentication state management for Playwright
- Sample test plans and tests for Salesforce CRM

### Features
- **Planner Agent**: Explores applications and creates detailed test plans with steps and expected results
- **Generator Agent**: Generates executable TypeScript Playwright tests from test plans
- **Healer Agent**: Automatically debugs and fixes failing tests using error patterns
- **Flexible Execution**: Run agents individually or as complete pipeline
- **Cost Optimization**: Uses GPT-4o-mini for affordable operation ($0.009 per test)
- **Token Management**: Strict iteration limits and optimized context to prevent overflow

### Technical Details
- Python 3.13+ support
- Node.js 18+ with Playwright
- CrewAI framework for multi-agent orchestration
- Tenacity for LLM retry logic
- YAML-based configuration for easy customization
- Structured logging for debugging and monitoring

### Documentation
- Comprehensive README with setup and usage instructions
- YAML configuration examples
- Sample test plans for reference
- Inline code documentation

### Known Limitations
- Healer requires OpenAI for complex debugging (local LLMs insufficient)
- Best suited for 1-50 tests; larger batches need optimization
- Requires authentication state for Salesforce testing
- Context window limits require careful task design

## [Unreleased]

### Planned
- Support for additional LLM providers
- Batch processing for large test suites
- Enhanced error pattern recognition
- Visual test report generation
- Integration with CI/CD pipelines
- Support for more application types beyond Salesforce
