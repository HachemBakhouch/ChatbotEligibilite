import os


class Config:
    # Server configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5005))
    DEBUG = os.getenv("DEBUG", "True") == "True"

    # PDF configuration
    PDF_OUTPUT_DIR = os.getenv(
        "PDF_OUTPUT_DIR",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "output"),
    )
    PUBLIC_URL = os.getenv(
        "PUBLIC_URL", "http://192.168.100.104:5005"
    )  # L'URL publique pour accéder aux fichiers PDF

    # Template configuration
    TEMPLATE_DIR = os.getenv(
        "TEMPLATE_DIR",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
    )
