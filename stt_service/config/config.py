import os


class Config:
    # Server configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5002))
    DEBUG = os.getenv("DEBUG", "False") == "True"  # Changer True en False

    # OpenAI API configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
