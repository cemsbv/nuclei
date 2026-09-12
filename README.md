# NUCLEI

[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

This repository is created by [CEMS BV](https://cemsbv.nl/) and helps the user to access and process API calls to
the [NUCLEI](https://nuclei.cemsbv.io/#/) environment.

# Installation

To install this package, including the `NucleiClient` library and its dependencies, run:

```bash
pip install cems-nuclei[client]
```

To skip the installation of the `NucleiClient` library, in case you do not need it (e.g. only use pure requests), run:

```bash
pip install cems-nuclei
```

## ENV VARS

To use `nuclei` add the follow ENV vars to your environment. Or provide them when asked.

```
* NUCLEI_TOKEN
    - Your NUCLEI user token
```

You can obtain your `NUCLEI_TOKEN` on [NUCLEI](https://nuclei.cemsbv.io/#/).
Go to `Access token` and create a new user token.

# Contribution

## Environment

This project is managed with [uv](https://docs.astral.sh/uv/). Install uv, then sync the environment
(including all optional extras) and it will create a `.venv` for you:

```bash
uv sync --all-extras
```

## Documentation

Build the docs:

```bash
uv sync --extra docs --extra client
uv run sphinx-build -b html docs public
```

Note: You'll need to set the `NUCLEI_TOKEN` environmental variable.
You can get your token at: `https://cemsbv.crux-nuclei.com`

## Format

We format our code with black and isort.

```bash
uv run black --config "pyproject.toml" src/nuclei tests
uv run isort --settings-path "pyproject.toml" src/nuclei tests
```

## Lint

To maintain code quality we use the GitHub super-linter.

To run the linters locally, run the `run_super_linters.sh` bash script from the root directory.

## UnitTest

Test the software with the use of coverage:

```bash
uv sync --all-extras
uv run coverage run -m pytest
```

## Dependency lock file

Dependencies are locked in `uv.lock`. To update it after changing `pyproject.toml`, run:

```bash
uv lock
```
