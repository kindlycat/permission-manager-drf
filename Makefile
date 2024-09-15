.PHONY: help
help: ## Help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help
PROJECT_NAME = '$(shell basename $(CURDIR)):dev'
DOCKER_CMD = docker run --rm -it -v "$(CURDIR):/app" -v /opt/venv $(PROJECT_NAME) /bin/bash

.PHONY: build
build: ## Build
	@docker build -t $(PROJECT_NAME) .

.PHONY: console
console: ## Console
	@$(DOCKER_CMD)

.PHONY: tests
tests: ## Tests
	@$(DOCKER_CMD) -c "pytest $(c)"

.PHONY: linters
check: ## Run linters check
	@$(DOCKER_CMD) -c 'ruff format --check .; ruff check .'

.PHONY: reformat
reformat: ## Run linters check
	@$(DOCKER_CMD) -c 'ruff format .; ruff check . --fix $(c)'

.PHONY: docs
docs: ## Make docs html
	@$(DOCKER_CMD) -c 'cd docs; rm -rf _build; make html'
