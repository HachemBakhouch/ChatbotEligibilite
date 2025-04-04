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
                    "message": "Bonjour et ravi de te voir ici ! Je suis CODEE, ton assistant intelligent prêt à t'aider. 🚀 Je suis là pour toi !",
                },
                "consent": {
                    "next": "age_verification",
                    "message": "Avant de commencer, je dois recueillir quelques informations personnelles pour déterminer votre éligibilité. Acceptez-vous que vos données soient traitées dans le cadre de cette évaluation ?",
                    "responses": {
                        "yes": {
                            "next": "age_verification",
                            "message": "Pour mieux t'orienter, peux tu me communiquer ton âge ? Cela m'aidera à te fournir des informations adaptées à ton profil. 😊",
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
                            "message": "D'accord, tu es scolarisé(e)?",
                        },
                        "no": {
                            "next": "schooling_verification_young_no_rsa",
                            "message": "D'accord, tu es scolarisé(e)?",
                        },
                    },
                },
                "rsa_verification_young": {
                    "next": "schooling_verification_young",
                    "message": "Êtes-vous bénéficiaire du RSA ?",
                    "responses": {
                        "yes": {
                            "next": "schooling_verification_young_rsa",
                            "message": "D'accord, tu es scolarisé(e)?",
                        },
                        "no": {
                            "next": "schooling_verification_young_no_rsa",
                            "message": "D'accord, tu es scolarisé(e)?",
                        },
                    },
                },
                "schooling_verification_young_rsa": {
                    "next": "city_verification_young_rsa",
                    "message": "D'accord, tu es scolarisé(e)?",
                    "responses": {
                        "yes": {
                            "next": "city_verification_young_rsa",
                            "message": "Pour mieux t'aider, peux tu me préciser ton code postal ou le nom de ta ville?",
                        },
                        "no": {
                            "next": "city_verification_young_rsa",
                            "message": "Pour mieux t'aider, peux tu me préciser ton code postal ou le nom de ta ville?",
                        },
                    },
                },
                "city_verification_young_rsa": {
                    "next": "result",
                    "message": "Pour mieux t'aider, peux tu me préciser ton code postal ou le nom de ta ville?",
                    "process": "extract_city",
                    "transitions": [
                        {
                            "condition": "city in ['saint-denis', 'stains', 'pierrefitte']",
                            "next": "eligible_ali",
                            "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par l'agence locale d'insertion de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. Cliquer ici pour prendre un rendez vous avec un conseiller",
                            "is_final": True,
                            "eligibility_result": "ALI",
                        },
                        {
                            "condition": "True",
                            "next": "not_eligible_city",
                            "message": "Important : Mon périmètre d'action est limité à la Plaine Commune et au département de la Seine-Saint-Denis (93). Pour ton cas, je te recommande de contacter les services de ta ville ou de ton département.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        },
                    ],
                },
                "schooling_verification_young_no_rsa": {
                    "next": "city_verification_young_no_rsa",
                    "message": "D'accord, tu es scolarisé(e)?D'accord, tu es scolarisé(e)?",
                    "responses": {
                        "yes": {
                            "next": "not_eligible_schooling",
                            "message": "Malheureusement, tu n’es pas éligible à un accompagnement pour le moment, tant que tu es encore scolarisé. 🎓 Cependant, dès que tu auras terminé tes études, tu pourras bénéficier de nos services d’accompagnement pour t'aider dans ta recherche d’emploi et ton insertion professionnelle. En attendant, si tu as des questions ou besoin de conseils, tu peux appeler CODEE au  0148131320. A bientôt",
                            "is_final": True,
                            "eligibility_result": "Non éligible (scolarisation)",
                        },
                        "no": {
                            "next": "city_verification_young_no_rsa",
                            "message": "Pour mieux t'aider, peux tu me préciser ton code postal ou le nom de ta ville?",
                        },
                    },
                },
                "city_verification_young_no_rsa": {
                    "next": "result",
                    "message": "Pour mieux t'aider, peux tu me préciser ton code postal ou le nom de ta ville?",
                    "process": "extract_city",
                    "transitions": [
                        {
                            "condition": "city in ['saint-denis', 'pierrefitte', 'saint-ouen', 'epinay', 'épinay', 'villetaneuse', 'ile-saint-denis', 'île-saint-denis']",
                            "next": "eligible_ml",
                            "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par la mission locale de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. Cliquer ici pour prendre un rendez vous avec un conseiller",
                            "is_final": True,
                            "eligibility_result": "ML",
                        },
                        {
                            "condition": "True",
                            "next": "not_eligible_city",
                            "message": "Important : Mon périmètre d'action est limité à la Plaine Commune et au département de la Seine-Saint-Denis (93). Pour ton cas, je te recommande de contacter les services de ta ville ou de ton département.",
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
                            "message": "D'accord, tu es scolarisé(e)?",
                        },
                        "no": {
                            "next": "schooling_verification_adult_no_rsa",
                            "message": "D'accord, tu es scolarisé(e)?",
                        },
                    },
                },
                "schooling_verification_adult_rsa": {
                    "next": "city_verification_adult_rsa",
                    "message": "D'accord, tu es scolarisé(e)?",
                    "responses": {
                        "yes": {
                            "next": "city_verification_adult_rsa",
                            "message": "Pour mieux t'aider, peux tu me préciser ton code postal ou le nom de ta ville?",
                        },
                        "no": {
                            "next": "city_verification_adult_rsa",
                            "message": "Pour mieux t'aider, peux tu me préciser ton code postal ou le nom de ta ville?",
                        },
                    },
                },
                "city_verification_adult_rsa": {
                    "next": "result",
                    "message": "Pour mieux t'aider, peux tu me préciser ton code postal ou le nom de ta ville?",
                    "process": "extract_city",
                    "transitions": [
                        {
                            "condition": "city in ['saint-denis', 'stains', 'pierrefitte']",
                            "next": "eligible_ali",
                            "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par l'agence locale d'insertion de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. Cliquer ici pour prendre un rendez vous avec un conseiller",
                            "is_final": True,
                            "eligibility_result": "ALI",
                        },
                        {
                            "condition": "True",
                            "next": "not_eligible_city",
                            "message": "Important : Mon périmètre d'action est limité à la Plaine Commune et au département de la Seine-Saint-Denis (93). Pour ton cas, je te recommande de contacter les services de ta ville ou de ton département.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        },
                    ],
                },
                "schooling_verification_adult_no_rsa": {
                    "next": "city_verification_adult_no_rsa",
                    "message": "D'accord, tu es scolarisé(e)?",
                    "responses": {
                        "yes": {
                            "next": "city_verification_adult_no_rsa",
                            "message": "Pour mieux t'aider, peux tu me préciser ton code postal ou le nom de ta ville?",
                        },
                        "no": {
                            "next": "city_verification_adult_no_rsa",
                            "message": "Pour mieux t'aider, peux tu me préciser ton code postal ou le nom de ta ville?",
                        },
                    },
                },
                "city_verification_adult_no_rsa": {
                    "next": "result",
                    "message": "Pour mieux t'aider, peux tu me préciser ton code postal ou le nom de ta ville?",
                    "process": "extract_city",
                    "transitions": [
                        {
                            "condition": "city in ['aubervilliers', 'epinay-sur-seine', 'épinay-sur-seine', 'ile-saint-denis', 'île-saint-denis', 'la-courneuve', 'la courneuve', 'pierrefitte', 'saint-denis', 'saint-ouen', 'stains', 'villetaneuse']",
                            "next": "eligible_plie",
                            "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par le PLIE de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. Cliquer ici pour prendre un rendez vous avec un conseiller",
                            "is_final": True,
                            "eligibility_result": "PLIE",
                        },
                        {
                            "condition": "True",
                            "next": "not_eligible_city",
                            "message": "Important : Mon périmètre d'action est limité à la Plaine Commune et au département de la Seine-Saint-Denis (93). Pour ton cas, je te recommande de contacter les services de ta ville ou de ton département.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        },
                    ],
                },
                "eligible_ali": {
                    "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par l'agence locale d'insertion de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. Cliquer ici pour prendre un rendez vous avec un conseiller",
                    "is_final": True,
                    "eligibility_result": "ALI",
                },
                "eligible_ml": {
                    "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par la mission locale de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. Cliquer ici pour prendre un rendez vous avec un conseiller",
                    "is_final": True,
                    "eligibility_result": "ML",
                },
                "eligible_plie": {
                    "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par le PLIE de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. Cliquer ici pour prendre un rendez vous avec un conseiller",
                    "is_final": True,
                    "eligibility_result": "PLIE",
                },
                "not_eligible_age": {
                    "message": "Je suis désolé, mais vous ne remplissez pas les critères d'âge pour être éligible aux programmes.",
                    "is_final": True,
                    "eligibility_result": "Non éligible (âge)",
                },
                "not_eligible_city": {
                    "message": "Important : Mon périmètre d'action est limité à la Plaine Commune et au département de la Seine-Saint-Denis (93). Pour ton cas, je te recommande de contacter les services de ta ville ou de ton département.",
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

        # Debug: Afficher l'état actuel des données utilisateur
        if conversation_id in self.user_data:
            print(
                f"DEBUG - Current user data: {json.dumps(self.user_data[conversation_id])}"
            )

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

            # Vérifier si le traitement a réussi à extraire l'information requise
            if process_type == "extract_age" and "age" not in process_result:
                # L'âge n'a pas pu être extrait, redemander
                return {
                    "next_state": current_state,  # Rester dans le même état
                    "message": "Je n'ai pas compris votre âge. Pourriez-vous me dire quel âge vous avez, en chiffres (par exemple 25) ou en lettres (par exemple trente ans) ?",
                    "is_final": False,
                }
            elif process_type == "extract_city" and "city" not in process_result:
                # La ville n'a pas pu être extraite, redemander
                return {
                    "next_state": current_state,  # Rester dans le même état
                    "message": "Je n'ai pas reconnu cette ville. Pourriez-vous préciser dans quelle ville vous habitez ? Par exemple : Saint-Denis, Stains, Pierrefitte, ou indiquer le code postal comme 93200.",
                    "is_final": False,
                }

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

        # Vérification RSA dans les états concernés
        if "rsa_verification" in current_state:
            text = nlp_data.get("text", "").lower() if nlp_data else ""
            intent = nlp_data.get("intent", "").lower() if nlp_data else ""
            rsa_detected = False

            # Détection explicite de la réponse "non"
            if "non" in text or intent == "no":
                # Forcer RSA à False
                if conversation_id not in self.user_data:
                    self.user_data[conversation_id] = {}
                self.user_data[conversation_id]["rsa"] = False
                rsa_detected = True

                # Forcer la transition vers l'état approprié
                if current_state == "rsa_verification_young":
                    print(
                        "*** Transition forcée vers schooling_verification_young_no_rsa ***"
                    )
                    return {
                        "next_state": "schooling_verification_young_no_rsa",
                        "message": "D'accord, tu es scolarisé(e)?",
                        "is_final": False,
                    }
            # Détection explicite de la réponse "oui"
            elif "oui" in text or intent == "yes" or "d'accord" in text or "ok" in text:
                # Forcer RSA à True
                if conversation_id not in self.user_data:
                    self.user_data[conversation_id] = {}
                self.user_data[conversation_id]["rsa"] = True
                rsa_detected = True

                # Forcer la transition vers l'état approprié
                if current_state == "rsa_verification_young":
                    print(
                        "*** Transition forcée vers schooling_verification_young_rsa ***"
                    )
                    return {
                        "next_state": "schooling_verification_young_rsa",
                        "message": "D'accord, tu es scolarisé(e)?",
                        "is_final": False,
                    }

            # Si les données RSA sont déjà présentes mais pas détectées dans le texte
            if not rsa_detected and "rsa" in self.user_data.get(conversation_id, {}):
                rsa_value = self.user_data[conversation_id]["rsa"]
                print(f"*** Utilisation de la valeur RSA existante: {rsa_value} ***")

                if current_state == "rsa_verification_young":
                    next_state = (
                        "schooling_verification_young_rsa"
                        if rsa_value
                        else "schooling_verification_young_no_rsa"
                    )
                    return {
                        "next_state": next_state,
                        "message": "D'accord, tu es scolarisé(e)?",
                        "is_final": False,
                    }

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
            else:
                # Si nous sommes dans un état qui attend une réponse oui/non mais qu'on n'a pas pu l'interpréter
                if "yes" in state_def["responses"] and "no" in state_def["responses"]:
                    return {
                        "next_state": current_state,  # Rester dans le même état
                        "message": "Je n'ai pas compris votre réponse. Pourriez-vous répondre simplement par oui ou par non ?",
                        "is_final": False,
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
                elif age < 64:
                    return {
                        "next_state": "rsa_verification_adult",
                        "message": "Êtes-vous bénéficiaire du RSA ?",
                        "is_final": False,
                    }
                else:
                    return {
                        "next_state": "not_eligible_age",
                        "message": "Je suis désolé, mais vous devez avoir moins de 64 ans pour être éligible aux programmes.",
                        "is_final": True,
                        "eligibility_result": "Non éligible (âge)",
                    }
            # Gérer le cas où on est dans un état qui nécessite l'âge mais qu'on ne l'a pas détecté
            elif current_state == "age_verification" and "age" not in entities:
                return {
                    "next_state": current_state,  # Rester dans le même état
                    "message": "Je n'ai pas compris votre âge. Pourriez-vous me dire quel âge vous avez en chiffres ?",
                    "is_final": False,
                }

            # Vérification scolarisation dans les états concernés
            if "schooling_verification" in current_state:
                schooling_detected = False
                text = nlp_data.get("text", "").lower() if nlp_data else ""
                intent = nlp_data.get("intent", "").lower() if nlp_data else ""

                if "schooling" in entities:
                    schooling_detected = True
                elif intent == "yes" or "oui" in text:
                    # Ajouter scolarisation aux données utilisateur si oui détecté
                    if conversation_id not in self.user_data:
                        self.user_data[conversation_id] = {}
                    self.user_data[conversation_id]["schooling"] = True
                    schooling_detected = True
                elif intent == "no" or "non" in text or "pas" in text:
                    # Ajouter scolarisation aux données utilisateur si non détecté
                    if conversation_id not in self.user_data:
                        self.user_data[conversation_id] = {}
                    self.user_data[conversation_id]["schooling"] = False
                    schooling_detected = True

                    # Traitement spécial pour jeune sans RSA et non scolarisé
                    if current_state == "schooling_verification_young_no_rsa":
                        print("*** Détecté: jeune, sans RSA, non scolarisé ***")
                        return {
                            "next_state": "city_verification_young_no_rsa",
                            "message": "Pour mieux t'aider, peux tu me préciser ton code postal ou le nom de ta ville?",
                            "is_final": False,
                        }

                if not schooling_detected:
                    # Scolarisation non détectée alors qu'on est dans un état qui l'attend
                    return {
                        "next_state": current_state,  # Rester dans le même état
                        "message": "Je n'ai pas compris si vous êtes actuellement scolarisé. Pourriez-vous répondre simplement par oui ou par non ?",
                        "is_final": False,
                    }

            # Vérification ville dans les états concernés
            if "city_verification" in current_state:
                # Vérifier d'abord les codes postaux directement
                text = nlp_data.get("text", "").lower() if nlp_data else ""
                code_postal_pattern = r"93\s*[0-9]{3}"

                # Tenter de trouver un code postal dans le texte
                import re

                code_match = re.search(code_postal_pattern, text)
                if code_match:
                    code_postal = code_match.group().replace(" ", "")

                    # Mappage des codes postaux
                    code_postal_mapping = {
                        "93200": "saint-denis",
                        "93240": "stains",
                        "93380": "pierrefitte",
                        "93400": "saint-ouen",
                        "93800": "épinay-sur-seine",
                        "93430": "villetaneuse",
                        "93450": "île-saint-denis",
                        "93300": "aubervilliers",
                        "93120": "la-courneuve",
                        "93370": "montfermeil",
                    }

                    if code_postal in code_postal_mapping:
                        # Ajouter la ville aux données utilisateur
                        if conversation_id not in self.user_data:
                            self.user_data[conversation_id] = {}
                        self.user_data[conversation_id]["city"] = code_postal_mapping[
                            code_postal
                        ]

                        # Traitement spécifique pour jeune non RSA non scolarisé
                        if current_state == "city_verification_young_no_rsa":
                            city = code_postal_mapping[code_postal]
                            ml_cities = [
                                "saint-denis",
                                "pierrefitte",
                                "saint-ouen",
                                "épinay-sur-seine",
                                "villetaneuse",
                                "île-saint-denis",
                            ]

                            if city in ml_cities:
                                print(
                                    f"*** Ville ML détectée via code postal: {city} ***"
                                )
                                return {
                                    "next_state": "eligible_ml",
                                    "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par la mission locale de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. Cliquer ici pour prendre un rendez vous avec un conseiller",
                                    "is_final": True,
                                    "eligibility_result": "ML",
                                }
                # Si aucun code postal n'a été détecté, vérifier si la ville est manquante
                elif "city" not in entities:
                    # Ville non détectée alors qu'on est dans un état qui l'attend
                    city_keywords = [
                        "saint-denis",
                        "st-denis",
                        "saint denis",
                        "stains",
                        "pierrefitte",
                        "pierrefitte-sur-seine",
                        "saint-ouen",
                        "st-ouen",
                        "saint ouen",
                        "épinay",
                        "epinay",
                        "épinay-sur-seine",
                        "villetaneuse",
                        "île-saint-denis",
                        "ile-saint-denis",
                        "île saint denis",
                        "aubervilliers",
                        "la courneuve",
                        "la-courneuve",
                        "montfermeil",
                    ]

                    # Vérifier si un mot-clé de ville est dans le texte
                    city_found = False
                    for city in city_keywords:
                        if city in text:
                            city_found = True
                            # Ajouter la ville normalisée aux données utilisateur
                            city_mapping = {
                                "saint denis": "saint-denis",
                                "st-denis": "saint-denis",
                                "st denis": "saint-denis",
                                "pierrefitte-sur-seine": "pierrefitte",
                                "pierfitte": "pierrefitte",
                                "pierrefite": "pierrefitte",
                                "saint ouen": "saint-ouen",
                                "st-ouen": "saint-ouen",
                                "st ouen": "saint-ouen",
                                "epinay": "épinay-sur-seine",
                                "épinay": "épinay-sur-seine",
                                "epinay-sur-seine": "épinay-sur-seine",
                                "ile-saint-denis": "île-saint-denis",
                                "ile saint denis": "île-saint-denis",
                                "île saint denis": "île-saint-denis",
                                "la courneuve": "la-courneuve",
                            }
                            normalized_city = city_mapping.get(city, city)
                            if conversation_id not in self.user_data:
                                self.user_data[conversation_id] = {}
                            self.user_data[conversation_id]["city"] = normalized_city

                            # Traitement spécifique pour jeune non RSA non scolarisé
                            if current_state == "city_verification_young_no_rsa":
                                ml_cities = [
                                    "saint-denis",
                                    "pierrefitte",
                                    "saint-ouen",
                                    "épinay-sur-seine",
                                    "villetaneuse",
                                    "île-saint-denis",
                                ]

                                if normalized_city in ml_cities:
                                    print(
                                        f"*** Ville ML détectée par mot-clé: {normalized_city} ***"
                                    )
                                    return {
                                        "next_state": "eligible_ml",
                                        "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par la mission locale de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. Cliquer ici pour prendre un rendez vous avec un conseiller",
                                        "is_final": True,
                                        "eligibility_result": "ML",
                                    }
                            break

                    if not city_found:
                        return {
                            "next_state": current_state,  # Rester dans le même état
                            "message": "Je n'ai pas reconnu cette ville. Pourriez-vous préciser dans quelle ville vous habitez parmi : Saint-Denis (93200), Stains (93240), Pierrefitte (93380), Saint-Ouen (93400), Épinay-sur-Seine (93800), Villetaneuse (93430), Île-Saint-Denis (93450), Aubervilliers (93300), La Courneuve (93120) ?",
                            "is_final": False,
                        }

        # Vérifier si toutes les conditions sont remplies pour ML et appliquer un override
        if conversation_id in self.user_data:
            user_data = self.user_data[conversation_id]

            # Cas spécifique: jeune (16-25.5) sans RSA, non scolarisé, habitant dans une ville ML
            if (
                user_data.get("age", 0) >= 16
                and user_data.get("age", 0) <= 25.5
                and user_data.get("rsa") is False
                and user_data.get("schooling") is False
                and "city" in user_data
                and user_data["city"].lower()
                in [
                    "saint-denis",
                    "pierrefitte",
                    "saint-ouen",
                    "épinay-sur-seine",
                    "villetaneuse",
                    "île-saint-denis",
                ]
            ):

                print("*** CONDITIONS ML DÉTECTÉES - OVERRIDE APPLIQUÉ ***")
                return {
                    "next_state": "eligible_ml",
                    "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par la mission locale de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. Cliquer ici pour prendre un rendez vous avec un conseiller",
                    "is_final": True,
                    "eligibility_result": "ML",
                }

        # État suivant par défaut - si on arrive ici, c'est qu'on n'a pas pu interpréter la réponse
        # Redemander en fonction de l'état actuel
        if "age_verification" in current_state:
            return {
                "next_state": current_state,
                "message": "Je n'ai pas compris votre âge. Pourriez-vous me donner votre âge en chiffres, par exemple 25 ?",
                "is_final": False,
            }
        elif "rsa_verification" in current_state:
            return {
                "next_state": current_state,
                "message": "Je n'ai pas compris si vous êtes bénéficiaire du RSA. Pouvez-vous répondre simplement par oui ou par non ?",
                "is_final": False,
            }
        elif "schooling_verification" in current_state:
            return {
                "next_state": current_state,
                "message": "Je n'ai pas compris si vous êtes actuellement scolarisé. Pouvez-vous répondre simplement par oui ou par non ?",
                "is_final": False,
            }
        elif "city_verification" in current_state:
            return {
                "next_state": current_state,
                "message": "Je n'ai pas reconnu cette ville. Pourriez-vous préciser dans quelle ville vous habitez ? Par exemple : Saint-Denis, Stains, Pierrefitte, etc.",
                "is_final": False,
            }
        else:
            # Transition par défaut générique
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

            # Extraire la ville des données NLP
            text = nlp_data.get("text", "").lower()

            # Vérifier d'abord si un code postal 93XXX est mentionné et si nous sommes dans un contexte de ville
            if (
                "ville" in text
                or "habite" in text
                or "code" in text
                or "postal" in text
            ):
                postcode_pattern = r"93\s*[0-9]{3}"
                postcode_match = re.search(postcode_pattern, text)
                if postcode_match:
                    # Ne pas interpréter code postal comme âge dans un contexte de ville
                    print(
                        f"Code postal trouvé dans un contexte de ville: {postcode_match.group()}"
                    )
                    return result

            # Sinon, extraire l'âge des données NLP ou du message utilisateur
            entities = nlp_data.get("entities", {})

            if "age" in entities:
                age = entities["age"]
                result["age"] = age
                print(f"Âge extrait des entités NLP: {age}")
            else:
                # Essayer d'extraire du texte brut
                print(f"Tentative d'extraction d'âge du texte: '{text}'")

                try:
                    # Trouver le premier nombre dans le texte
                    age_match = re.search(r"\d+", text)
                    if age_match:
                        age = int(age_match.group())
                        result["age"] = age
                        print(f"Âge extrait du texte (chiffres): {age}")
                    else:
                        # Liste étendue de nombres écrits en toutes lettres
                        number_words = {
                            # Nombres de 16 à 19
                            "seize": 16,
                            "16 ans": 16,
                            "dix-sept": 17,
                            "dix sept": 17,
                            "dixsept": 17,
                            "17 ans": 17,
                            "dix-huit": 18,
                            "dix huit": 18,
                            "dixhuit": 18,
                            "18 ans": 18,
                            "dix-neuf": 19,
                            "dix neuf": 19,
                            "dixneuf": 19,
                            "19 ans": 19,
                            # Nombres de 20 à 29
                            "vingt": 20,
                            "20 ans": 20,
                            "vingt et un": 21,
                            "vingt-et-un": 21,
                            "21 ans": 21,
                            "vingt-deux": 22,
                            "vingt deux": 22,
                            "22 ans": 22,
                            "vingt-trois": 23,
                            "vingt trois": 23,
                            "23 ans": 23,
                            "vingt-quatre": 24,
                            "vingt quatre": 24,
                            "24 ans": 24,
                            "vingt-cinq": 25,
                            "vingt cinq": 25,
                            "25 ans": 25,
                            "vingt-six": 26,
                            "vingt six": 26,
                            "26 ans": 26,
                            "vingt-sept": 27,
                            "vingt sept": 27,
                            "27 ans": 27,
                            "vingt-huit": 28,
                            "vingt huit": 28,
                            "28 ans": 28,
                            "vingt-neuf": 29,
                            "vingt neuf": 29,
                            "29 ans": 29,
                            # Nombres de 30 à 39
                            "trente": 30,
                            "30 ans": 30,
                            "trente et un": 31,
                            "trente-et-un": 31,
                            "31 ans": 31,
                            "trente-deux": 32,
                            "trente deux": 32,
                            "32 ans": 32,
                            "trente-trois": 33,
                            "trente trois": 33,
                            "33 ans": 33,
                            "trente-quatre": 34,
                            "trente quatre": 34,
                            "34 ans": 34,
                            "trente-cinq": 35,
                            "trente cinq": 35,
                            "35 ans": 35,
                            "trente-six": 36,
                            "trente six": 36,
                            "36 ans": 36,
                            "trente-sept": 37,
                            "trente sept": 37,
                            "37 ans": 37,
                            "trente-huit": 38,
                            "trente huit": 38,
                            "38 ans": 38,
                            "trente-neuf": 39,
                            "trente neuf": 39,
                            "39 ans": 39,
                            # Nombres de 40 à 49
                            "quarante": 40,
                            "40 ans": 40,
                            "quarante et un": 41,
                            "quarante-et-un": 41,
                            "41 ans": 41,
                            "quarante-deux": 42,
                            "quarante deux": 42,
                            "42 ans": 42,
                            "quarante-trois": 43,
                            "quarante trois": 43,
                            "43 ans": 43,
                            "quarante-quatre": 44,
                            "quarante quatre": 44,
                            "44 ans": 44,
                            "quarante-cinq": 45,
                            "quarante cinq": 45,
                            "45 ans": 45,
                            "quarante-six": 46,
                            "quarante six": 46,
                            "46 ans": 46,
                            "quarante-sept": 47,
                            "quarante sept": 47,
                            "47 ans": 47,
                            "quarante-huit": 48,
                            "quarante huit": 48,
                            "48 ans": 48,
                            "quarante-neuf": 49,
                            "quarante neuf": 49,
                            "49 ans": 49,
                            # Nombres de 50 à 61
                            "cinquante": 50,
                            "50 ans": 50,
                            "cinquante et un": 51,
                            "cinquante-et-un": 51,
                            "51 ans": 51,
                            "cinquante-deux": 52,
                            "cinquante deux": 52,
                            "52 ans": 52,
                            "cinquante-trois": 53,
                            "cinquante trois": 53,
                            "53 ans": 53,
                            "cinquante-quatre": 54,
                            "cinquante quatre": 54,
                            "54 ans": 54,
                            "cinquante-cinq": 55,
                            "cinquante cinq": 55,
                            "55 ans": 55,
                            "cinquante-six": 56,
                            "cinquante six": 56,
                            "56 ans": 56,
                            "cinquante-sept": 57,
                            "cinquante sept": 57,
                            "57 ans": 57,
                            "cinquante-huit": 58,
                            "cinquante huit": 58,
                            "58 ans": 58,
                            "cinquante-neuf": 59,
                            "cinquante neuf": 59,
                            "59 ans": 59,
                            "soixante": 60,
                            "60 ans": 60,
                            "soixante et un": 61,
                            "soixante-et-un": 61,
                            "61 ans": 61,
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
            text = nlp_data.get("text", "").lower()

            # Vérifier d'abord si un code postal de Seine-Saint-Denis est présent
            postcode_pattern = r"93\s*[0-9]{3}"
            postcode_match = re.search(postcode_pattern, text)
            if postcode_match:
                postcode = (
                    postcode_match.group()
                    .replace(" ", "")
                    .replace(".", "")
                    .replace(",", "")
                )

                # Mappage des codes postaux
                code_postal_mapping = {
                    "93200": "saint-denis",
                    "93240": "stains",
                    "93380": "pierrefitte",
                    "93400": "saint-ouen",
                    "93800": "épinay-sur-seine",
                    "93430": "villetaneuse",
                    "93450": "île-saint-denis",
                    "93300": "aubervilliers",
                    "93120": "la-courneuve",
                    "93370": "montfermeil",
                }

                if postcode in code_postal_mapping:
                    result["city"] = code_postal_mapping[postcode]
                    print(
                        f"Ville extraite via code postal: {postcode} => {result['city']}"
                    )
                    return result

            # Si pas de code postal trouvé, continuer avec la logique existante
            if "city" in entities:
                city = entities["city"]
                result["city"] = city.lower()
                print(f"Ville extraite des entités NLP: {city}")
            else:
                # Essayer d'extraire du texte brut
                print(f"Tentative d'extraction de ville du texte: '{text}'")

                cities = [
                    # Saint-Denis
                    "saint-denis",
                    "saint denis",
                    "st-denis",
                    "st denis",
                    "93200",
                    "93 200",
                    "93.200",
                    "932 00",
                    "93-200",
                    "quatre-vingt-treize deux cents",
                    "quatre vingt treize deux cents",
                    # Pierrefitte-sur-Seine
                    "pierrefitte",
                    "pierrefitte-sur-seine",
                    "pierfitte",
                    "pierrefite",
                    "93380",
                    "93 380",
                    "93.380",
                    "933 80",
                    "93-380",
                    "quatre-vingt-treize trois cent quatre-vingts",
                    "quatre vingt treize trois cent quatre vingts",
                    # Saint-Ouen-sur-Seine
                    "saint-ouen",
                    "saint ouen",
                    "st-ouen",
                    "st ouen",
                    "saint-ouen-sur-seine",
                    "93400",
                    "93 400",
                    "93.400",
                    "934 00",
                    "93-400",
                    "quatre-vingt-treize quatre cents",
                    "quatre vingt treize quatre cents",
                    # Épinay-sur-Seine
                    "epinay",
                    "épinay",
                    "epinay-sur-seine",
                    "épinay-sur-seine",
                    "93800",
                    "93 800",
                    "93.800",
                    "938 00",
                    "93-800",
                    "quatre-vingt-treize huit cents",
                    "quatre vingt treize huit cents",
                    # Villetaneuse
                    "villetaneuse",
                    "93430",
                    "93 430",
                    "93.430",
                    "934 30",
                    "93-430",
                    "quatre-vingt-treize quatre cent trente",
                    "quatre vingt treize quatre cent trente",
                    # Île-Saint-Denis
                    "ile-saint-denis",
                    "île-saint-denis",
                    "ile saint denis",
                    "île saint denis",
                    "93450",
                    "93 450",
                    "93.450",
                    "934 50",
                    "93-450",
                    "quatre-vingt-treize quatre cent cinquante",
                    "quatre vingt treize quatre cent cinquante",
                    # Aubervilliers
                    "aubervilliers",
                    "93300",
                    "93 300",
                    "93.300",
                    "933 00",
                    "93-300",
                    "quatre-vingt-treize trois cents",
                    "quatre vingt treize trois cents",
                    # La Courneuve
                    "la courneuve",
                    "la-courneuve",
                    "93120",
                    "93 120",
                    "93.120",
                    "931 20",
                    "93-120",
                    "quatre-vingt-treize cent vingt",
                    "quatre vingt treize cent vingt",
                    # Stains
                    "stains",
                    "93240",
                    "93 240",
                    "93.240",
                    "932 40",
                    "93-240",
                    "quatre-vingt-treize deux cent quarante",
                    "quatre vingt treize deux cent quarante",
                    # Montfermeil
                    "montfermeil",
                    "93370",
                    "93 370",
                    "93.370",
                    "933 70",
                    "93-370",
                    "quatre-vingt-treize trois cent soixante-dix",
                    "quatre vingt treize trois cent soixante dix",
                ]

                # Normalisation des variantes de noms de villes vers leur forme standard
                city_mapping = {
                    # Saint-Denis
                    "saint denis": "saint-denis",
                    "st-denis": "saint-denis",
                    "st denis": "saint-denis",
                    "93200": "saint-denis",
                    "93 200": "saint-denis",
                    "93.200": "saint-denis",
                    "932 00": "saint-denis",
                    "93-200": "saint-denis",
                    "quatre-vingt-treize deux cents": "saint-denis",
                    "quatre vingt treize deux cents": "saint-denis",
                    # Stains
                    "93240": "stains",
                    "93 240": "stains",
                    "93.240": "stains",
                    "932 40": "stains",
                    "93-240": "stains",
                    "quatre-vingt-treize deux cent quarante": "stains",
                    "quatre vingt treize deux cent quarante": "stains",
                    # Pierrefitte
                    "pierrefitte-sur-seine": "pierrefitte",
                    "pierfitte": "pierrefitte",
                    "pierrefite": "pierrefitte",
                    "93380": "pierrefitte",
                    "93 380": "pierrefitte",
                    "93.380": "pierrefitte",
                    "933 80": "pierrefitte",
                    "93-380": "pierrefitte",
                    "quatre-vingt-treize trois cent quatre-vingts": "pierrefitte",
                    "quatre vingt treize trois cent quatre vingts": "pierrefitte",
                    # Saint-Ouen
                    "saint ouen": "saint-ouen",
                    "st-ouen": "saint-ouen",
                    "st ouen": "saint-ouen",
                    "saint-ouen-sur-seine": "saint-ouen",
                    "93400": "saint-ouen",
                    "93 400": "saint-ouen",
                    "93.400": "saint-ouen",
                    "934 00": "saint-ouen",
                    "93-400": "saint-ouen",
                    "quatre-vingt-treize quatre cents": "saint-ouen",
                    "quatre vingt treize quatre cents": "saint-ouen",
                    # Épinay-sur-Seine
                    "epinay": "épinay-sur-seine",
                    "épinay": "épinay-sur-seine",
                    "epinay-sur-seine": "épinay-sur-seine",
                    "93800": "épinay-sur-seine",
                    "93 800": "épinay-sur-seine",
                    "93.800": "épinay-sur-seine",
                    "938 00": "épinay-sur-seine",
                    "93-800": "épinay-sur-seine",
                    "quatre-vingt-treize huit cents": "épinay-sur-seine",
                    "quatre vingt treize huit cents": "épinay-sur-seine",
                    # Villetaneuse
                    "93430": "villetaneuse",
                    "93 430": "villetaneuse",
                    "93.430": "villetaneuse",
                    "934 30": "villetaneuse",
                    "93-430": "villetaneuse",
                    "quatre-vingt-treize quatre cent trente": "villetaneuse",
                    "quatre vingt treize quatre cent trente": "villetaneuse",
                    # Île-Saint-Denis
                    "ile-saint-denis": "île-saint-denis",
                    "ile saint denis": "île-saint-denis",
                    "île saint denis": "île-saint-denis",
                    "93450": "île-saint-denis",
                    "93 450": "île-saint-denis",
                    "93.450": "île-saint-denis",
                    "934 50": "île-saint-denis",
                    "93-450": "île-saint-denis",
                    "quatre-vingt-treize quatre cent cinquante": "île-saint-denis",
                    "quatre vingt treize quatre cent cinquante": "île-saint-denis",
                    # Aubervilliers
                    "93300": "aubervilliers",
                    "93 300": "aubervilliers",
                    "93.300": "aubervilliers",
                    "933 00": "aubervilliers",
                    "93-300": "aubervilliers",
                    "quatre-vingt-treize trois cents": "aubervilliers",
                    "quatre vingt treize trois cents": "aubervilliers",
                    # La Courneuve
                    "la courneuve": "la-courneuve",
                    "93120": "la-courneuve",
                    "93 120": "la-courneuve",
                    "93.120": "la-courneuve",
                    "931 20": "la-courneuve",
                    "93-120": "la-courneuve",
                    "quatre-vingt-treize cent vingt": "la-courneuve",
                    "quatre vingt treize cent vingt": "la-courneuve",
                    # Montfermeil
                    "93370": "montfermeil",
                    "93 370": "montfermeil",
                    "93.370": "montfermeil",
                    "933 70": "montfermeil",
                    "93-370": "montfermeil",
                    "quatre-vingt-treize trois cent soixante-dix": "montfermeil",
                    "quatre vingt treize trois cent soixante dix": "montfermeil",
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
                                "93200",
                                "93 200",
                                "93.200",
                                "932 00",
                                "93-200",
                                "quatre-vingt-treize deux cents",
                                "quatre vingt treize deux cents",
                            ],
                            "stains": [
                                "stains",
                                "93240",
                                "93 240",
                                "93.240",
                                "932 40",
                                "93-240",
                                "quatre-vingt-treize deux cent quarante",
                                "quatre vingt treize deux cent quarante",
                            ],
                            "pierrefitte": [
                                "pierrefitte",
                                "pierrefitte-sur-seine",
                                "pierfitte",
                                "pierrefite",
                                "93380",
                                "93 380",
                                "93.380",
                                "933 80",
                                "93-380",
                                "quatre-vingt-treize trois cent quatre-vingts",
                                "quatre vingt treize trois cent quatre vingts",
                            ],
                            "saint-ouen": [
                                "saint-ouen",
                                "saint ouen",
                                "st-ouen",
                                "st ouen",
                                "saint-ouen-sur-seine",
                                "93400",
                                "93 400",
                                "93.400",
                                "934 00",
                                "93-400",
                                "quatre-vingt-treize quatre cents",
                                "quatre vingt treize quatre cents",
                            ],
                            "épinay-sur-seine": [
                                "epinay",
                                "épinay",
                                "epinay-sur-seine",
                                "épinay-sur-seine",
                                "93800",
                                "93 800",
                                "93.800",
                                "938 00",
                                "93-800",
                                "quatre-vingt-treize huit cents",
                                "quatre vingt treize huit cents",
                            ],
                            "villetaneuse": [
                                "villetaneuse",
                                "93430",
                                "93 430",
                                "93.430",
                                "934 30",
                                "93-430",
                                "quatre-vingt-treize quatre cent trente",
                                "quatre vingt treize quatre cent trente",
                            ],
                            "île-saint-denis": [
                                "ile-saint-denis",
                                "île-saint-denis",
                                "ile saint denis",
                                "île saint denis",
                                "93450",
                                "93 450",
                                "93.450",
                                "934 50",
                                "93-450",
                                "quatre-vingt-treize quatre cent cinquante",
                                "quatre vingt treize quatre cent cinquante",
                            ],
                            "aubervilliers": [
                                "aubervilliers",
                                "93300",
                                "93 300",
                                "93.300",
                                "933 00",
                                "93-300",
                                "quatre-vingt-treize trois cents",
                                "quatre vingt treize trois cents",
                            ],
                            "la-courneuve": [
                                "la courneuve",
                                "la-courneuve",
                                "93120",
                                "93 120",
                                "93.120",
                                "931 20",
                                "93-120",
                                "quatre-vingt-treize cent vingt",
                                "quatre vingt treize cent vingt",
                            ],
                            "montfermeil": [
                                "montfermeil",
                                "93370",
                                "93 370",
                                "93.370",
                                "933 70",
                                "93-370",
                                "quatre-vingt-treize trois cent soixante-dix",
                                "quatre vingt treize trois cent soixante dix",
                            ],
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
