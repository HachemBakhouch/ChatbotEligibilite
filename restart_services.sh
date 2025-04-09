#!/bin/bash

# Exit on any error
set -e

# Navigate to the project directory
cd /opt/chatbot-eligibilite

# Ensure .env file exists and has required variables
if [ ! -f .env ]; then
    echo "Creating .env file"
    touch .env
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY" .env; then
    echo "WARNING: OPENAI_API_KEY is not set in .env file"
fi

# Prune docker system to remove old containers and images
docker system prune -f

# Remove existing containers
docker-compose down || true

# Update requirements
./update_requirements.sh

# Rebuild services with no cache
docker-compose build --no-cache

# Start services
docker-compose up -d

# Show service status
docker-compose ps

# Check logs for any persistent issues
echo "Checking logs:"
docker-compose logs
