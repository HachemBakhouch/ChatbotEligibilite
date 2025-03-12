# Chatbot d'Éligibilité aux Programmes Sociaux

Ce projet implémente un chatbot intelligent capable de déterminer l'éligibilité des utilisateurs à différents programmes sociaux (ALI, PLIE, ML) via des conversations vocales et textuelles.

## Architecture
Le système est basé sur une architecture microservices:
- **API Gateway**: Point d'entrée unique pour toutes les requêtes client
- **Chatbot Service**: Gère la logique de conversation et l'état
- **STT Service**: Service de reconnaissance vocale (Speech-to-Text)
- **NLP Service**: Traitement du langage naturel pour l'analyse d'intention et d'entités
- **Decision Tree Service**: Applique la logique d'arbre décisionnel pour déterminer l'éligibilité
- **PDF Service**: Génère des rapports PDF à partir des résultats

## Installation
1. Cloner le dépôt
2. Installer les dépendances pour chaque service:
   ```
   pip install -r [service]/requirements.txt
   ```
3. Configurer les variables d'environnement (voir .env.example)
4. Lancer les services individuellement ou via Docker Compose

## Utilisation
Le chatbot peut être intégré dans:
- Une application web PHP Symfony
- Une application mobile Ionic
- Un site web WordPress

Pour plus de détails sur l'API, consulter la documentation dans le dossier `/docs`.

## Développement
Pour contribuer au projet:
1. Forker le dépôt
2. Créer une branche pour votre fonctionnalité
3. Soumettre une pull request

## Licence
Confidentiel - Tous droits réservés
