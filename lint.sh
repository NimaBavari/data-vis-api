#!/bin/bash
isort -rc src/
autoflake -r --in-place --remove-unused-variables src/
black -l 120 src/
flake8 --max-line-length 120 src/