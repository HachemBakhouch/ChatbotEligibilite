import os


class Config:
    # Server configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5001))
    DEBUG = os.getenv("DEBUG", "False") == "True"  # Changer True en False

    # Service URLs - utiliser les noms des services Docker
    NLP_SERVICE_URL = os.getenv("NLP_SERVICE_URL", "http://nlp-service:5003")
    DECISION_TREE_SERVICE_URL = os.getenv(
        "DECISION_TREE_SERVICE_URL", "http://decision-tree-service:5004"
    )
    PDF_SERVICE_URL = os.getenv("PDF_SERVICE_URL", "http://pdf-service:5005")
    STT_SERVICE_URL = os.getenv("STT_SERVICE_URL", "http://stt-service:5002")

    # Database configuration (for future use)
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///chatbot.db")
