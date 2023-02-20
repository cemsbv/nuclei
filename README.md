# NUCLEI

[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)


This repository is created by [CEMS BV](https://cemsbv.nl/) and helps the user to access and process API calls to the [NUCLEI](https://nuclei.cemsbv.io/#/) environment.

# Installation

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

# Contribution

## Environment

We recommend developing in Python3.8 with a clean virtual environment (using `virtualenv` or `conda`), installing the requirements from the requirements.txt file:

Example using `virtualenv` and `pip` to install the dependencies in a new environment .env on Linux:

```bash
python -m venv .env
source activate .env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Dependencies
To keep all dependencies nicely pinned, we use pip-tools to create the requirements.txt file: 

```bash
pip-compile --extra=client --output-file=requirements.txt requirements.in setup.py
```

## Code quality tools

To maintain code quality we use the Gitlab `super-linter`.

To run the linters locally, run the `run_super_linters.sh` bash script from the root directory:

```bash

./run_super_linter.sh

```

*Note: this requires `docker` to be installed.*

For first-time use, set the correct permissions with:

```bash

chmod u+x run_super_linter.sh

```



## Documentation


Build the docs:

```bash

sphinx-build -b html docs public

```