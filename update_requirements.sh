#!/bin/bash

# Services list
SERVICES=(
    "api_gateway"
    "chatbot_service"
    "decision_tree_service"
    "nlp_service"
    "stt_service"
)

# Function to update requirements
update_requirements() {
    local service_dir=$1
    
    # Create or update requirements.txt
    cat > "$service_dir/requirements.txt" << EOL
Flask==2.2.5
flask-cors
gunicorn==20.1.0
Werkzeug==2.2.3
requests
jsonschema
python-dotenv
openai
EOL

    # Update Dockerfile if necessary
    if [ -f "$service_dir/Dockerfile" ]; then
        # Simplify Dockerfile pip install command
        sed -i 's/pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt/pip install --no-cache-dir -r requirements.txt/g' "$service_dir/Dockerfile"
    fi
}

# Main script
for service in "${SERVICES[@]}"; do
    service_dir="./${service}"
    if [ -d "$service_dir" ]; then
        echo "Updating requirements for $service"
        update_requirements "$service_dir"
    else
        echo "Directory $service_dir not found"
    fi
done

echo "Requirements update complete."
