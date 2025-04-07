@echo off
echo Arrêt de tous les services Docker...
cd deployment\docker
docker-compose down
echo Services arrêtés.
pause