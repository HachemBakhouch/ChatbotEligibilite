FROM python:3.9-slim

WORKDIR /app

# Copier les fichiers de l'application web
COPY . /app/

# Installer Flask pour servir l'application web
RUN pip install flask flask-cors

# Exposer le port 8080
EXPOSE 8080

# Commande pour démarrer le serveur
CMD ["python", "server.py"]