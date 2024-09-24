CODE ?= ./src
TESTS ?= ./tests
VENV ?= .venv

init:
	python3.12 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install


plint:
	$(VENV)/bin/ruff format $(CODE)
	$(VENV)/bin/ruff check $(CODE) --fix --show-fixes
	$(VENV)/bin/mypy --install-types --non-interactive $(CODE)
