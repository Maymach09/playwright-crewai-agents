# Contributing to Playwright CrewAI Agents

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, Node version)
- Relevant logs from `logs/` directory

### Suggesting Features

Feature requests are welcome! Please:
- Check existing issues first
- Describe the feature clearly
- Explain the use case
- Consider implementation details

### Pull Requests

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add tests if applicable
   - Update documentation
   - Keep commits atomic and well-described

4. **Test your changes**
   ```bash
   # Run tests
   pytest tests/
   
   # Run linting
   pylint src/
   
   # Test agents individually
   python src/test_ai_assistant/main.py planner
   python src/test_ai_assistant/main.py generator
   python src/test_ai_assistant/main.py healer
   ```

5. **Update documentation**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update YAML configs if agent behavior changes

6. **Submit pull request**
   - Reference related issues
   - Describe what changed and why
   - Include screenshots/logs if relevant

## Development Setup

1. **Clone and install**
   ```bash
   git clone <repo-url>
   cd playwright_agents
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Add your API keys
   ```

3. **Run in development mode**
   ```bash
   # Test individual agents
   python src/test_ai_assistant/main.py planner
   ```

## Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write descriptive variable names
- Add comments for complex logic
- Keep functions focused and small

## Agent Development Guidelines

### Adding New Agents

1. Add agent definition to `src/test_ai_assistant/config/agents.yaml`
2. Add task definition to `src/test_ai_assistant/config/tasks.yaml`
3. Add agent method in `crew.py` with `@agent` decorator
4. Add task method in `crew.py` with `@task` decorator
5. Update `build_crew()` method to include new agent
6. Document in README.md

### Modifying Existing Agents

- Test thoroughly before submitting
- Update task descriptions in YAML files
- Maintain backward compatibility if possible
- Document breaking changes clearly

## Testing

- Write tests for new features
- Ensure existing tests pass
- Test with different LLM providers (OpenAI, Gemini)
- Test error handling and edge cases

## Documentation

- Use clear, concise language
- Include code examples
- Update README for user-facing changes
- Add inline comments for complex code

## Questions?

Open an issue for discussion or reach out to maintainers.

Thank you for contributing! 🎉
