# Makefile to setup and run the healthcare system app

.PHONY: setup run check-python-version clean

VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

check-python-version:
	@echo "Checking Python version..."
	@python -c 'import sys; assert sys.version_info >= (3, 10), "Python 3.10 or higher is required";'

setup: check-python-version
	@echo "Creating virtual environment..."
	python -m venv $(VENV)
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

run: check-python-version
	@echo "Starting FastAPI server..."
	$(PYTHON) -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
