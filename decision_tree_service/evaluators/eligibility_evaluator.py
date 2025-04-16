import json
import os
import re
from datetime import datetime

# Importer le module city_variants
try:
    from data.city_variants import (
        CITY_VARIANTS,
        find_city_from_text,
        normalize_city_name,
    )
except ImportError:
    # Fallback si le chemin d'import direct ne fonctionne pas
    import sys
    import os.path

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from data.city_variants import (
        CITY_VARIANTS,
        find_city_from_text,
        normalize_city_name,
    )


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
                "pre_consent": {
                    "next": "consent",
                    "message": "Bien sûr, je suis là pour t'aider ! 😊\nDonne moi plus de détails sur ton besoin?",
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
                            "message": "Êtes-vous bénéficiaire du <b>RSA</b> (Revenu de Solidarité Active) ? C'est une aide sociale qui garantit un revenu minimum aux personnes sans ressources ou à faibles revenus, versée par la CAF ou la MSA.",
                        },
                        {
                            "condition": "age > 25.5 and age < 62",
                            "next": "rsa_verification_adult",
                            "message": "Êtes-vous bénéficiaire du <b>RSA</b> (Revenu de Solidarité Active) ? C'est une aide sociale qui garantit un revenu minimum aux personnes sans ressources ou à faibles revenus, versée par la CAF ou la MSA.",
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
                    "message": "Êtes-vous bénéficiaire du <b>RSA</b> (Revenu de Solidarité Active) ? C'est une aide sociale qui garantit un revenu minimum aux personnes sans ressources ou à faibles revenus, versée par la CAF ou la MSA.",
                    "responses": {
                        "yes": {
                            "next": "schooling_verification_young_rsa",
                            "message": "D'accord, tu es scolarisé?",
                        },
                        "no": {
                            "next": "schooling_verification_young_no_rsa",
                            "message": "D'accord, tu es scolarisé?",
                        },
                    },
                },
                "rsa_verification_young": {
                    "next": "schooling_verification_young",
                    "message": "Êtes-vous bénéficiaire du <b>RSA</b> (Revenu de Solidarité Active) ? C'est une aide sociale qui garantit un revenu minimum aux personnes sans ressources ou à faibles revenus, versée par la CAF ou la MSA.",
                    "responses": {
                        "yes": {
                            "next": "schooling_verification_young_rsa",
                            "message": "D'accord, tu es scolarisé?",
                        },
                        "no": {
                            "next": "schooling_verification_young_no_rsa",
                            "message": "D'accord, tu es scolarisé?",
                        },
                    },
                },
                "schooling_verification_young_rsa": {
                    "next": "city_verification_young_rsa",
                    "message": "D'accord, tu es scolarisé?",
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
                            "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par l'agence locale d'insertion de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. <a href='https://code93.fr/rendezvous/formulaire_ali.php' target='_blank'>Cliquez ici </a> pour prendre un rendez-vous avec un conseiller",
                            "is_final": True,
                            "eligibility_result": "ALI",
                        },
                        {
                            "condition": "True",
                            "next": "not_eligible_city",
                            "message": "Pour ton cas, je te recommande de contacter les services sociaux de ta ville ou de ton département pour explorer les dispositifs d'accompagnement disponibles localement.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        },
                    ],
                },
                "schooling_verification_young_no_rsa": {
                    "next": "city_verification_young_no_rsa",
                    "message": "D'accord, tu es scolarisé?",
                    "responses": {
                        "yes": {
                            "next": "not_eligible_schooling",
                            "message": "Malheureusement, tu n'es pas éligible à un accompagnement pour le moment, tant que tu es encore scolarisé. 🎓 Cependant, dès que tu auras terminé tes études, tu pourras bénéficier de nos services d'accompagnement pour t'aider dans ta recherche d'emploi et ton insertion professionnelle. En attendant, si tu as des questions ou besoin de conseils, tu peux appeler CODEE au  0148131320. A bientôt",
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
                            "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par la mission locale de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. <a href='https://code93.fr/rendezvous/formulaire_ml.php' target='_blank'>Cliquez ici </a> pour prendre un rendez-vous avec un conseiller",
                            "is_final": True,
                            "eligibility_result": "ML",
                        },
                        {
                            "condition": "True",
                            "next": "not_eligible_city",
                            "message": "Pour ton cas, je te recommande de contacter les services sociaux de ta ville ou de ton département pour explorer les dispositifs d'accompagnement disponibles localement.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        },
                    ],
                },
                "rsa_verification_adult": {
                    "next": "schooling_verification_adult",
                    "message": "Êtes-vous bénéficiaire du <b>RSA</b> (Revenu de Solidarité Active) ? C'est une aide sociale qui garantit un revenu minimum aux personnes sans ressources ou à faibles revenus, versée par la CAF ou la MSA.",
                    "responses": {
                        "yes": {
                            "next": "schooling_verification_adult_rsa",
                            "message": "D'accord, tu es scolarisé?",
                        },
                        "no": {
                            "next": "schooling_verification_adult_no_rsa",
                            "message": "D'accord, tu es scolarisé?",
                        },
                    },
                },
                "schooling_verification_adult_rsa": {
                    "next": "city_verification_adult_rsa",
                    "message": "D'accord, tu es scolarisé?",
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
                            "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par l'agence locale d'insertion de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. <a href='https://code93.fr/rendezvous/formulaire_ali.php' target='_blank'>Cliquez ici</a> pour prendre un rendez-vous avec un conseiller",
                            "is_final": True,
                            "eligibility_result": "ALI",
                        },
                        {
                            "condition": "True",
                            "next": "not_eligible_city",
                            "message": "Pour ton cas, je te recommande de contacter les services sociaux de ta ville ou de ton département pour explorer les dispositifs d'accompagnement disponibles localement.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        },
                    ],
                },
                "schooling_verification_adult_no_rsa": {
                    "next": "city_verification_adult_no_rsa",
                    "message": "D'accord, tu es scolarisé?",
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
                            "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par le PLIE de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. <a href='https://code93.fr/rendezvous/formulaire_plie.php' target='_blank'>Cliquez ici </a> pour prendre un rendez-vous avec un conseiller",
                            "is_final": True,
                            "eligibility_result": "PLIE",
                        },
                        {
                            "condition": "True",
                            "next": "not_eligible_city",
                            "message": "Pour ton cas, je te recommande de contacter les services sociaux de ta ville ou de ton département pour explorer les dispositifs d'accompagnement disponibles localement.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        },
                    ],
                },
                "eligible_ali": {
                    "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par l'agence locale d'insertion de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. <a href='https://code93.fr/rendezvous/formulaire_ali.php' target='_blank'>Cliquez ici </a> pour prendre un rendez-vous avec un conseiller",
                    "is_final": True,
                    "eligibility_result": "ALI",
                },
                "eligible_ml": {
                    "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par la mission locale de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. <a href='https://code93.fr/rendezvous/formulaire_ml.php' target='_blank'>Cliquez ici </a> pour prendre un rendez-vous avec un conseiller",
                    "is_final": True,
                    "eligibility_result": "ML",
                },
                "eligible_plie": {
                    "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par le PLIE de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. <a href='https://code93.fr/rendezvous/formulaire_plie.php' target='_blank'>Cliquez ici </a> pour prendre un rendez-vous avec un conseiller",
                    "is_final": True,
                    "eligibility_result": "PLIE",
                },
                "not_eligible_age": {
                    "message": "Je suis désolé, mais vous ne remplissez pas les critères d'âge pour être éligible aux programmes.",
                    "is_final": True,
                    "eligibility_result": "Non éligible (âge)",
                },
                "not_eligible_city": {
                    "message": "Pour ton cas, je te recommande de contacter les services sociaux de ta ville ou de ton département pour explorer les dispositifs d'accompagnement disponibles localement.",
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

    def calculate_similarity(self, str1, str2):
        """
        Calcule la similarité entre deux chaînes de caractères (distance de Levenshtein normalisée)
        Retourne un pourcentage de similarité entre 0 et 100
        """
        # Normaliser les chaînes
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()

        # Si les chaînes sont identiques, retourner 100%
        if str1 == str2:
            return 100

        # Si l'une des chaînes est vide, la distance est égale à la longueur de l'autre chaîne
        if len(str1) == 0 or len(str2) == 0:
            return 0

        # Initialisation de la matrice
        matrix = [[0 for x in range(len(str2) + 1)] for x in range(len(str1) + 1)]

        # Remplissage de la première ligne et de la première colonne
        for i in range(len(str1) + 1):
            matrix[i][0] = i
        for j in range(len(str2) + 1):
            matrix[0][j] = j

        # Calcul de la distance de Levenshtein
        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                cost = 0 if str1[i - 1] == str2[j - 1] else 1
                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,  # Suppression
                    matrix[i][j - 1] + 1,  # Insertion
                    matrix[i - 1][j - 1] + cost,  # Substitution
                )

        # La distance de Levenshtein est la valeur dans le coin inférieur droit de la matrice
        distance = matrix[len(str1)][len(str2)]

        # Normaliser la distance pour obtenir un pourcentage de similarité
        max_length = max(len(str1), len(str2))
        similarity = (1 - distance / max_length) * 100

        return similarity

    def find_closest_city(self, city_input, city_list, similarity_threshold=60):
        """
        Trouve la ville la plus proche dans la liste si elle dépasse le seuil de similarité

        Args:
            city_input (str): Nom de ville saisi par l'utilisateur
            city_list (list): Liste des noms de villes valides
            similarity_threshold (int): Seuil de similarité en pourcentage (défaut: 60%)

        Returns:
            tuple: (ville la plus proche, score de similarité) ou (None, 0) si aucune correspondance
        """
        if not city_input or not city_list:
            return None, 0

        max_similarity = 0
        closest_city = None

        for city in city_list:
            similarity = self.calculate_similarity(city_input, city)
            if similarity > max_similarity:
                max_similarity = similarity
                closest_city = city

        # Retourner la ville la plus proche si elle dépasse le seuil
        if max_similarity >= similarity_threshold:
            return closest_city, max_similarity

        return None, 0

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
            elif process_type == "extract_city":
                if "out_of_zone" in process_result:
                    ville = process_result.get("mentioned_city", "mentionnée")
                    return {
                        "next_state": "not_eligible_city",  # Passer directement à l'état non éligible
                        "message": f"⚠️ Important : Mon périmètre d'action est limité à la Plaine Commune et au département de la Seine-Saint-Denis (93). La ville de {ville} est en dehors de ma zone d'intervention. Pour ton cas, je te recommande de contacter les services de ta ville ou de ton département.",
                        "is_final": True,
                        "eligibility_result": "Non éligible (ville hors périmètre)",
                    }

                # Gérer le cas où une ville similaire est détectée et nécessite confirmation
                if "city_needs_confirmation" in process_result:
                    suggested_city = process_result.get("suggested_city")
                    user_input = process_result.get("user_input")
                    similarity_score = process_result.get("similarity_score", 0)

                    # Formatage du score pour l'affichage
                    similarity_formatted = f"{similarity_score:.1f}"

                    confirmation_message = (
                        f'Vous avez indiqué "{user_input}". '
                        f'Souhaitez-vous dire "{suggested_city}" ? '
                        f"(Score de similarité: {similarity_formatted}%)\n\n"
                        f'Veuillez confirmer par "oui" ou "non".'
                    )

                    print(
                        f"Demande de confirmation pour la ville similaire: {suggested_city}"
                    )

                    # Créer un état temporaire pour la confirmation de la ville
                    temp_state = f"{current_state}_city_confirmation"

                    # Stocker la ville suggérée pour référence future
                    if conversation_id not in self.user_data:
                        self.user_data[conversation_id] = {}
                    self.user_data[conversation_id]["suggested_city"] = suggested_city

                    return {
                        "next_state": temp_state,
                        "message": confirmation_message,
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

        # Gérer spécifiquement les états de confirmation de ville
        if "_city_confirmation" in current_state:
            text = nlp_data.get("text", "").lower() if nlp_data else ""
            intent = nlp_data.get("intent", "").lower() if nlp_data else ""

            # Récupérer la ville suggérée stockée précédemment
            suggested_city = self.user_data.get(conversation_id, {}).get(
                "suggested_city"
            )

            # Déterminer si l'utilisateur a confirmé ou non
            confirmed = False
            if (
                intent in ["yes", "affirm", "agree"]
                or "oui" in text
                or "d'accord" in text
                or "ok" in text
            ):
                confirmed = True
            elif intent in ["no", "deny", "disagree"] or "non" in text or "pas" in text:
                confirmed = False
            else:
                # Si la réponse est ambiguë, demander à nouveau
                return {
                    "next_state": current_state,
                    "message": "Je n'ai pas compris votre réponse. Veuillez répondre par 'oui' si vous souhaitiez bien dire \""
                    + str(suggested_city)
                    + "\", ou 'non' dans le cas contraire.",
                    "is_final": False,
                }

            # Extraire le state de base (sans "_city_confirmation")
            base_state = current_state.replace("_city_confirmation", "")

            if confirmed:
                # Si l'utilisateur confirme, utiliser la ville suggérée
                if conversation_id not in self.user_data:
                    self.user_data[conversation_id] = {}
                self.user_data[conversation_id]["city"] = suggested_city

                print(f"Utilisateur a confirmé la ville: {suggested_city}")

                # Continuer avec l'arbre de décision normal
                state_def = self.rules["states"].get(base_state)
                if state_def and "transitions" in state_def:
                    for transition in state_def["transitions"]:
                        condition = transition["condition"]

                        # Préparer les données pour l'évaluation
                        eval_data = {}
                        if user_data:
                            eval_data.update(user_data)
                        eval_data["city"] = suggested_city

                        # Évaluer la condition avec les données mises à jour
                        if self._evaluate_condition(condition, eval_data):
                            return {
                                "next_state": transition["next"],
                                "message": transition["message"],
                                "is_final": transition.get("is_final", False),
                                "eligibility_result": transition.get(
                                    "eligibility_result"
                                ),
                            }

                # Si aucune transition ne correspond, utiliser la transition par défaut
                return {
                    "next_state": "not_eligible_city",
                    "message": "Pour ton cas, je te recommande de contacter les services sociaux de ta ville ou de ton département pour explorer les dispositifs d'accompagnement disponibles localement.",
                    "is_final": True,
                    "eligibility_result": "Non éligible (ville)",
                }
            else:
                # Si l'utilisateur ne confirme pas, lui demander à nouveau la ville
                return {
                    "next_state": base_state,
                    "message": "D'accord. Pourriez-vous préciser à nouveau le nom de votre ville ou votre code postal ?",
                    "is_final": False,
                }

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
                        "message": "D'accord, tu es scolarisé?",
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
                        "message": "D'accord, tu es scolarisé?",
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
                        "message": "D'accord, tu es scolarisé?",
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
                        "message": "Êtes-vous bénéficiaire du <b>RSA</b> (Revenu de Solidarité Active) ? C'est une aide sociale qui garantit un revenu minimum aux personnes sans ressources ou à faibles revenus, versée par la CAF ou la MSA.",
                        "is_final": False,
                    }
                elif age < 64:
                    return {
                        "next_state": "rsa_verification_adult",
                        "message": "Êtes-vous bénéficiaire du <b>RSA</b> (Revenu de Solidarité Active) ? C'est une aide sociale qui garantit un revenu minimum aux personnes sans ressources ou à faibles revenus, versée par la CAF ou la MSA.",
                        "is_final": False,
                    }
                else:
                    return {
                        "next_state": "not_eligible_age",
                        "message": "Je suis désolé, mais vous devez avoir moins de 64 ans pour être éligible aux programmes.",
                        "is_final": True,
                        "eligibility_result": "Non éligible (âge)",
                    }
            # Gérer le cas où on est dans l'état age_verification mais qu'on n'a pas détecté l'âge
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
                # Utiliser la fonction find_city_from_text du module city_variants
                text = nlp_data.get("text", "").lower() if nlp_data else ""

                # Essayer d'abord de trouver une ville dans le texte
                city_name = find_city_from_text(text)

                if city_name:
                    # Ajouter la ville aux données utilisateur
                    if conversation_id not in self.user_data:
                        self.user_data[conversation_id] = {}
                    self.user_data[conversation_id]["city"] = city_name

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

                        if city_name in ml_cities:
                            print(
                                f"*** Ville ML détectée via city_variants: {city_name} ***"
                            )
                            return {
                                "next_state": "eligible_ml",
                                "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par la mission locale de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. <a href='https://code93.fr/rendezvous/formulaire_ml.php' target='_blank'>Cliquez ici </a> pour prendre un rendez-vous avec un conseiller",
                                "is_final": True,
                                "eligibility_result": "ML",
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
                and normalize_city_name(user_data["city"].lower())
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
                    "message": "🎉 Bonne nouvelle ! 🎉 Tu es éligible à un accompagnement personnalisé par la mission locale de ta ville ! 🙌 Cela peut t'aider à trouver des opportunités professionnelles, recevoir des conseils et bien plus. <a href='https://code93.fr/rendezvous/formulaire_ml.php' target='_blank'>Cliquez ici </a> pour prendre un rendez-vous avec un conseiller",
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

            # Sinon, extraire l'âge des données NLP ou du message utilisateur
            text = nlp_data.get("text", "").lower() if nlp_data else ""
            entities = nlp_data.get("entities", {})

            # Vérifier si l'âge est dans un contexte de code postal
            if (
                "ville" in text
                or "habite" in text
                or "code" in text
                or "postal" in text
            ) and re.search(r"93\s*\d{3}", text):
                print(f"Détection d'un code postal, pas d'un âge")
                return result

            # Extraire l'âge des entités ou du texte
            if "age" in entities:
                age = entities["age"]
                result["age"] = age
                print(f"Âge extrait des entités NLP: {age}")
            else:
                # Essayer d'extraire du texte brut
                print(f"Tentative d'extraction d'âge du texte: '{text}'")
                try:
                    # Trouver le premier nombre dans le texte
                    age_match = re.search(r"\b\d+\b", text)
                    if age_match:
                        age = int(age_match.group())
                        result["age"] = age
                        print(f"Âge extrait du texte (chiffres): {age}")
                    else:
                        # Dictionnaire des nombres en lettres
                        number_words = {
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
                            "vingt": 20,
                            "20 ans": 20,
                            "vingt et un": 21,
                            "vingt-et-un": 21,
                            "21 ans": 21,
                            # ... (autres nombres)
                        }

                        for word, value in number_words.items():
                            if word in text:
                                result["age"] = value
                                print(f"Âge extrait du texte (mots): {value}")
                                break

                except Exception as e:
                    print(f"Erreur lors de l'extraction d'âge: {str(e)}")

        elif process_type == "extract_city":
            # D'abord vérifier si la ville est déjà dans les données existantes
            if existing_data and "city" in existing_data:
                print(f"Ville déjà présente dans les données: {existing_data['city']}")
                result["city"] = existing_data["city"].lower()
                return result

            # Extraire la ville des données NLP
            text = nlp_data.get("text", "").lower() if nlp_data else ""

            # Liste des villes hors 93
            villes_hors_93 = [
                "paris",
                "marseille",
                "lyon",
                "toulouse",
                "nice",
                "nantes",
                "strasbourg",
                "montpellier",
                "bordeaux",
                "lille",
                "rennes",
                "reims",
                "toulon",
                "grenoble",
                "dijon",
                "angers",
                "nîmes",
                "villeurbanne",
                "le havre",
                "clermont-ferrand",
                "brest",
                "limoges",
                "tours",
                "amiens",
                "courbevoie",
                "nanterre",
                "boulogne",
                "versailles",
                "cergy",
                "poissy",
                "sarcelles",
                "argenteuil",
                "asnières",
                "colombes",
                "créteil",
                "vitry",
                "evry",
                "meaux",
                "melun",
                "fontainebleau",
                "provins",
                "mantes",
                "neuilly",
                "puteaux",
            ]

            # Vérifier si le texte contient un code postal hors 93
            postcode_match = re.search(r"\b(\d{5})\b", text)
            if postcode_match:
                code = postcode_match.group(1)
                if code and not code.startswith("93"):
                    result["out_of_zone"] = True
                    result["mentioned_city"] = code
                    print(f"Code postal hors zone détecté: {code}")
                    return result

            # Vérifier si le texte contient explicitement une ville hors 93
            for ville in villes_hors_93:
                if ville in text:
                    result["out_of_zone"] = True
                    result["mentioned_city"] = ville
                    print(f"Ville hors zone détectée: {ville}")
                    return result

            # 1. D'abord chercher dans notre base de données CITY_VARIANTS
            city_name = find_city_from_text(text)
            if city_name:
                result["city"] = city_name
                print(f"Ville extraite via find_city_from_text: {city_name}")
                return result

            # 2. Si pas trouvé, essayer avec l'algorithme de similarité
            standard_cities = list(CITY_VARIANTS.keys())
            closest_city, similarity = self.find_closest_city(text, standard_cities, 60)

            if closest_city and similarity >= 60:
                # Une ville similaire a été trouvée
                result["city_needs_confirmation"] = True
                result["suggested_city"] = closest_city
                result["user_input"] = text
                result["similarity_score"] = similarity
                print(
                    f"Ville similaire détectée: {closest_city} (score: {similarity:.2f}%)"
                )
                return result

            # 3. Si on a toujours rien, essayer d'extraire des entités
            entities = nlp_data.get("entities", {})
            if "city" in entities:
                city = entities["city"].lower()

                # Vérifier si c'est une ville hors zone
                for ville in villes_hors_93:
                    if ville in city:
                        result["out_of_zone"] = True
                        result["mentioned_city"] = ville
                        print(f"Ville hors zone détectée via entités: {ville}")
                        return result

                # Normaliser le nom de la ville
                normalized_city = normalize_city_name(city)
                if normalized_city:
                    result["city"] = normalized_city
                    print(
                        f"Ville extraite des entités NLP: {city} -> {normalized_city}"
                    )
                    return result
                else:
                    # Si la ville n'est pas reconnue du tout
                    result["unrecognized_city"] = city
                    print(f"Ville non reconnue détectée: {city}")
                    return result

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
            if " in " in condition and "[" in condition and "]" in condition:
                # Extraire la variable et la liste
                var_name, list_str = condition.split(" in ", 1)
                var_name = var_name.strip()

                if var_name in data:
                    # Normaliser la valeur entrée
                    value = data[var_name]
                    if var_name == "city" and isinstance(value, str):
                        value = value.lower()

                    # Évaluer la liste (en supposant qu'elle est correctement formatée)
                    try:
                        list_value = eval(list_str, {"__builtins__": {}})

                        # Pour les villes, on vérifie aussi les variantes
                        if var_name == "city":
                            # Normaliser la ville
                            normalized_city = normalize_city_name(value)
                            if not normalized_city:
                                normalized_city = value

                            print(f"Ville normalisée: '{value}' -> '{normalized_city}'")

                            # Vérifier si la ville normalisée est dans la liste
                            for listed_city in list_value:
                                listed_city = str(listed_city).lower()

                                # Vérification directe
                                if normalized_city == listed_city:
                                    return True

                                # Vérifier dans les variantes connues
                                if (
                                    normalized_city in CITY_VARIANTS
                                    and listed_city in CITY_VARIANTS[normalized_city]
                                ):
                                    print(
                                        f"Ville '{normalized_city}' trouvée comme variante de '{listed_city}'"
                                    )
                                    return True

                                if (
                                    listed_city in CITY_VARIANTS
                                    and normalized_city in CITY_VARIANTS[listed_city]
                                ):
                                    print(
                                        f"Ville '{listed_city}' trouvée comme variante de '{normalized_city}'"
                                    )
                                    return True

                            # Dernière vérification directe dans la liste
                            if value in list_value:
                                return True

                            print(f"Ville '{value}' non trouvée dans la liste")
                            return False
                        else:
                            # Pour les autres types de données, simple vérification d'appartenance
                            return value in list_value
                    except Exception as e:
                        print(f"Erreur lors de l'évaluation de la liste: {str(e)}")
                        return False
                else:
                    print(
                        f"Variable '{var_name}' requise pour l'évaluation mais absente des données!"
                    )
                    return False

            # Créer un environnement d'évaluation sécurisé pour les autres conditions
            eval_context = {"__builtins__": {}}
            for key, val in data.items():
                eval_context[key] = val
                print(f"Variable ajoutée au contexte: {key} = {val}")

            # Vérifier si toutes les variables nécessaires sont présentes
            for var_name in re.findall(r"\b([a-zA-Z_]\w*)\b", condition):
                if var_name not in eval_context and var_name not in [
                    "True",
                    "False",
                    "and",
                    "or",
                    "not",
                    "in",
                ]:
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
