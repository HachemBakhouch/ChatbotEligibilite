import json
import os
import re
from datetime import datetime


class EligibilityEvaluator:
    """Évalue l'éligibilité des utilisateurs basée sur les règles de l'arbre décisionnel"""

    def __init__(self, rules_file=None):
        """Initialiser avec un fichier de règles optionnel"""
        # Créer le répertoire rules s'il n'existe pas
        if not os.path.exists("../rules"):
            os.makedirs("../rules")

        self.rules_file = rules_file or os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "rules",
            "eligibility_rules.json",
        )
        self.rules = self._load_rules()
        self.user_data = {}  # Stocker temporairement les données utilisateur

    def _load_rules(self):
        """Charger les règles depuis le fichier JSON"""
        try:
            # Vérifier si le fichier existe
            if not os.path.exists(self.rules_file):
                # Créer le fichier avec les règles par défaut
                os.makedirs(os.path.dirname(self.rules_file), exist_ok=True)
                with open(self.rules_file, "w", encoding="utf-8") as f:
                    json.dump(
                        self._get_default_rules(), f, ensure_ascii=False, indent=2
                    )

            with open(
                self.rules_file, "r", encoding="utf-8-sig"
            ) as f:  # Utiliser utf-8-sig pour gérer le BOM
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des règles: {str(e)}")
            # Revenir aux règles par défaut
            return self._get_default_rules()

    def _get_default_rules(self):
        """Retourner les règles par défaut si le fichier ne peut pas être chargé"""
        return {
            "states": {
                "initial": {
                    "next": "consent",
                    "message": "Bonjour, je suis CODEE, votre assistant virtuel. Je suis là pour vous aider à déterminer votre éligibilité aux programmes sociaux. Quelques questions simples me permettront de vous orienter vers le dispositif le plus adapté à votre situation.",
                },
                "consent": {
                    "next": "age_verification",
                    "message": "Avant de commencer, je dois recueillir quelques informations personnelles pour déterminer votre éligibilité. Acceptez-vous que vos données soient traitées dans le cadre de cette évaluation ?",
                    "responses": {
                        "yes": {
                            "next": "age_verification",
                            "message": "Merci. Commençons par votre âge. Quel âge avez-vous ?",
                        },
                        "no": {
                            "next": "end",
                            "message": "Je comprends. Sans ces informations, je ne peux pas déterminer votre éligibilité. N'hésitez pas à revenir si vous changez d'avis.",
                            "is_final": True,
                        },
                    },
                },
                "age_verification": {
                    "next": "rsa_verification",
                    "message": "Quel âge avez-vous ?",
                    "process": "extract_age",
                    "transitions": [
                        {
                            "condition": "age < 16",
                            "next": "not_eligible_age",
                            "message": "Je suis désolé, mais vous devez avoir au moins 16 ans pour être éligible aux programmes.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (âge)",
                        },
                        {
                            "condition": "age >= 16 and age <= 25.5",
                            "next": "rsa_verification_young",
                            "message": "Êtes-vous bénéficiaire du RSA ?",
                        },
                        {
                            "condition": "age > 25.5 and age < 62",
                            "next": "rsa_verification_adult",
                            "message": "Êtes-vous bénéficiaire du RSA ?",
                        },
                        {
                            "condition": "age >= 62",
                            "next": "not_eligible_age",
                            "message": "Je suis désolé, mais vous devez avoir moins de 62 ans pour être éligible aux programmes.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (âge)",
                        },
                    ],
                },
                "rsa_verification": {
                    "next": "schooling_verification",
                    "message": "Êtes-vous bénéficiaire du RSA ?",
                    "responses": {
                        "yes": {
                            "next": "schooling_verification_young_rsa",
                            "message": "Êtes-vous scolarisé actuellement ?",
                        },
                        "no": {
                            "next": "schooling_verification_young_no_rsa",
                            "message": "Êtes-vous scolarisé actuellement ?",
                        },
                    },
                },
                "rsa_verification_young": {
                    "next": "schooling_verification_young",
                    "message": "Êtes-vous bénéficiaire du RSA ?",
                    "responses": {
                        "yes": {
                            "next": "schooling_verification_young_rsa",
                            "message": "Êtes-vous scolarisé actuellement ?",
                        },
                        "no": {
                            "next": "schooling_verification_young_no_rsa",
                            "message": "Êtes-vous scolarisé actuellement ?",
                        },
                    },
                },
                "schooling_verification_young_rsa": {
                    "next": "city_verification_young_rsa",
                    "message": "Êtes-vous scolarisé actuellement ?",
                    "responses": {
                        "yes": {
                            "next": "city_verification_young_rsa",
                            "message": "Dans quelle ville habitez-vous ?",
                        },
                        "no": {
                            "next": "city_verification_young_rsa",
                            "message": "Dans quelle ville habitez-vous ?",
                        },
                    },
                },
                "city_verification_young_rsa": {
                    "next": "result",
                    "message": "Dans quelle ville habitez-vous ?",
                    "process": "extract_city",
                    "transitions": [
                        {
                            "condition": "city in ['saint-denis', 'stains', 'pierrefitte']",
                            "next": "eligible_ali",
                            "message": "Vous êtes éligible au programme ALI (Accompagnement Logement Insertion). Souhaitez-vous que je génère un rapport détaillé ?",
                            "is_final": True,
                            "eligibility_result": "ALI",
                        },
                        {
                            "condition": "True",
                            "next": "not_eligible_city",
                            "message": "Je suis désolé, mais vous n'êtes pas éligible aux programmes sociaux dans votre ville actuelle.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        },
                    ],
                },
                "schooling_verification_young_no_rsa": {
                    "next": "city_verification_young_no_rsa",
                    "message": "Êtes-vous scolarisé actuellement ?",
                    "responses": {
                        "yes": {
                            "next": "not_eligible_schooling",
                            "message": "Je suis désolé, mais vous n'êtes pas éligible aux programmes si vous êtes scolarisé et ne bénéficiez pas du RSA.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (scolarisation)",
                        },
                        "no": {
                            "next": "city_verification_young_no_rsa",
                            "message": "Dans quelle ville habitez-vous ?",
                        },
                    },
                },
                "city_verification_young_no_rsa": {
                    "next": "result",
                    "message": "Dans quelle ville habitez-vous ?",
                    "process": "extract_city",
                    "transitions": [
                        {
                            "condition": "city in ['saint-denis', 'pierrefitte', 'saint-ouen', 'epinay', 'épinay', 'villetaneuse', 'ile-saint-denis', 'île-saint-denis']",
                            "next": "eligible_ml",
                            "message": "Vous êtes éligible au programme ML (Mission Locale). Souhaitez-vous que je génère un rapport détaillé ?",
                            "is_final": True,
                            "eligibility_result": "ML",
                        },
                        {
                            "condition": "True",
                            "next": "not_eligible_city",
                            "message": "Je suis désolé, mais vous n'êtes pas éligible aux programmes sociaux dans votre ville actuelle.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        },
                    ],
                },
                "rsa_verification_adult": {
                    "next": "schooling_verification_adult",
                    "message": "Êtes-vous bénéficiaire du RSA ?",
                    "responses": {
                        "yes": {
                            "next": "schooling_verification_adult_rsa",
                            "message": "Êtes-vous scolarisé actuellement ?",
                        },
                        "no": {
                            "next": "schooling_verification_adult_no_rsa",
                            "message": "Êtes-vous scolarisé actuellement ?",
                        },
                    },
                },
                "schooling_verification_adult_rsa": {
                    "next": "city_verification_adult_rsa",
                    "message": "Êtes-vous scolarisé actuellement ?",
                    "responses": {
                        "yes": {
                            "next": "city_verification_adult_rsa",
                            "message": "Dans quelle ville habitez-vous ?",
                        },
                        "no": {
                            "next": "city_verification_adult_rsa",
                            "message": "Dans quelle ville habitez-vous ?",
                        },
                    },
                },
                "city_verification_adult_rsa": {
                    "next": "result",
                    "message": "Dans quelle ville habitez-vous ?",
                    "process": "extract_city",
                    "transitions": [
                        {
                            "condition": "city in ['saint-denis', 'stains', 'pierrefitte']",
                            "next": "eligible_ali",
                            "message": "Vous êtes éligible au programme ALI (Accompagnement Logement Insertion). Souhaitez-vous que je génère un rapport détaillé ?",
                            "is_final": True,
                            "eligibility_result": "ALI",
                        },
                        {
                            "condition": "True",
                            "next": "not_eligible_city",
                            "message": "Je suis désolé, mais vous n'êtes pas éligible aux programmes sociaux dans votre ville actuelle.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        },
                    ],
                },
                "schooling_verification_adult_no_rsa": {
                    "next": "city_verification_adult_no_rsa",
                    "message": "Êtes-vous scolarisé actuellement ?",
                    "responses": {
                        "yes": {
                            "next": "city_verification_adult_no_rsa",
                            "message": "Dans quelle ville habitez-vous ?",
                        },
                        "no": {
                            "next": "city_verification_adult_no_rsa",
                            "message": "Dans quelle ville habitez-vous ?",
                        },
                    },
                },
                "city_verification_adult_no_rsa": {
                    "next": "result",
                    "message": "Dans quelle ville habitez-vous ?",
                    "process": "extract_city",
                    "transitions": [
                        {
                            "condition": "city in ['aubervilliers', 'epinay-sur-seine', 'épinay-sur-seine', 'ile-saint-denis', 'île-saint-denis', 'la-courneuve', 'la courneuve', 'pierrefitte', 'saint-denis', 'saint-ouen', 'stains', 'villetaneuse']",
                            "next": "eligible_plie",
                            "message": "Vous êtes éligible au programme PLIE (Plan Local pour l'Insertion et l'Emploi). Souhaitez-vous que je génère un rapport détaillé ?",
                            "is_final": True,
                            "eligibility_result": "PLIE",
                        },
                        {
                            "condition": "True",
                            "next": "not_eligible_city",
                            "message": "Je suis désolé, mais vous n'êtes pas éligible aux programmes sociaux dans votre ville actuelle.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        },
                    ],
                },
                "eligible_ali": {
                    "message": "Vous êtes éligible au programme ALI (Accompagnement Logement Insertion). Souhaitez-vous que je génère un rapport détaillé ?",
                    "is_final": True,
                    "eligibility_result": "ALI",
                },
                "eligible_ml": {
                    "message": "Vous êtes éligible au programme ML (Mission Locale). Souhaitez-vous que je génère un rapport détaillé ?",
                    "is_final": True,
                    "eligibility_result": "ML",
                },
                "eligible_plie": {
                    "message": "Vous êtes éligible au programme PLIE (Plan Local pour l'Insertion et l'Emploi). Souhaitez-vous que je génère un rapport détaillé ?",
                    "is_final": True,
                    "eligibility_result": "PLIE",
                },
                "not_eligible_age": {
                    "message": "Je suis désolé, mais vous ne remplissez pas les critères d'âge pour être éligible aux programmes.",
                    "is_final": True,
                    "eligibility_result": "Non éligible (âge)",
                },
                "not_eligible_city": {
                    "message": "Je suis désolé, mais vous n'êtes pas éligible aux programmes sociaux dans votre ville actuelle.",
                    "is_final": True,
                    "eligibility_result": "Non éligible (ville)",
                },
                "not_eligible_schooling": {
                    "message": "Je suis désolé, mais vous n'êtes pas éligible aux programmes avec votre statut de scolarisation actuel.",
                    "is_final": True,
                    "eligibility_result": "Non éligible (scolarisation)",
                },
            }
        }

    def evaluate(self, conversation_id, current_state, nlp_data=None, user_data=None):
        """
        Évaluer l'état actuel et déterminer la prochaine étape

        Args:
            conversation_id (str): ID de la conversation
            current_state (str): État actuel dans l'arbre décisionnel
            nlp_data (dict): Résultats du traitement NLP
            user_data (dict): Données utilisateur collectées jusqu'à présent

        Returns:
            dict: Informations sur la prochaine étape
        """
        print(
            f"\nEvaluating - conversation_id: {conversation_id}, current_state: {current_state}"
        )
        if nlp_data:
            print(f"NLP data: {json.dumps(nlp_data)}")
        if user_data:
            print(f"User data: {json.dumps(user_data)}")

        # Mettre à jour les données utilisateur
        if user_data:
            if conversation_id not in self.user_data:
                self.user_data[conversation_id] = {}
            self.user_data[conversation_id].update(user_data)

        # Obtenir la définition de l'état actuel
        state_def = self.rules["states"].get(current_state)

        if not state_def:
            print(f"État non reconnu dans l'arbre de décision: {current_state}")
            return {
                "next_state": "error",
                "message": "État non reconnu dans l'arbre de décision.",
                "is_final": False,
            }

        print(f"État actuel: {current_state}, définition: {json.dumps(state_def)}")

        # Traiter la logique d'état spéciale si nécessaire
        if "process" in state_def:
            process_type = state_def["process"]
            print(f"Traitement spécial requis: {process_type}")

            # Utiliser à la fois nlp_data et user_data pour le traitement
            combined_data = {}
            if user_data:
                combined_data.update(user_data)

            # Le traitement peut ajouter de nouvelles données
            process_result = self._process_special_logic(
                process_type, nlp_data, combined_data
            )

            print(f"Résultats du traitement: {json.dumps(process_result)}")

            # Mettre à jour les données utilisateur avec les résultats du traitement
            if conversation_id not in self.user_data:
                self.user_data[conversation_id] = {}
            self.user_data[conversation_id].update(process_result)

            # Si user_data est fourni, mettre à jour combined_data
            combined_data.update(process_result)

            # Gérer les transitions basées sur le traitement
            if "transitions" in state_def:
                print(f"Évaluation des transitions...")
                for transition in state_def["transitions"]:
                    condition = transition["condition"]
                    print(f"Vérification de la condition: {condition}")

                    # Évaluer la condition avec les données combinées
                    if self._evaluate_condition(condition, combined_data):
                        print(
                            f"Condition satisfaite! Transition vers: {transition['next']}"
                        )
                        return {
                            "next_state": transition["next"],
                            "message": transition["message"],
                            "is_final": transition.get("is_final", False),
                            "eligibility_result": transition.get("eligibility_result"),
                        }
                    else:
                        print(f"Condition non satisfaite.")

        # Gérer les réponses directes si présentes
        if nlp_data and "responses" in state_def:
            intent = nlp_data.get("intent", "").lower()
            text = nlp_data.get("text", "").lower() if nlp_data else ""
            print(f"Vérification des réponses pour l'intention: {intent}")

            # Vérifier les intentions oui/non
            if (
                intent in ["yes", "affirm", "agree"]
                or "oui" in text.lower()
                or "d'accord" in text.lower()
                or "ok" in text.lower()
            ):
                if "yes" in state_def["responses"]:
                    response = state_def["responses"]["yes"]
                    print(
                        f"Réponse 'oui' détectée, transition vers: {response['next']}"
                    )
                    return {
                        "next_state": response["next"],
                        "message": response["message"],
                        "is_final": response.get("is_final", False),
                        "eligibility_result": response.get("eligibility_result"),
                    }
            elif (
                intent in ["no", "deny", "disagree"]
                or "non" in text.lower()
                or "pas" in text.lower()
            ):
                if "no" in state_def["responses"]:
                    response = state_def["responses"]["no"]
                    print(
                        f"Réponse 'non' détectée, transition vers: {response['next']}"
                    )
                    return {
                        "next_state": response["next"],
                        "message": response["message"],
                        "is_final": response.get("is_final", False),
                        "eligibility_result": response.get("eligibility_result"),
                    }

        # Rechercher d'autres entités dans les données
        if nlp_data and "entities" in nlp_data:
            entities = nlp_data["entities"]

            # Traitement spécial pour l'âge si nous sommes dans l'état age_verification
            if current_state == "age_verification" and "age" in entities:
                age = entities["age"]
                print(f"Âge détecté: {age}")

                # Déterminer la prochaine étape en fonction de l'âge
                if age < 16:
                    return {
                        "next_state": "not_eligible_age",
                        "message": "Je suis désolé, mais vous devez avoir au moins 16 ans pour être éligible aux programmes.",
                        "is_final": True,
                        "eligibility_result": "Non éligible (âge)",
                    }
                elif age <= 25.5:
                    return {
                        "next_state": "rsa_verification_young",
                        "message": "Êtes-vous bénéficiaire du RSA ?",
                        "is_final": False,
                    }
                elif age < 62:
                    return {
                        "next_state": "rsa_verification_adult",
                        "message": "Êtes-vous bénéficiaire du RSA ?",
                        "is_final": False,
                    }
                else:
                    return {
                        "next_state": "not_eligible_age",
                        "message": "Je suis désolé, mais vous devez avoir moins de 62 ans pour être éligible aux programmes.",
                        "is_final": True,
                        "eligibility_result": "Non éligible (âge)",
                    }

        # État suivant par défaut
        print(f"Transition par défaut vers: {state_def.get('next', current_state)}")
        return {
            "next_state": state_def.get("next", current_state),
            "message": state_def.get("message", "Comment puis-je vous aider ?"),
            "is_final": state_def.get("is_final", False),
            "eligibility_result": state_def.get("eligibility_result"),
        }

    def get_rules(self):
        """Retourner les règles actuelles"""
        return self.rules

    def _process_special_logic(self, process_type, nlp_data, existing_data=None):
        """Traiter la logique spéciale basée sur le type de processus"""
        result = {}
        if existing_data:
            result.update(existing_data)

        if process_type == "extract_age":
            # D'abord vérifier si l'âge est déjà dans les données existantes
            if existing_data and "age" in existing_data:
                print(f"Âge déjà présent dans les données: {existing_data['age']}")
                result["age"] = existing_data["age"]
                return result

            # Sinon, extraire l'âge des données NLP ou du message utilisateur
            entities = nlp_data.get("entities", {})

            if "age" in entities:
                age = entities["age"]
                result["age"] = age
                print(f"Âge extrait des entités NLP: {age}")
            else:
                # Essayer d'extraire du texte brut
                text = nlp_data.get("text", "").lower()
                print(f"Tentative d'extraction d'âge du texte: '{text}'")

                try:
                    # Trouver le premier nombre dans le texte
                    age_match = re.search(r"\d+", text)
                    if age_match:
                        age = int(age_match.group())
                        result["age"] = age
                        print(f"Âge extrait du texte (chiffres): {age}")
                    else:
                        # Tenter de trouver des nombres écrits en toutes lettres
                        number_words = {
                            "dix-huit": 18,
                            "dix huit": 18,
                            "dixhuit": 18,
                            "vingt": 20,
                            "vingt et un": 21,
                            "vingt-et-un": 21,
                            "vingt-deux": 22,
                            "vingt deux": 22,
                            "vingt-trois": 23,
                            "vingt trois": 23,
                            "vingt-quatre": 24,
                            "vingt quatre": 24,
                            "vingt-cinq": 25,
                            "vingt cinq": 25,
                            "vingt-six": 26,
                            "vingt six": 26,
                            "vingt-sept": 27,
                            "vingt sept": 27,
                            "vingt-huit": 28,
                            "vingt huit": 28,
                            "vingt-neuf": 29,
                            "vingt neuf": 29,
                            "trente": 30,
                            "trente-cinq": 35,
                            "trente cinq": 35,
                            "quarante": 40,
                            "cinquante": 50,
                        }

                        for word, value in number_words.items():
                            if word in text:
                                result["age"] = value
                                print(f"Âge extrait du texte (mots): {value}")
                                break
                        else:
                            print(f"Aucun âge trouvé dans le texte")
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'âge: {str(e)}")

        elif process_type == "extract_city":
            # D'abord vérifier si la ville est déjà dans les données existantes
            if existing_data and "city" in existing_data:
                print(f"Ville déjà présente dans les données: {existing_data['city']}")
                result["city"] = existing_data["city"].lower()
                return result

            # Extraire la ville des données NLP
            entities = nlp_data.get("entities", {})

            if "city" in entities:
                city = entities["city"]
                result["city"] = city.lower()
                print(f"Ville extraite des entités NLP: {city}")
            else:
                # Essayer d'extraire du texte brut
                text = nlp_data.get("text", "").lower()
                print(f"Tentative d'extraction de ville du texte: '{text}'")

                cities = [
                    "saint-denis",
                    "st-denis",
                    "saint denis",
                    "st denis",
                    "stains",
                    "pierrefitte",
                    "pierfitte",
                    "pierrefite",
                    "saint-ouen",
                    "st-ouen",
                    "saint ouen",
                    "st ouen",
                    "epinay",
                    "épinay",
                    "epinay-sur-seine",
                    "épinay-sur-seine",
                    "villetaneuse",
                    "ile-saint-denis",
                    "île-saint-denis",
                    "ile saint denis",
                    "île saint denis",
                    "aubervilliers",
                    "la-courneuve",
                    "la courneuve",
                    "montfermeil",
                ]

                # Normalisation des variantes de noms de villes vers leur forme standard
                city_mapping = {
                    "st-denis": "saint-denis",
                    "saint denis": "saint-denis",
                    "st denis": "saint-denis",
                    "pierfitte": "pierrefitte",
                    "pierrefite": "pierrefitte",
                    "st-ouen": "saint-ouen",
                    "saint ouen": "saint-ouen",
                    "st ouen": "saint-ouen",
                    "epinay": "épinay-sur-seine",
                    "épinay": "épinay-sur-seine",
                    "epinay-sur-seine": "épinay-sur-seine",
                    "ile-saint-denis": "île-saint-denis",
                    "ile saint denis": "île-saint-denis",
                    "île saint denis": "île-saint-denis",
                    "la courneuve": "la-courneuve",
                }

                for city in cities:
                    if city in text or city.replace("-", " ") in text:
                        # Normaliser le nom de la ville si nécessaire
                        normalized_city = city_mapping.get(city, city)
                        result["city"] = normalized_city
                        print(
                            f"Ville extraite du texte: {city} (normalisée en: {normalized_city})"
                        )
                        break
                else:
                    print(f"Aucune ville reconnue dans le texte")

        return result

    def _evaluate_condition(self, condition, data):
        """Évaluer une condition par rapport aux données"""
        print(
            f"Évaluation de la condition: '{condition}' avec les données: {json.dumps(data)}"
        )

        try:
            # Cas spécial pour la condition "True"
            if condition == "True":
                return True

            # Cas spécial pour vérifier si une valeur est dans une liste
            if " in [" in condition and "]" in condition:
                # Extraire la variable et la liste
                var_name, list_str = condition.split(" in ", 1)
                var_name = var_name.strip()

                if var_name in data:
                    # Normaliser la valeur entrée
                    city_value = (
                        data[var_name].lower() if var_name == "city" else data[var_name]
                    )

                    # Évaluer la liste (en supposant qu'elle est correctement formatée)
                    list_value = eval(list_str, {"__builtins__": {}})

                    # Pour les villes, vérifier avec plus de flexibilité
                    if var_name == "city":
                        # Définir des mappings pour normaliser les noms de villes
                        city_normalization = {
                            "saint-denis": [
                                "saint-denis",
                                "saint denis",
                                "st-denis",
                                "st denis",
                            ],
                            "stains": ["stains"],
                            "pierrefitte": ["pierrefitte", "pierrefite", "pierfitte"],
                            "saint-denis": [
                                "saint-denis",
                                "saint denis",
                                "st-denis",
                                "st denis",
                            ],
                            "stains": ["stains"],
                            "pierrefitte": ["pierrefitte", "pierrefite", "pierfitte"],
                            "saint-ouen": [
                                "saint-ouen",
                                "saint ouen",
                                "st-ouen",
                                "st ouen",
                            ],
                            "épinay-sur-seine": [
                                "épinay-sur-seine",
                                "epinay-sur-seine",
                                "épinay",
                                "epinay",
                            ],
                            "villetaneuse": ["villetaneuse"],
                            "île-saint-denis": [
                                "île-saint-denis",
                                "ile-saint-denis",
                                "île saint denis",
                                "ile saint denis",
                            ],
                            "aubervilliers": ["aubervilliers"],
                            "la-courneuve": ["la-courneuve", "la courneuve"],
                        }

                        # Vérifier si la ville entrée correspond à l'une des villes normalisées dans la liste
                        for listed_city in list_value:
                            listed_city_lower = listed_city.lower()
                            # Vérification directe
                            if city_value == listed_city_lower:
                                return True

                            # Vérifier les variantes connues
                            for standard_city, variants in city_normalization.items():
                                if (
                                    listed_city_lower in variants
                                    and city_value in variants
                                ):
                                    print(
                                        f"Ville '{city_value}' reconnue comme variante de '{standard_city}' qui est dans la liste"
                                    )
                                    return True

                        print(
                            f"Ville '{city_value}' non trouvée dans les variantes reconnues"
                        )
                        return False
                    else:
                        # Pour les autres variables, vérification standard
                        result = data[var_name] in list_value
                        print(
                            f"Évaluation standard 'in': {data[var_name]} in {list_value} => {result}"
                        )
                        return result
                else:
                    print(
                        f"Variable '{var_name}' requise pour 'in' mais absente des données!"
                    )
                    return False

            # Créer un contexte d'évaluation sécurisé pour les autres conditions
            eval_context = {}

            # Ajouter les données au contexte
            for key, value in data.items():
                eval_context[key] = value
                print(f"Variable ajoutée au contexte: {key} = {value}")

            # Vérifier si toutes les variables requises sont présentes
            for var_name in re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b", condition):
                if (
                    var_name not in eval_context
                    and var_name != "True"
                    and var_name != "False"
                    and var_name != "and"
                    and var_name != "or"
                    and var_name != "in"
                    and var_name != "not"
                ):
                    print(
                        f"ATTENTION: Variable '{var_name}' requise dans la condition mais absente des données!"
                    )
                    return False

            # Évaluer la condition dans un environnement sécurisé
            result = eval(condition, {"__builtins__": {}}, eval_context)
            print(f"Résultat de l'évaluation: {result}")
            return result
        except Exception as e:
            print(f"Erreur lors de l'évaluation de la condition: {str(e)}")
            if condition == "True":  # Fallback pour la condition "True"
                print(f"Condition 'True' évaluée par défaut à True")
                return True
            return False
