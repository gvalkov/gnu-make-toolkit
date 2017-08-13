PYTHON ?= python3
CMD_EXTRACT_DOCS := ./docs/extract-toolkit-docs.py
CMD_EXPAND_DOCS := ./docs/expand-toolkit-docs.py

include toolkit.mk

test tests:
	py.test -v -n $$(nproc) --basetemp=/dev/shm/gnu-make-toolkit

docs/docs.json: toolkit.mk $(CMD_EXTRACT_DOCS) Makefile
	$(CMD_EXTRACT_DOCS) < $< > $@

docs/docs/ref.md: $(CMD_EXPAND_DOCS) docs/docs/ref.tmpl.md docs/docs.json
	$(CMD_EXPAND_DOCS) $(call rest,$^) > $@

docs: docs/mkdocs.yml docs/docs/ref.md
	cd docs && $(PYTHON) -m mkdocs build

test-requirements:
	$(PYTHON) -m pip install pytest pytest-xdist

doc-requirements:
	$(PYTHON) -m pip install mkdocs mkdocs-material pygments pymdown-extensions

install-requirements: test-requirements doc-requirements

.PHONY: docs test tests %-requirements
