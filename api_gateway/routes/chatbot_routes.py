from flask import Blueprint, request, jsonify
import requests
from config.config import Config
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/start", methods=["POST"])
def start_conversation():
    """Start a new chatbot conversation"""
    try:
        # Récupérer l'identifiant du device mobile le cas échéant
        data = request.json
        device_id = data.get("device_id")
        if device_id:
            logger.info(f"Starting conversation for mobile device: {device_id}")

        # Forward request to chatbot service
        response = requests.post(
            f"{Config.CHATBOT_SERVICE_URL}/conversation", json=request.json
        )

        result = response.json()

        # Ajouter des métadonnées pour le client mobile
        if response.status_code == 200:
            result["mobile_metadata"] = {"api_version": "1.0", "supports_audio": True}

        return jsonify(result), response.status_code
    except Exception as e:
        logger.error(f"Error starting conversation: {str(e)}")
        return (
            jsonify(
                {
                    "error": str(e),
                    "mobile_friendly_message": "Impossible de démarrer la conversation. Veuillez réessayer.",
                }
            ),
            500,
        )


@chatbot_bp.route("/process", methods=["POST"])
def process_input():
    """Process user input (text or audio)"""
    try:
        data = request.json
        conversation_id = data.get("conversation_id")

        if not conversation_id:
            return (
                jsonify(
                    {
                        "error": "Missing conversation_id",
                        "mobile_friendly_message": "Identifiant de conversation manquant",
                    }
                ),
                400,
            )

        # Handle audio input
        if "audio" in data:
            logger.info(f"Processing audio input for conversation: {conversation_id}")

            # Informations supplémentaires sur l'audio pour mobile
            audio_format = data.get("audio_format", "wav")  # Format par défaut
            language = data.get("language", "fr")  # Langue par défaut

            # Forward to STT service
            stt_response = requests.post(
                f"{Config.STT_SERVICE_URL}/transcribe",
                json={
                    "audio": data["audio"],
                    "language": language,
                    "format": audio_format,
                },
            )

            if stt_response.status_code != 200:
                logger.error(f"Failed to transcribe audio: {stt_response.text}")
                return (
                    jsonify(
                        {
                            "error": "Failed to transcribe audio",
                            "mobile_friendly_message": "Impossible de transcrire l'audio. Veuillez réessayer.",
                        }
                    ),
                    400,
                )

            text_input = stt_response.json().get("text")

            # Pour le mobile, on renvoie aussi la transcription
            transcription = text_input
        else:
            text_input = data.get("text", "")
            transcription = None

            if not text_input:
                return (
                    jsonify(
                        {
                            "error": "Missing text input",
                            "mobile_friendly_message": "Message texte vide",
                        }
                    ),
                    400,
                )

        # Forward to chatbot service for processing
        response = requests.post(
            f"{Config.CHATBOT_SERVICE_URL}/process",
            json={"conversation_id": conversation_id, "text": text_input},
        )

        # Enrichir la réponse pour le mobile
        if response.status_code == 200:
            result = response.json()

            # Ajouter la transcription si disponible
            if transcription:
                result["transcription"] = transcription

            # Ajouter des métadonnées utiles pour le mobile
            result["mobile_metadata"] = {
                "timestamp": int(__import__("time").time()),
                "message_type": "audio" if "audio" in data else "text",
            }

            return jsonify(result), 200
        else:
            logger.error(f"Error from chatbot service: {response.text}")
            return jsonify(response.json()), response.status_code

    except Exception as e:
        logger.error(f"Error processing input: {str(e)}")
        return (
            jsonify(
                {
                    "error": str(e),
                    "mobile_friendly_message": "Impossible de traiter votre message. Veuillez réessayer.",
                }
            ),
            500,
        )


@chatbot_bp.route("/conversation/<conversation_id>", methods=["GET"])
def get_conversation(conversation_id):
    """Get conversation history - useful for mobile to sync conversation state"""
    try:
        response = requests.get(
            f"{Config.CHATBOT_SERVICE_URL}/conversation/{conversation_id}"
        )

        if response.status_code == 200:
            result = response.json()

            # Optimiser les données pour mobile (moins de données à transférer)
            if request.args.get("mobile") == "true":
                # Ne garder que les messages et le statut d'éligibilité
                compact_result = {
                    "messages": result.get("messages", []),
                    "eligibility_result": result.get("eligibility_result"),
                    "current_state": result.get("current_state"),
                }
                return jsonify(compact_result), 200

            return jsonify(result), 200
        else:
            return (
                jsonify({"error": "Failed to retrieve conversation"}),
                response.status_code,
            )

    except Exception as e:
        logger.error(f"Error retrieving conversation: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Route pour vérifier l'état de la connexion mobile
@chatbot_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for mobile client"""
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "chatbot-api",
                "timestamp": int(__import__("time").time()),
            }
        ),
        200,
    )
