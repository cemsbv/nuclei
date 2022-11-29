# NUCLEI

[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

This repository is created by [CEMS BV](https://cemsbv.nl/) and helps the user to access and process API calls to the [NUCLEI](https://nuclei.cemsbv.io/#/) environment.

## Installation

To install a package in this repository run:

`$ pip install cems-nuclei`

Please note that to use `NucleiClient` library `cems-nuclei[client]` should be installed.

## ENV VARS

To use `nuclei` add the follow ENV vars to your environment. Or provide them when asked.

```
* NUCLEI_TOKEN
    - Your NUCLEI user token
```

You can obtain your `NUCLEI_TOKEN` on [NUCLEI](https://nuclei.cemsbv.io/#/). 
Go to `personal-access-tokens` and create a new user token.

## Code quality tools

To maintain code quality we use `super-linter`.

```bash

docker pull github/super-linter:latest
docker run -e RUN_LOCAL=true \
-e VALIDATE_PYTHON_PYLINT=false \
-e VALIDATE_MARKDOWN=false \
-e VALIDATE_JSCPD=false \
-e VALIDATE_CSS=false \
-e VALIDATE_YAML=false \
-e VALIDATE_PYTHON_FLAKE8=false \
-v $PWD:/tmp/lint github/super-linter

```

## Documentation

Install the requirements:

```bash

  pip install -r docs.requirements.txt

```

Build the docs:

```bash

    sphinx-build -b html docs public

```

## Dependencies

```bash

pip-compile --extra=client --output-file=requirements.txt requirements.in setup.py

```