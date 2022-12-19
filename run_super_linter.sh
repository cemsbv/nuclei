#!/bin/bash

docker pull github/super-linter@v4
docker run -e RUN_LOCAL=true \
-e VALIDATE_PYTHON_PYLINT=false \
-e VALIDATE_MARKDOWN=false \
-e VALIDATE_JSCPD=false \
-e VALIDATE_CSS=false \
-e VALIDATE_YAML=false \
-e VALIDATE_PYTHON_FLAKE8=false \
-e LINTER_RULES_PATH=/ \
-e PYTHON_ISORT_CONFIG_FILE=pyproject.toml \
-e PYTHON_MYPY_CONFIG_FILE=.mypy.ini \
-v $PWD:/tmp/lint github/super-linter