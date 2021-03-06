# NUCLEI

[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

This repository is created by [CEMS BV](https://cemsbv.nl/) and helps the user to access and process API calls to the [NUCLEI](https://crux-nuclei.com/) environment.

## Installation

To install a package in this repository run:

`$ pip install cems-nuclei`

Please note that to use `GeoDataFrames` from the `geopandas` library `cems-nuclei[geo]` should be installed.

## ENV VARS

To use `nuclei` add the follow ENV vars to your environment. Or provide them when asked.

```
* NUCLEI_USER
    - Your NUCLEI user name
* NUCLEI_PASSWORD
    - Your NUCLEI user password
```


## Code quality tools

To maintain code quality we use `super-linter`.

```commandline

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

`pip install -r docs.requirements.txt`

Build the docs:

`sphinx-build -b html docs public`