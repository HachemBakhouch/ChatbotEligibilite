from flask import Flask, request, jsonify
from flask_cors import CORS
from core.conversation_manager import ConversationManager
from config.config import Config

print(f"Config has STT_SERVICE_URL: {'STT_SERVICE_URL' in dir(Config)}")
print(f"Available Config attributes: {dir(Config)}")
import requests

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
)  # Activer CORS pour toutes les routes

conversation_manager = ConversationManager()


@app.route("/conversation", methods=["POST"])
def start_conversation():
    """Start a new conversation session"""
    try:
        data = request.json
        user_id = data.get("user_id", "anonymous")

        # Create new conversation
        conversation_id = conversation_manager.create_conversation(user_id)

        # Get initial message
        initial_message = conversation_manager.get_welcome_message()

        return (
            jsonify({"conversation_id": conversation_id, "message": initial_message}),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/process", methods=["POST"])
def process_message():
    """Process a message in an existing conversation"""
    try:
        data = request.json
        conversation_id = data.get("conversation_id")
        text = data.get("text")

        if not conversation_id or not text:
            return jsonify({"error": "Missing conversation_id or text"}), 400

        # Process the message through conversation manager
        response = conversation_manager.process_message(conversation_id, text)

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/conversation/<conversation_id>", methods=["GET"])
def get_conversation(conversation_id):
    """Get conversation data"""
    try:
        conversation = conversation_manager.get_conversation(conversation_id)

        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        return jsonify(conversation), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/process-audio", methods=["POST"])
def process_audio():
    """Process audio input"""
    try:
        print("Received audio processing request")
        data = request.json
        conversation_id = data.get("conversation_id")
        audio_data = data.get("audio")

        print(f"Conversation ID: {conversation_id}")
        print(f"Audio data length: {len(audio_data) if audio_data else 'None'}")

        if not conversation_id or not audio_data:
            return jsonify({"error": "Missing conversation_id or audio data"}), 400

        # URL du service STT codée en dur pour contourner le problème de Config
        stt_service_url = "http://192.168.100.104:5002"
        print(f"Using hardcoded STT Service URL: {stt_service_url}")

        try:
            # Transcribe audio using STT service
            stt_response = requests.post(
                f"{stt_service_url}/transcribe",
                json={"audio": audio_data, "language": "fr"},
            )

            if stt_response.status_code != 200:
                print(f"STT service error: {stt_response.text}")
                # Utiliser un texte par défaut en cas d'erreur
                text = "Message vocal reçu mais non transcrit."
            else:
                text = stt_response.json().get("text", "")
                print(f"Transcribed text: {text}")
        except Exception as stt_err:
            print(f"Error during STT request: {str(stt_err)}")
            # Utiliser un texte par défaut en cas d'erreur
            text = "Message vocal reçu mais erreur lors de la transcription."

        # Process the transcribed text
        response = conversation_manager.process_message(conversation_id, text)

        # Include transcription in response
        response["transcription"] = text

        return jsonify(response), 200
    except Exception as e:
        print(f"Error in process_audio: {str(e)}")
        import traceback

        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    """Generate PDF report for conversation"""
    try:
        data = request.json
        conversation_id = data.get("conversation_id")

        if not conversation_id:
            return jsonify({"error": "Missing conversation_id"}), 400

        # Get conversation data
        conversation = conversation_manager.get_conversation(conversation_id)

        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        # Forward to PDF service
        pdf_response = requests.post(
            f"{Config.PDF_SERVICE_URL}/generate", json=conversation
        )

        if pdf_response.status_code != 200:
            return (
                jsonify(
                    {
                        "error": f"Failed to generate PDF: {pdf_response.status_code} - {pdf_response.text}"
                    }
                ),
                500,
            )

        pdf_data = pdf_response.json()

        return (
            jsonify(
                {
                    "status": "success",
                    "file_url": pdf_data.get("file_url"),
                    "filename": pdf_data.get("filename"),
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
