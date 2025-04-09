#!/bin/bash

# API Gateway
cat > api_gateway/Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
EOF

# Chatbot Service
cat > chatbot_service/Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
EOF

# STT Service
cat > stt_service/Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5002
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app"]
EOF

# NLP Service
cat > nlp_service/Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5003
CMD ["gunicorn", "--bind", "0.0.0.0:5003", "app:app"]
EOF

# Decision Tree Service
cat > decision_tree_service/Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5004
CMD ["gunicorn", "--bind", "0.0.0.0:5004", "app:app"]
EOF

# PDF Service
cat > pdf_service/Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
COPY . /app/
RUN mkdir -p output
RUN mkdir -p templates
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5005
CMD ["gunicorn", "--bind", "0.0.0.0:5005", "app:app"]
EOF
