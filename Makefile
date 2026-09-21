# Contributor entry points. `make check` is the one to run before opening a PR.

PYTHON ?= python3
SLUG ?=

.PHONY: help install validate links build check clean

help:
	@echo "make install   install the Python dependencies"
	@echo "make check     validate the data and confirm the generated files are in sync"
	@echo "make build     regenerate README.md and the exports"
	@echo "make validate  schema and scope rules only"
	@echo "make links     fetch the URLs in one category: make links SLUG=threat-intelligence"

install:
	$(PYTHON) -m pip install -r requirements.txt

validate:
	$(PYTHON) scripts/validate.py

build:
	$(PYTHON) scripts/build.py

check: validate
	$(PYTHON) scripts/build.py --check

links:
ifeq ($(SLUG),)
	$(PYTHON) scripts/check_links.py
else
	$(PYTHON) scripts/check_links.py --only $(SLUG)
endif

clean:
	rm -rf scripts/__pycache__
