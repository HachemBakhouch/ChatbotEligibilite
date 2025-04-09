#!/bin/bash

# Navigate to the project directory
cd /opt/chatbot-eligibilite

# Inspect NLP service
echo "Inspecting NLP Service Contents:"
echo "----------------------------"

echo "Dockerfile:"
cat nlp_service/Dockerfile

echo -e "\n\nrequirements.txt:"
cat nlp_service/requirements.txt

echo -e "\n\napp.py:"
cat nlp_service/app.py

echo -e "\n\nDocker Compose Configuration:"
grep -A 10 "nlp-service:" docker-compose.yml

echo -e "\n\nInstalled Python Packages:"
docker-compose run --rm nlp-service pip freeze | grep -E "flask|werkzeug"

echo -e "\n\nContainer Environment:"
docker-compose run --rm nlp-service env
