from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Assurez-vous que les chemins sont corrects
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import après avoir ajusté les chemins
from config.config import Config
from evaluators.eligibility_evaluator import EligibilityEvaluator

# Créer l'application Flask
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

# Créer une instance de l'évaluateur d'éligibilité
evaluator = EligibilityEvaluator()


@app.route("/evaluate", methods=["POST"])
def evaluate_decision():
    """Évaluer l'état actuel et déterminer la prochaine étape"""
    try:
        data = request.json

        conversation_id = data.get("conversation_id")
        current_state = data.get("current_state")
        nlp_data = data.get("nlp_data", {})
        user_data = data.get("user_data", {})

        if not conversation_id or not current_state:
            return (
                jsonify(
                    {"error": "Paramètres conversation_id ou current_state manquants"}
                ),
                400,
            )

        # Évaluer en utilisant l'évaluateur d'éligibilité
        result = evaluator.evaluate(
            conversation_id=conversation_id,
            current_state=current_state,
            nlp_data=nlp_data,
            user_data=user_data,
        )

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/rules", methods=["GET"])
def get_rules():
    """Obtenir les règles de l'arbre décisionnel actuelles"""
    try:
        rules = evaluator.get_rules()
        return jsonify(rules), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Vérifier l'état de santé du service"""
    return jsonify({"status": "healthy", "service": "decision-tree-service"}), 200


@app.route("/", methods=["GET"])
def index():
    """Page d'accueil simple pour les tests"""
    return (
        jsonify(
            {
                "service": "Decision Tree Service",
                "status": "running",
                "endpoints": [
                    "/evaluate - POST - Évaluer l'état actuel dans l'arbre décisionnel",
                    "/rules - GET - Obtenir les règles de l'arbre décisionnel",
                    "/health - GET - Vérifier l'état de santé du service",
                ],
            }
        ),
        200,
    )


@app.route("/debug", methods=["GET"])
def debug_tree():
    """Route de débogage pour tester les transitions"""
    try:
        # Créer un évaluateur temporaire
        temp_evaluator = EligibilityEvaluator()

        # Tester les transitions problématiques
        results = {
            "rsa_verification_adult_yes": temp_evaluator.evaluate(
                conversation_id="debug",
                current_state="rsa_verification_adult",
                nlp_data={"intent": "yes", "text": "Oui"},
            ),
            "rsa_verification_adult_no": temp_evaluator.evaluate(
                conversation_id="debug",
                current_state="rsa_verification_adult",
                nlp_data={"intent": "no", "text": "Non"},
            ),
            "rsa_verification_young_yes": temp_evaluator.evaluate(
                conversation_id="debug",
                current_state="rsa_verification_young",
                nlp_data={"intent": "yes", "text": "Oui"},
            ),
            "rsa_verification_young_no": temp_evaluator.evaluate(
                conversation_id="debug",
                current_state="rsa_verification_young",
                nlp_data={"intent": "no", "text": "Non"},
            ),
        }

        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
