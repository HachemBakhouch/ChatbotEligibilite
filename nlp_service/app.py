from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from processors.openai_processor import OpenAIProcessor

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)


# Configuration
class Config:
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5003))
    DEBUG = os.getenv("DEBUG", "True") == "True"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "default-key")


# Initialiser le processeur NLP
nlp_processor = OpenAIProcessor(api_key=Config.OPENAI_API_KEY)


@app.route("/process", methods=["POST"])
def process_text():
    """Process text for intent and entity extraction"""
    try:
        data = request.json

        if "text" not in data:
            return jsonify({"error": "No text provided"}), 400

        text = data["text"]
        language = data.get("language", "fr")

        # Process using the NLP processor
        result = nlp_processor.analyze(text, language)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "nlp-service"}), 200


if __name__ == "__main__":
    # Assurez-vous que les répertoires nécessaires existent
    os.makedirs("processors", exist_ok=True)

    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
