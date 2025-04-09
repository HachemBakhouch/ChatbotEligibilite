#!/bin/bash

# Exit on any error
set -e

# Navigate to the project directory
cd /opt/chatbot-eligibilite

# Stop and remove the NLP service container
docker-compose stop nlp-service
docker-compose rm -f nlp-service

# Rebuild the NLP service with verbose output
docker-compose build --no-cache nlp-service

# Start the NLP service with interactive mode to see full error
docker-compose run --rm nlp-service /bin/bash -c "
    pip install -r requirements.txt &&
    python -m pip install --upgrade pip &&
    python -c 'import flask; import flask_cors; import werkzeug; print(flask.__version__, flask_cors.__version__, werkzeug.__version__)' &&
    gunicorn --bind 0.0.0.0:5003 app:app
"
