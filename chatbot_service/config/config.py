import os

class Config:
    # Server configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5001))
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Service URLs - assurez-vous que cette adresse est correcte
    NLP_SERVICE_URL = os.getenv('NLP_SERVICE_URL', 'http://localhost:5003')
    DECISION_TREE_SERVICE_URL = os.getenv('DECISION_TREE_SERVICE_URL', 'http://192.168.100.104:5004')
    
    # Database configuration (for future use)
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///chatbot.db')