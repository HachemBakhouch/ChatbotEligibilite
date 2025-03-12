from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from adapters.whisper_adapter import WhisperAdapter

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)


# Configuration
class Config:
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5002))
    DEBUG = os.getenv("DEBUG", "True") == "True"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "default-key")


# Initialiser l'adaptateur Whisper
stt_adapter = WhisperAdapter(api_key=Config.OPENAI_API_KEY)


@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    """Transcribe audio to text"""
    try:
        data = request.json

        if "audio" not in data:
            return jsonify({"error": "No audio data provided"}), 400

        audio_data = data["audio"]
        language = data.get("language", "fr")

        # Transcribe using the adapter
        text = stt_adapter.transcribe(audio_data, language)

        return jsonify({"text": text, "language": language}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "stt-service"}), 200


if __name__ == "__main__":
    # Assurez-vous que les répertoires nécessaires existent
    os.makedirs("adapters", exist_ok=True)

    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
