#!/bin/bash

# Exit on any error
set -e

# Navigate to the project directory
cd /opt/chatbot-eligibilite

# Function to check and modify app.py
fix_werkzeug_import() {
    local service_dir=$1
    local app_path="${service_dir}/app.py"
    
    if [ -f "$app_path" ]; then
        echo "Checking $app_path for Werkzeug import"
        if grep -q "from werkzeug.urls import url_quote" "$app_path"; then
            echo "Replacing Werkzeug import in $app_path"
            sed -i 's/from werkzeug.urls import url_quote/from werkzeug.utils import escape as url_quote/g' "$app_path"
        fi
    fi
}

# Services to process
SERVICES=(
    "nlp_service"
    "api_gateway"
    "chatbot_service"
    "decision_tree_service"
    "stt_service"
)

# Fix Werkzeug imports
for service in "${SERVICES[@]}"; do
    fix_werkzeug_import "$service"
done

# Prune docker system to remove old containers and images
docker system prune -f

# Remove existing containers
docker-compose down

# Rebuild services
docker-compose build

# Start services
docker-compose up -d

# Show service status
docker-compose ps

# Check logs for any persistent issues
echo "Checking logs for NLP service:"
docker-compose logs nlp-service
