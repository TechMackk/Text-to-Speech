PYTHON ?= python
PIP ?= $(PYTHON) -m pip

.PHONY: setup test build install-local clean smoke

setup:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && $(PIP) install --upgrade pip build
	. .venv/bin/activate && $(PIP) install -r requirements.txt

install-local:
	$(PIP) install -e .

test:
	$(PYTHON) -m unittest discover -s tests

build:
	$(PYTHON) -m build

smoke:
	tts --list-voices

clean:
	rm -rf .venv dist build *.egg-info __pycache__ .pytest_cache
