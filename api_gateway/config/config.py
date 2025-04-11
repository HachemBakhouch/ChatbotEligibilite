import os


class Config:
    # API Gateway configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "False") == "True"  # Changer True en False

    # Service URLs - Utiliser les noms des services Docker
    CHATBOT_SERVICE_URL = os.getenv(
        "CHATBOT_SERVICE_URL", "http://chatbot-service:5001"
    )
    STT_SERVICE_URL = os.getenv("STT_SERVICE_URL", "http://stt-service:5002")
    NLP_SERVICE_URL = os.getenv("NLP_SERVICE_URL", "http://nlp-service:5003")
    DECISION_TREE_SERVICE_URL = os.getenv(
        "DECISION_TREE_SERVICE_URL", "http://decision-tree-service:5004"
    )
    # PDF_SERVICE_URL = os.getenv("PDF_SERVICE_URL", "http://pdf-service:5005")

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key-here")
