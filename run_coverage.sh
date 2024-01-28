#!/usr/bin/env bash
# This script pytests and runs the coverage report for the project

coverage run -m pytest
coverage report --omit="*/test*,*/__init__.py,database.py,*/conftest.py"