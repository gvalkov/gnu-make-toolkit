docs/docs.json: toolkit.mk
	./extract-function-docs.py < $^ > $@

test:
	py.test -v -n $$(nproc) --basetemp=/dev/shm/gnu-make-toolkit

install-requirements:
	python3 -m pip install pytest pytest-xdist

