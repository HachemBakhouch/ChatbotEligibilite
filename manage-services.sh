#!/bin/bash

# Script pour gérer tous les services Docker

# Vérifier si Docker est installé
if ! [ -x "$(command -v docker)" ]; then
  echo 'Erreur: Docker n'"'"'est pas installé.' >&2
  exit 1
fi

# Vérifier si Docker Compose est installé
if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Erreur: Docker Compose n'"'"'est pas installé.' >&2
  exit 1
fi

# Fonction pour afficher l'aide
show_help() {
  echo "Usage: $0 [option]"
  echo "Options:"
  echo "  start       Démarrer tous les services"
  echo "  stop        Arrêter tous les services"
  echo "  restart     Redémarrer tous les services"
  echo "  status      Afficher l'état de tous les services"
  echo "  logs        Afficher les logs de tous les services"
  echo "  build       Reconstruire tous les services"
  echo "  clean       Nettoyer toutes les ressources (containers, images, volumes)"
  echo "  help        Afficher cette aide"
}

# Vérifier si un argument a été fourni
if [ $# -lt 1 ]; then
  show_help
  exit 1
fi

# Définir le répertoire du docker-compose.yml
COMPOSE_DIR="deployment/docker"

# Fonction pour exécuter une commande docker-compose
run_compose() {
  cd "$COMPOSE_DIR" || { echo "Erreur: Impossible d'accéder au répertoire $COMPOSE_DIR"; exit 1; }
  docker-compose "$@"
}

# Traiter l'argument
case "$1" in
  start)
    echo "Démarrage de tous les services..."
    run_compose up -d
    echo "Tous les services sont démarrés."
    ;;
  stop)
    echo "Arrêt de tous les services..."
    run_compose down
    echo "Tous les services sont arrêtés."
    ;;
  restart)
    echo "Redémarrage de tous les services..."
    run_compose restart
    echo "Tous les services sont redémarrés."
    ;;
  status)
    echo "État de tous les services:"
    run_compose ps
    ;;
  logs)
    echo "Logs de tous les services:"
    run_compose logs -f
    ;;
  build)
    echo "Reconstruction de tous les services..."
    run_compose build
    echo "Tous les services sont reconstruits."
    ;;
  clean)
    echo "Nettoyage de toutes les ressources..."
    run_compose down -v --rmi all
    echo "Toutes les ressources sont nettoyées."
    ;;
  help)
    show_help
    ;;
  *)
    echo "Option invalide: $1"
    show_help
    exit 1
    ;;
esac

exit 0