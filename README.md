# Chatbot d'Ã‰ligibilitÃ© aux Programmes Sociaux

Ce projet implÃ©mente un chatbot intelligent capable de dÃ©terminer l'Ã©ligibilitÃ© des utilisateurs Ã  diffÃ©rents programmes sociaux (ALI, PLIE, ML) via des conversations vocales et textuelles.

## Architecture

Le systÃ¨me est basÃ© sur une architecture microservices:

- **API Gateway**: Point d'entrÃ©e unique pour toutes les requÃªtes client
- **Chatbot Service**: GÃ¨re la logique de conversation et l'Ã©tat
- **STT Service**: Service de reconnaissance vocale (Speech-to-Text)
- **NLP Service**: Traitement du langage naturel pour l'analyse d'intention et d'entitÃ©s
- **Decision Tree Service**: Applique la logique d'arbre dÃ©cisionnel pour dÃ©terminer l'Ã©ligibilitÃ©
- **PDF Service**: GÃ©nÃ¨re des rapports PDF Ã  partir des rÃ©sultats

## Installation

1. Cloner le dÃ©pÃ´t
2. Installer les dÃ©pendances pour chaque service:
   ```
   pip install -r [service]/requirements.txt
   ```
3. Configurer les variables d'environnement (voir .env.example)
4. Lancer les services individuellement ou via Docker Compose

## Utilisation

Le chatbot peut Ãªtre intÃ©grÃ© dans:
- Une application web PHP Symfony
- Une application mobile Ionic
- Un site web WordPress

Pour plus de dÃ©tails sur l'API, consulter la documentation dans le dossier `/docs`.

## DÃ©veloppement

Pour contribuer au projet:
1. Forker le dÃ©pÃ´t
2. CrÃ©er une branche pour votre fonctionnalitÃ©
3. Soumettre une pull request

## Licence

Confidentiel - Tous droits rÃ©servÃ©s
