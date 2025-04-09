#!/bin/bash

# Exit on any error
set -e

# Navigate to the project directory
cd /opt/chatbot-eligibilite

# Restore docker-compose.yml
cp docker-compose.yml docker-compose.yml.bak
cat > docker-compose.yml << 'EOL'
version: '3'

services:
  api-gateway:
    build: ./api_gateway
    ports:
      - "5000:5000"
    environment:
      - CHATBOT_SERVICE_URL=http://chatbot-service:5001
      - STT_SERVICE_URL=http://stt-service:5002
      - NLP_SERVICE_URL=http://nlp-service:5003
      - DECISION_TREE_SERVICE_URL=http://decision-tree-service:5004
    restart: always
    depends_on:
      - chatbot-service
      - stt-service
      - nlp-service
      - decision-tree-service

  chatbot-service:
    build: ./chatbot_service
    ports:
      - "5001:5001"
    environment:
      - NLP_SERVICE_URL=http://nlp-service:5003
      - DECISION_TREE_SERVICE_URL=http://decision-tree-service:5004
    restart: always
    depends_on:
      - nlp-service
      - decision-tree-service

  stt-service:
    build: ./stt_service
    ports:
      - "5002:5002"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: always

  nlp-service:
    build: ./nlp_service
    ports:
      - "5003:5003"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: always

  decision-tree-service:
    build: ./decision_tree_service
    ports:
      - "5004:5004"
    restart: always

  web-client:
    build:
      context: ./web
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - API_BASE_URL=http://api-gateway:5000
    restart: always
    depends_on:
      - api-gateway
EOL

# Prune docker system to remove old containers and images
docker system prune -f

# Remove existing containers and images
docker-compose down --rmi all

# Update requirements for all services
./update_requirements.sh

# Rebuild services with no cache to ensure clean build
docker-compose build --no-cache

# Start services
docker-compose up -d

# Show service status
docker-compose ps

# Check logs for any persistent issues
echo "Checking logs for services:"
docker-compose logs
