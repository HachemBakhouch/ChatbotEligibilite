#!/bin/bash

# Navigate to the NLP service directory
cd nlp_service

# Check and modify app.py to handle Werkzeug import
sed -i 's/from werkzeug.urls import url_quote/from werkzeug.utils import escape as url_quote/g' app.py

# Return to the original directory
cd ..

# Rebuild and restart the NLP service
docker-compose build nlp-service
docker-compose up -d nlp-service

# Show service status
docker-compose ps
