from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import sys

app = Flask(__name__, static_folder=".", static_url_path="")
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

print(f"Répertoire de travail: {os.getcwd()}")
files = os.listdir(".")
print(f"Fichiers dans le répertoire: {files}")


@app.route("/")
def index():
    print("Requête reçue sur '/'")
    try:
        return send_from_directory(".", "index.html")
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return f"Erreur: {str(e)}", 500


@app.route("/<path:path>")
def serve_static(path):
    print(f"Requête reçue pour: {path}")
    return send_from_directory(".", path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Démarrage du serveur sur {host}:{port}...")
    app.run(host=host, port=port, debug=True)
