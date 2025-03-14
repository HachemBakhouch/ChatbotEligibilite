from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from config.config import Config
import requests
import base64
import json
import tempfile

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "allow_headers": "*",
            "methods": ["GET", "POST", "OPTIONS"],
        }
    },
)

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", Config.OPENAI_API_KEY)


@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    """Transcribe audio to text"""
    try:
        print("Received transcription request")
        data = request.json

        if "audio" not in data:
            return jsonify({"error": "No audio data provided"}), 400

        audio_data = data["audio"]
        language = data.get("language", "fr")

        print(f"Audio data length: {len(audio_data) if audio_data else 'None'}")
        print(f"Language: {language}")

        # Decode base64 audio
        try:
            audio_bytes = base64.b64decode(audio_data)
            print(f"Decoded audio bytes length: {len(audio_bytes)}")
        except Exception as decode_err:
            print(f"Error decoding audio: {str(decode_err)}")
            return jsonify({"error": f"Error decoding audio: {str(decode_err)}"}), 400

        # Create a temporary file
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
                temp_file.write(audio_bytes)
                print(f"Temporary file created: {temp_filename}")
        except Exception as file_err:
            print(f"Error creating temporary file: {str(file_err)}")
            return (
                jsonify({"error": f"Error creating temporary file: {str(file_err)}"}),
                500,
            )

        # Prepare the request to OpenAI Whisper API
        api_url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

        # For debugging, check if the file exists and its size
        print(f"File exists: {os.path.exists(temp_filename)}")
        print(f"File size: {os.path.getsize(temp_filename)}")

        try:
            with open(temp_filename, "rb") as audio_file:
                files = {
                    "file": audio_file,
                    "model": (None, "whisper-1"),
                    "language": (None, language),
                }

                print("Sending request to OpenAI Whisper API...")
                response = requests.post(api_url, headers=headers, files=files)

                print(f"OpenAI response status: {response.status_code}")

                # Clean up the temporary file
                os.unlink(temp_filename)

                if response.status_code == 200:
                    result = response.json()
                    transcribed_text = result.get("text", "")
                    print(f"Transcribed text: {transcribed_text}")
                    return (
                        jsonify({"text": transcribed_text, "language": language}),
                        200,
                    )
                else:
                    print(f"OpenAI API error: {response.text}")
                    return (
                        jsonify(
                            {
                                "error": f"API error: {response.status_code} - {response.text}"
                            }
                        ),
                        500,
                    )
        except Exception as api_err:
            print(f"Error during API request: {str(api_err)}")
            import traceback

            print(traceback.format_exc())
            # Clean up the temporary file if it exists
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            return jsonify({"error": f"API request error: {str(api_err)}"}), 500
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        import traceback

        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "stt-service"}), 200


@app.route("/", methods=["GET"])
def index():
    """Root endpoint for testing"""
    return (
        jsonify(
            {
                "service": "Speech-to-Text Service",
                "status": "running",
                "endpoints": [
                    "/transcribe - POST - Transcribe audio to text",
                    "/health - GET - Health check",
                ],
            }
        ),
        200,
    )


if __name__ == "__main__":
    print(
        f"Starting STT service with API key: {OPENAI_API_KEY[:5]}..."
        if OPENAI_API_KEY
        else "Warning: No OpenAI API key found!"
    )
    print(f"Server will run on {Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
