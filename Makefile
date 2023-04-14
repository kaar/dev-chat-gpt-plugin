export PIPENV_VENV_IN_PROJECT=1
PYTHON = python3
PYTEST = pytest
PIPENV = pipenv
HOST = "localhost"
PORT = 8000
API_URL = "http://$(HOST):$(PORT)/"

.PHONY: run
run: install
	@cd dev-chat-gpt-plugin && pipenv run uvicorn main:app --reload

.PHONY: install
install: Pipfile
	@echo "Installing dependencies..."
	@$(PIPENV) install

.PHONY: clean
clean:
	@echo "Cleaning up Pipenv environment..."
	@$(PIPENV) --rm
