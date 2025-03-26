import uuid
import requests
import json
from datetime import datetime
from config.config import Config


class ConversationManager:
    def __init__(self):
        self.conversations = {}  # In-memory storage for development

    def create_conversation(self, user_id):
        """Create a new conversation and return its ID"""
        conversation_id = str(uuid.uuid4())

        self.conversations[conversation_id] = {
            "id": conversation_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "current_state": "initial",
            "eligibility_result": None,
            "user_data": {},  # Storage for user data across the conversation
        }

        return conversation_id

    def get_welcome_message(self):
        """Return the welcome message to start the conversation"""
        return "Bonjour, je suis CODEE, votre assistant virtuel. Je suis là pour vous aider à déterminer votre éligibilité aux programmes sociaux. Quelques questions simples me permettront de vous orienter vers le dispositif le plus adapté à votre situation."

    def process_message(self, conversation_id, text):
        """Process user message and advance the conversation"""
        if conversation_id not in self.conversations:
            raise Exception("Conversation not found")

        conversation = self.conversations[conversation_id]

        # Add user message to history
        conversation["messages"].append(
            {"role": "user", "content": text, "timestamp": datetime.now().isoformat()}
        )

        # Process with NLP service
        nlp_response = self._process_with_nlp(text)
        print(f"NLP Response: {json.dumps(nlp_response)}")

        # Store extracted entities in user_data
        if "entities" in nlp_response and nlp_response["entities"]:
            if "user_data" not in conversation:
                conversation["user_data"] = {}
            for key, value in nlp_response["entities"].items():
                conversation["user_data"][key] = value
            print(f"User data updated: {json.dumps(conversation['user_data'])}")

        # Get next step from decision tree
        decision_response = self._process_with_decision_tree(
            conversation_id,
            conversation["current_state"],
            nlp_response,
            conversation.get("user_data", {}),
        )

        # Update conversation state
        conversation["current_state"] = decision_response.get(
            "next_state", conversation["current_state"]
        )

        if "eligibility_result" in decision_response:
            conversation["eligibility_result"] = decision_response["eligibility_result"]

        # Add bot response to history
        conversation["messages"].append(
            {
                "role": "bot",
                "content": decision_response.get(
                    "message", "Je n'ai pas compris. Pouvez-vous répéter ?"
                ),
                "timestamp": datetime.now().isoformat(),
            }
        )

        return {
            "message": decision_response.get("message"),
            "conversation_id": conversation_id,
            "is_final": decision_response.get("is_final", False),
        }

    def get_conversation(self, conversation_id):
        """Get the full conversation data"""
        return self.conversations.get(conversation_id)

    def _process_with_nlp(self, text):
        """Send text to NLP service for intent and entity extraction"""
        try:
            # Pour l'instant, nous simulons la réponse NLP
            # Extraction basique des entités
            entities = {}

            # Tenter d'extraire l'âge
            import re

            age_match = re.search(r"\d+", text)
            if age_match:
                entities["age"] = int(age_match.group())

            # Vérifier pour le RSA
            rsa_keywords = ["rsa", "revenu de solidarité active"]
            if any(keyword in text.lower() for keyword in rsa_keywords):
                if "non" in text.lower() or "pas" in text.lower():
                    entities["rsa"] = False
                else:
                    entities["rsa"] = True

            # Vérifier pour la scolarisation
            schooling_keywords = ["scolarisé", "école", "étudiant", "études"]
            if any(keyword in text.lower() for keyword in schooling_keywords):
                if "non" in text.lower() or "pas" in text.lower():
                    entities["schooling"] = False
                else:
                    entities["schooling"] = True

            # Vérifier pour les villes
            cities = [
                "saint-denis",
                "stains",
                "pierrefitte",
                "saint-ouen",
                "épinay",
                "villetaneuse",
                "île-saint-denis",
                "aubervilliers",
                "épinay-sur-seine",
                "la courneuve",
                "montfermeil",
            ]
            for city in cities:
                if city in text.lower() or city.replace("-", " ") in text.lower():
                    entities["city"] = city
                    break

            # Déterminer l'intention
            intent = "provide_info"
            if "?" in text:
                intent = "ask_question"
            elif (
                "oui" in text.lower()
                or "yes" in text.lower()
                or "accepte" in text.lower()
            ):
                intent = "yes"
            elif "non" in text.lower() or "no" in text.lower():
                intent = "no"

            return {
                "intent": intent,
                "entities": entities,
                "text": text,
                "sentiment": "neutral",
                "confidence": 0.8,
            }
        except Exception as e:
            print(f"Error processing with NLP: {str(e)}")
            return {"intent": "unknown", "entities": {}}

    def _process_with_decision_tree(
        self, conversation_id, current_state, nlp_data, user_data=None
    ):
        """Get next step from decision tree service"""
        try:
            print(
                f"Calling decision tree service with: state={current_state}, nlp_data={json.dumps(nlp_data)}"
            )
            if user_data:
                print(f"User data: {json.dumps(user_data)}")

            # Tenter d'appeler le service d'arbre décisionnel réel
            try:
                decision_tree_url = f"{Config.DECISION_TREE_SERVICE_URL}/evaluate"
                print(f"Sending request to: {decision_tree_url}")

                payload = {
                    "conversation_id": conversation_id,
                    "current_state": current_state,
                    "nlp_data": nlp_data,
                    "user_data": user_data or {},
                }
                print(f"Payload: {json.dumps(payload)}")

                response = requests.post(decision_tree_url, json=payload)

                print(f"Decision tree response status: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"Decision tree result: {json.dumps(result)}")
                    return result
                else:
                    print(
                        f"Decision tree service returned an error: {response.status_code} - {response.text}"
                    )
                    # Continue with fallback
            except Exception as api_error:
                print(f"Failed to call decision tree service: {str(api_error)}")
                # Continue with fallback

            # Simulation comme plan de secours
            print("Using fallback decision tree logic")

            # Consentement
            if current_state == "initial":
                return {
                    "next_state": "consent",
                    "message": "Bonjour, je suis un CODEE qui peut vous aider à déterminer votre éligibilité aux programmes sociaux.",
                    "is_final": False,
                }
            elif current_state == "consent":
                intent = nlp_data.get("intent", "").lower() if nlp_data else ""
                if intent == "yes":
                    return {
                        "next_state": "age_verification",
                        "message": "Merci. Commençons par votre âge. Quel âge avez-vous ?",
                        "is_final": False,
                    }
                else:
                    return {
                        "next_state": "age_verification",
                        "message": "Merci. Commençons par votre âge. Quel âge avez-vous ?",
                        "is_final": False,
                    }

            # Vérification de l'âge
            elif current_state == "age_verification":
                # Vérifier si l'âge est dans les données utilisateur
                age = None
                if user_data and "age" in user_data:
                    age = user_data["age"]
                elif (
                    nlp_data
                    and "entities" in nlp_data
                    and "age" in nlp_data["entities"]
                ):
                    age = nlp_data["entities"]["age"]

                if age is not None:
                    if age < 16:
                        return {
                            "next_state": "not_eligible_age",
                            "message": "Je suis désolé, mais vous devez avoir au moins 16 ans pour être éligible aux programmes.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (âge)",
                        }
                    elif age >= 16 and age <= 25.5:
                        return {
                            "next_state": "rsa_verification_young",
                            "message": "Êtes-vous bénéficiaire du RSA ?",
                            "is_final": False,
                        }
                    elif age > 25.5 and age < 62:
                        return {
                            "next_state": "rsa_verification_adult",
                            "message": "Êtes-vous bénéficiaire du RSA ?",
                            "is_final": False,
                        }
                    else:  # age >= 62
                        return {
                            "next_state": "not_eligible_age",
                            "message": "Je suis désolé, mais vous devez avoir moins de 62 ans pour être éligible aux programmes.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (âge)",
                        }
                else:
                    return {
                        "next_state": "age_verification",
                        "message": "Quel âge avez-vous ?",
                        "is_final": False,
                    }

            # RSA verification - Young (16-25.5)
            elif current_state == "rsa_verification_young":
                intent = nlp_data.get("intent", "").lower() if nlp_data else ""
                rsa = None

                if "entities" in nlp_data and "rsa" in nlp_data["entities"]:
                    rsa = nlp_data["entities"]["rsa"]
                elif user_data and "rsa" in user_data:
                    rsa = user_data["rsa"]
                elif "oui" in nlp_data.get("text", "").lower() or intent == "yes":
                    rsa = True
                elif "non" in nlp_data.get("text", "").lower() or intent == "no":
                    rsa = False

                if rsa is True:
                    return {
                        "next_state": "schooling_verification_young_rsa",
                        "message": "Êtes-vous scolarisé actuellement ?",
                        "is_final": False,
                    }
                elif rsa is False:
                    return {
                        "next_state": "schooling_verification_young_no_rsa",
                        "message": "Êtes-vous scolarisé actuellement ?",
                        "is_final": False,
                    }
                else:
                    return {
                        "next_state": "rsa_verification_young",
                        "message": "Êtes-vous bénéficiaire du RSA ? Veuillez répondre par oui ou non.",
                        "is_final": False,
                    }

            # RSA verification - Adult (>25.5)
            elif current_state == "rsa_verification_adult":
                intent = nlp_data.get("intent", "").lower() if nlp_data else ""
                rsa = None

                if "entities" in nlp_data and "rsa" in nlp_data["entities"]:
                    rsa = nlp_data["entities"]["rsa"]
                elif user_data and "rsa" in user_data:
                    rsa = user_data["rsa"]
                elif "oui" in nlp_data.get("text", "").lower() or intent == "yes":
                    rsa = True
                elif "non" in nlp_data.get("text", "").lower() or intent == "no":
                    rsa = False

                if rsa is True:
                    return {
                        "next_state": "schooling_verification_adult_rsa",
                        "message": "Êtes-vous scolarisé actuellement ?",
                        "is_final": False,
                    }
                elif rsa is False:
                    return {
                        "next_state": "schooling_verification_adult_no_rsa",
                        "message": "Êtes-vous scolarisé actuellement ?",
                        "is_final": False,
                    }
                else:
                    return {
                        "next_state": "rsa_verification_adult",
                        "message": "Êtes-vous bénéficiaire du RSA ? Veuillez répondre par oui ou non.",
                        "is_final": False,
                    }

            # Schooling verification - Young with RSA
            elif current_state == "schooling_verification_young_rsa":
                return {
                    "next_state": "city_verification_young_rsa",
                    "message": "Dans quelle ville habitez-vous ?",
                    "is_final": False,
                }

            # Schooling verification - Young without RSA
            elif current_state == "schooling_verification_young_no_rsa":
                intent = nlp_data.get("intent", "").lower() if nlp_data else ""
                schooling = None

                if "entities" in nlp_data and "schooling" in nlp_data["entities"]:
                    schooling = nlp_data["entities"]["schooling"]
                elif user_data and "schooling" in user_data:
                    schooling = user_data["schooling"]
                elif "oui" in nlp_data.get("text", "").lower() or intent == "yes":
                    schooling = True
                elif "non" in nlp_data.get("text", "").lower() or intent == "no":
                    schooling = False

                if schooling is True:
                    return {
                        "next_state": "not_eligible_schooling",
                        "message": "Je suis désolé, mais vous n'êtes pas éligible aux programmes si vous êtes scolarisé et ne bénéficiez pas du RSA.",
                        "is_final": True,
                        "eligibility_result": "Non éligible (scolarisation)",
                    }
                elif schooling is False:
                    return {
                        "next_state": "city_verification_young_no_rsa",
                        "message": "Dans quelle ville habitez-vous ?",
                        "is_final": False,
                    }
                else:
                    return {
                        "next_state": "schooling_verification_young_no_rsa",
                        "message": "Êtes-vous scolarisé actuellement ? Veuillez répondre par oui ou non.",
                        "is_final": False,
                    }

            # Schooling verification - Adult with RSA
            elif current_state == "schooling_verification_adult_rsa":
                return {
                    "next_state": "city_verification_adult_rsa",
                    "message": "Dans quelle ville habitez-vous ?",
                    "is_final": False,
                }

            # Schooling verification - Adult without RSA
            elif current_state == "schooling_verification_adult_no_rsa":
                return {
                    "next_state": "city_verification_adult_no_rsa",
                    "message": "Dans quelle ville habitez-vous ?",
                    "is_final": False,
                }

            # City verification - Young with RSA
            elif current_state == "city_verification_young_rsa":
                city = None

                if "entities" in nlp_data and "city" in nlp_data["entities"]:
                    city = nlp_data["entities"]["city"].lower()
                elif user_data and "city" in user_data:
                    city = user_data["city"].lower()

                if city:
                    if city in ["saint-denis", "stains", "pierrefitte"]:
                        return {
                            "next_state": "eligible_ali",
                            "message": "Vous êtes éligible au programme ALI (Accompagnement Logement Insertion). Souhaitez-vous que je génère un rapport détaillé ?",
                            "is_final": True,
                            "eligibility_result": "ALI",
                        }
                    else:
                        return {
                            "next_state": "not_eligible_city",
                            "message": "Je suis désolé, mais vous n'êtes pas éligible aux programmes sociaux dans votre ville actuelle.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        }
                else:
                    return {
                        "next_state": "city_verification_young_rsa",
                        "message": "Pourriez-vous me préciser dans quelle ville vous habitez ?",
                        "is_final": False,
                    }

            # City verification - Young without RSA
            elif current_state == "city_verification_young_no_rsa":
                city = None

                if "entities" in nlp_data and "city" in nlp_data["entities"]:
                    city = nlp_data["entities"]["city"].lower()
                elif user_data and "city" in user_data:
                    city = user_data["city"].lower()

                if city:
                    ml_cities = [
                        "saint-denis",
                        "pierrefitte",
                        "saint-ouen",
                        "épinay",
                        "villetaneuse",
                        "île-saint-denis",
                    ]
                    normalized_city = city.replace(" ", "-").lower()

                    if normalized_city in ml_cities or any(
                        city in c for c in ml_cities
                    ):
                        return {
                            "next_state": "eligible_ml",
                            "message": "Vous êtes éligible au programme ML (Mission Locale). Souhaitez-vous que je génère un rapport détaillé ?",
                            "is_final": True,
                            "eligibility_result": "ML",
                        }
                    else:
                        return {
                            "next_state": "not_eligible_city",
                            "message": "Je suis désolé, mais vous n'êtes pas éligible aux programmes sociaux dans votre ville actuelle.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        }
                else:
                    return {
                        "next_state": "city_verification_young_no_rsa",
                        "message": "Pourriez-vous me préciser dans quelle ville vous habitez ?",
                        "is_final": False,
                    }

            # City verification - Adult with RSA
            elif current_state == "city_verification_adult_rsa":
                city = None

                if "entities" in nlp_data and "city" in nlp_data["entities"]:
                    city = nlp_data["entities"]["city"].lower()
                elif user_data and "city" in user_data:
                    city = user_data["city"].lower()

                if city:
                    if city in ["saint-denis", "stains", "pierrefitte"]:
                        return {
                            "next_state": "eligible_ali",
                            "message": "Vous êtes éligible au programme ALI (Accompagnement Logement Insertion). Souhaitez-vous que je génère un rapport détaillé ?",
                            "is_final": True,
                            "eligibility_result": "ALI",
                        }
                    else:
                        return {
                            "next_state": "not_eligible_city",
                            "message": "Je suis désolé, mais vous n'êtes pas éligible aux programmes sociaux dans votre ville actuelle.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        }
                else:
                    return {
                        "next_state": "city_verification_adult_rsa",
                        "message": "Pourriez-vous me préciser dans quelle ville vous habitez ?",
                        "is_final": False,
                    }

            # City verification - Adult without RSA
            elif current_state == "city_verification_adult_no_rsa":
                city = None

                if "entities" in nlp_data and "city" in nlp_data["entities"]:
                    city = nlp_data["entities"]["city"].lower()
                elif user_data and "city" in user_data:
                    city = user_data["city"].lower()

                if city:
                    plie_cities = [
                        "aubervilliers",
                        "épinay-sur-seine",
                        "île-saint-denis",
                        "la-courneuve",
                        "pierrefitte",
                        "saint-denis",
                        "saint-ouen",
                        "stains",
                        "villetaneuse",
                    ]

                    normalized_city = city.replace(" ", "-").lower()

                    if normalized_city in plie_cities or any(
                        city in c for c in plie_cities
                    ):
                        return {
                            "next_state": "eligible_plie",
                            "message": "Vous êtes éligible au programme PLIE (Plan Local pour l'Insertion et l'Emploi). Souhaitez-vous que je génère un rapport détaillé ?",
                            "is_final": True,
                            "eligibility_result": "PLIE",
                        }
                    else:
                        return {
                            "next_state": "not_eligible_city",
                            "message": "Je suis désolé, mais vous n'êtes pas éligible aux programmes sociaux dans votre ville actuelle.",
                            "is_final": True,
                            "eligibility_result": "Non éligible (ville)",
                        }
                else:
                    return {
                        "next_state": "city_verification_adult_no_rsa",
                        "message": "Pourriez-vous me préciser dans quelle ville vous habitez ?",
                        "is_final": False,
                    }

            # Fallback for any other state
            else:
                return {
                    "next_state": "error",
                    "message": "État non reconnu dans l'arbre de décision.",
                    "is_final": False,
                }
        except Exception as e:
            print(f"Error processing with decision tree: {str(e)}")
            return {
                "next_state": current_state,
                "message": "Je suis désolé, mais j'ai rencontré un problème. Pouvez-vous réessayer ?",
                "is_final": False,
            }
