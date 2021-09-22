PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VIRTUALENV_DIR := $(PROJECT_DIR)/venv
VIRTUAL_ENV_DISABLE_PROMPT = true

.SHELLFLAGS := -eu -o pipefail -c

PATH := $(VIRTUALENV_DIR)/bin:$(EXTRA_PATH):/usr/local/bin:/bin:$(PATH)
export PATH

help:
	@grep -E '^[a-zA-Z1-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN { FS = ":.*?## " }; { printf "\033[36m%-30s\033[0m %s\n", $$1, $$2 }'

$(VIRTUALENV_DIR):
	virtualenv -p $(shell command -v python3) $(VIRTUALENV_DIR)

$(VIRTUALENV_DIR)/bin: requirements.txt
	pip install -r requirements.txt
	@touch '$(@)'

$(VIRTUALENV_DIR)/bin/black: requirements-dev.txt
	pip install -r requirements-dev.txt
	python setup.py develop
	@touch '$(@)'

pre-commit-install: ## Install pre-commit hooks
		pre-commit install

install: $(VIRTUALENV_DIR) $(VIRTUALENV_DIR)/bin ## Install project

install-dev: install $(VIRTUALENV_DIR)/bin/black ## Install project for development
	$(info Run make pre-commit-install to install git hooks)

lint: ## Run flake8, isort and black linters
	flake8 chaosopenstack/ tests/
	isort --check-only --profile black chaosopenstack/ tests/
	black --check --diff chaosopenstack/ tests/

format: ## Run isort and black formaters
	isort --profile black chaosopenstack/ tests/
	black chaosopenstack/ tests/

tests: ## Run python test suite
	pytest
	coverage html

.PHONY: format lint tests
