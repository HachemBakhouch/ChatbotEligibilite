from flask import Blueprint, request, jsonify
import requests
from config.config import Config

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/start", methods=["POST"])
def start_conversation():
    """Start a new chatbot conversation"""
    try:
        # Forward request to chatbot service
        response = requests.post(
            f"{Config.CHATBOT_SERVICE_URL}/conversation", json=request.json
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/process", methods=["POST"])
def process_input():
    """Process user input (text or audio)"""
    try:
        data = request.json
        conversation_id = data.get("conversation_id")

        # Handle audio input
        if "audio" in data:
            # Forward to STT service
            stt_response = requests.post(
                f"{Config.STT_SERVICE_URL}/transcribe", json={"audio": data["audio"]}
            )

            if stt_response.status_code != 200:
                return jsonify({"error": "Failed to transcribe audio"}), 400

            text_input = stt_response.json().get("text")
        else:
            text_input = data.get("text", "")

        # Forward to chatbot service for processing
        response = requests.post(
            f"{Config.CHATBOT_SERVICE_URL}/process",
            json={"conversation_id": conversation_id, "text": text_input},
        )

        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    """Generate PDF report based on conversation"""
    try:
        data = request.json
        conversation_id = data.get("conversation_id")

        # Get conversation data and eligibility result
        conversation_response = requests.get(
            f"{Config.CHATBOT_SERVICE_URL}/conversation/{conversation_id}"
        )

        if conversation_response.status_code != 200:
            return jsonify({"error": "Failed to retrieve conversation data"}), 400

        # Forward to PDF service
        pdf_response = requests.post(
            f"{Config.PDF_SERVICE_URL}/generate", json=conversation_response.json()
        )

        return jsonify(pdf_response.json()), pdf_response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
