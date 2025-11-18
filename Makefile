# Makefile for Playwright CrewAI Agents

.PHONY: help install setup test lint format clean run-planner run-generator run-healer docker-build docker-run

help: ## Show this help message
	@echo "Playwright CrewAI Agents - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install Python and Node dependencies
	pip install -r requirements.txt
	npm install
	npx playwright install --with-deps chromium

setup: ## Initial setup (create venv, install deps, setup env)
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	npm install
	npx playwright install --with-deps chromium
	cp .env.example .env
	@echo "Setup complete! Edit .env with your API keys"

test: ## Run tests
	pytest tests/ -v

lint: ## Run linting (pylint, black check)
	black --check src/
	pylint src/

format: ## Format code with black
	black src/

clean: ## Clean generated files and caches
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf logs/*.log
	rm -rf test-results/
	rm -rf playwright-report/

run-planner: ## Run planner agent
	python src/test_ai_assistant/main.py planner

run-generator: ## Run generator agent
	python src/test_ai_assistant/main.py generator

run-healer: ## Run healer agent
	python src/test_ai_assistant/main.py healer

run-sequential: ## Run planner then generator
	python src/test_ai_assistant/main.py sequential

run-full: ## Run full pipeline (planner → generator → healer)
	python src/test_ai_assistant/main.py full

docker-build: ## Build Docker image
	docker build -t playwright-crewai-agents .

docker-run: ## Run in Docker container
	docker-compose up

docker-stop: ## Stop Docker containers
	docker-compose down

logs: ## View recent logs
	tail -f logs/crew_execution_*.log

validate-yaml: ## Validate YAML configuration files
	python -c "import yaml; yaml.safe_load(open('src/test_ai_assistant/config/agents.yaml')); yaml.safe_load(open('src/test_ai_assistant/config/tasks.yaml')); print('✅ YAML configs valid')"

security-check: ## Run security checks
	safety check --file requirements.txt
	bandit -r src/

update-deps: ## Update dependencies
	pip install --upgrade -r requirements.txt
	npm update

dev: ## Start development environment
	@echo "Starting development environment..."
	@echo "1. Activating venv"
	. venv/bin/activate
	@echo "2. Ready to code!"
