@echo off
echo Démarrage de tous les services Docker...
cd deployment\docker
docker-compose up -d
echo Services démarrés.
pause