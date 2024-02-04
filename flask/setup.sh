#!/usr/bin/env bash
# This script sets up the project for development

# Create a virtual environment for dependencies
if [ ! -d venv ]
then
  python -m venv venv
fi
. venv/Scripts/activate

# install requirements
python -m pip install -r requirements.txt
# To generate a new requirements.txt file, run "pip freeze > requirements.txt"

export FLASK_DEBUG=1
export FLASK_APP=wsgi.py
export APP_ENV=development
export FLASK_RUN_PORT=5000
export FLASK_RUN_HOST=0.0.0.0   # To allow external routing to the application for development
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/gabduel