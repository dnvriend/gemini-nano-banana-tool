.PHONY: help
.DEFAULT_GOAL := help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

lint: ## Run linting with ruff
	uv run ruff check .

format: ## Format code with ruff
	uv run ruff format .

typecheck: ## Run type checking with mypy
	uv run mypy gemini_nano_banana_tool

test: ## Run tests
	uv run pytest tests/

check: lint typecheck test ## Run all checks (lint, typecheck, test)

pipeline: format lint typecheck test build install-global ## Run full pipeline (format, lint, typecheck, test, build, install-global)

clean: ## Remove build artifacts and cache
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

run: ## Run gemini-nano-banana-tool (usage: make run ARGS="...")
	uv run gemini-nano-banana-tool $(ARGS)

build: ## Build package
	uv build

install-global: ## Install globally with uv tool
	uv tool install . --reinstall

uninstall-global: ## Uninstall global installation
	uv tool uninstall gemini-nano-banana-tool
