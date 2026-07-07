PYTHON := .venv/bin/python

.DEFAULT_GOAL := help

.PHONY: help install test lint format typecheck check demo

help:
	@echo "Available targets:"
	@echo "  install    create .venv and install the package with dev deps"
	@echo "  check      run all quality gates (lint, format, typecheck, test)"
	@echo "  test       run the test suite"
	@echo "  lint       run ruff check"
	@echo "  format     run ruff format --check"
	@echo "  typecheck  run mypy (strict)"
	@echo "  demo       analyze the sample data against the live Samples API"

install:
	python3 -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format --check .

typecheck:
	$(PYTHON) -m mypy mini_nucleiq

check: lint format typecheck test

demo:
	$(PYTHON) -m examples.demo
