# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
