# Development

To run the test suite and generate the documentation you need Python 3.

## Setup virtualenv

```shell
python3 -m vevn path/to/gmt-venv
source path/to/gmt-venv
```

## Install dependencies

```shell
cd path/to/gnu-make-toolkit
make install-requirements
```

## Run tests

The test suite uses [py.test] and some custom test fixtures (see
`tests/conftest.py` and `tests/make_runner.py`).

```shell
make tests
```


## Build documentation

The documentation is generated using [mkdocs]. The docstrings are extracted from
`toolkit.mk` with the help of these two helper scripts:

 - `docs/extract-toolkit-docs.py`: Parses the docstrings in `toolkit.mk` into `docs/docs.json`.

 - `docs/expand-toolkit-docs.py`: Renders the `docs/docs/ref.tmpl.mk` file to
   `docs/docs/ref.mk` (i.e the [Reference](ref.mk) page).


To generate the docs:

```shell
make docs
```


[mkdocs]:  http://www.mkdocs.org/
[py.test]: https://docs.pytest.org/en/latest/
