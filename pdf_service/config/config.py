import os


class Config:
    # Server configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5005))
    DEBUG = os.getenv("DEBUG", "False") == "True"  # Changer True en False

    # PDF configuration
    PDF_OUTPUT_DIR = os.getenv(
        "PDF_OUTPUT_DIR",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "output"),
    )
    # Utiliser le nom du service Docker au lieu de l'IP
    PUBLIC_URL = os.getenv("PUBLIC_URL", "http://pdf-service:5005")

    # Template configuration
    TEMPLATE_DIR = os.getenv(
        "TEMPLATE_DIR",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
    )
