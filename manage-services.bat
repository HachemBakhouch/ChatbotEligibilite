@echo off
setlocal

REM Script pour gérer tous les services Docker sur Windows

REM Vérifier si Docker est installé
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Erreur: Docker n'est pas installé ou n'est pas dans le PATH.
  exit /b 1
)

REM Vérifier si Docker Compose est installé
where docker-compose >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Erreur: Docker Compose n'est pas installé ou n'est pas dans le PATH.
  exit /b 1
)

REM Fonction pour afficher l'aide
:show_help
if "%~1"=="" (
  echo Usage: %0 [option]
  echo Options:
  echo   start       Démarrer tous les services
  echo   stop        Arrêter tous les services
  echo   restart     Redémarrer tous les services
  echo   status      Afficher l'état de tous les services
  echo   logs        Afficher les logs de tous les services
  echo   build       Reconstruire tous les services
  echo   clean       Nettoyer toutes les ressources (containers, images, volumes)
  echo   help        Afficher cette aide
  exit /b 1
)

REM Définir le répertoire du docker-compose.yml
set COMPOSE_DIR=deployment\docker

REM Vérifier si le répertoire existe
if not exist "%COMPOSE_DIR%" (
  echo Erreur: Le répertoire %COMPOSE_DIR% n'existe pas.
  exit /b 1
)

REM Traiter l'argument
if "%~1"=="start" (
  echo Démarrage de tous les services...
  cd "%COMPOSE_DIR%" && docker-compose up -d
  echo Tous les services sont démarrés.
) else if "%~1"=="stop" (
  echo Arrêt de tous les services...
  cd "%COMPOSE_DIR%" && docker-compose down
  echo Tous les services sont arrêtés.
) else if "%~1"=="restart" (
  echo Redémarrage de tous les services...
  cd "%COMPOSE_DIR%" && docker-compose restart
  echo Tous les services sont redémarrés.
) else if "%~1"=="status" (
  echo État de tous les services:
  cd "%COMPOSE_DIR%" && docker-compose ps
) else if "%~1"=="logs" (
  echo Logs de tous les services:
  cd "%COMPOSE_DIR%" && docker-compose logs -f
) else if "%~1"=="build" (
  echo Reconstruction de tous les services...
  cd "%COMPOSE_DIR%" && docker-compose build
  echo Tous les services sont reconstruits.
) else if "%~1"=="clean" (
  echo Nettoyage de toutes les ressources...
  cd "%COMPOSE_DIR%" && docker-compose down -v --rmi all
  echo Toutes les ressources sont nettoyées.
) else if "%~1"=="help" (
  goto :show_help
) else (
  echo Option invalide: %~1
  goto :show_help
)

exit /b 0