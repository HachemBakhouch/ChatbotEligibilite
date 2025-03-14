from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
from generators.pdf_generator import PDFGenerator
from config.config import Config

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

pdf_generator = PDFGenerator()


@app.route("/generate", methods=["POST"])
def generate_pdf():
    """Generate a PDF report from conversation data"""
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Generate PDF
        filename = f"eligibility_report_{str(uuid.uuid4())[:8]}.pdf"
        filepath = os.path.join(Config.PDF_OUTPUT_DIR, filename)

        # Ensure output directory exists
        os.makedirs(Config.PDF_OUTPUT_DIR, exist_ok=True)

        pdf_generator.generate(data, filepath)

        # Return file URL
        file_url = f"{Config.PUBLIC_URL}/reports/{filename}"

        return (
            jsonify({"status": "success", "file_url": file_url, "filename": filename}),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/reports/<filename>", methods=["GET"])
def get_report(filename):
    """Serve a generated PDF report"""
    try:
        filepath = os.path.join(Config.PDF_OUTPUT_DIR, filename)

        if not os.path.exists(filepath):
            return jsonify({"error": "Report not found"}), 404

        return send_file(filepath, mimetype="application/pdf")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "pdf-service"}), 200


if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs(Config.PDF_OUTPUT_DIR, exist_ok=True)

    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
