#!/bin/bash

# Navigate to the NLP service directory
cd nlp_service

# Check the contents of requirements.txt
echo "Requirements:"
cat requirements.txt

# Check the contents of app.py
echo -e "\n\nApp.py contents:"
cat app.py

# Run pip freeze to check installed packages
echo -e "\n\nInstalled Packages:"
docker-compose run --rm nlp-service pip freeze

# Check the Dockerfile
echo -e "\n\nDockerfile:"
cat ../nlp_service/Dockerfile

# Get the full logs for the NLP service
echo -e "\n\nDocker Compose Logs:"
docker-compose logs nlp-service
