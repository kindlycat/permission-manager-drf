.PHONY: help
help: ## Help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help
PROJECT_NAME := '$(shell basename $(CURDIR)):dev'

.PHONY: build
build: ## Build
	@docker build -t $(PROJECT_NAME) .

.PHONY: console
console: ## Console
	@docker run --rm -it -v "$(CURDIR):/code" $(PROJECT_NAME) /bin/bash

.PHONY: tests
tests: ## Tests
	@docker run --rm -it -v "$(CURDIR):/code" $(PROJECT_NAME) /bin/bash -c "pytest $(c)"

.PHONY: linters
check: ## Run linters check
	@docker run --rm -it -v "$(CURDIR):/code" $(PROJECT_NAME) /bin/bash -c 'ruff format --check .; ruff check .'

.PHONY: reformat
reformat: ## Run linters check
	@docker run --rm -it -v "$(CURDIR):/code" $(PROJECT_NAME) /bin/bash -c 'ruff format .; ruff check . --fix $(c)'
