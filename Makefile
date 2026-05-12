PYTHON := .venv/bin/python
PYTEST := .venv/bin/pytest

.PHONY: bootstrap verify test test-patch test-research

bootstrap:
	./scripts/bootstrap.sh

verify:
	$(PYTHON) scripts/verify_setup.py

test:
	$(MAKE) test-patch
	$(MAKE) test-research

test-patch:
	$(PYTEST) -q tests/patch_tests

test-research:
	$(PYTEST) -q tests/research_tests
