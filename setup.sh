#!/usr/bin/env bash

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
export FLASK_APP=main.py
export APP_ENV=development
export FLASK_RUN_PORT=8080
export FLASK_RUN_HOST=0.0.0.0   # To allow external routing to the application for development
