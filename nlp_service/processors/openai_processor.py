import json
import requests


class OpenAIProcessor:
    """Processes text using OpenAI's API for NLP tasks"""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def analyze(self, text, language="fr"):
        """
        Analyze text to extract intent and entities

        Args:
            text (str): Text to analyze
            language (str): Language code (default: 'fr')

        Returns:
            dict: Analysis results with intent and entities
        """
        try:
            # Prepare the prompt for intent and entity extraction
            prompt = f"""
            Analyse le texte suivant et extrait l'intention et les entités.
            
            Texte: "{text}"
            
            Instructions spécifiques:
            - Si le texte contient des mots comme "oui", "bien sûr", "d'accord", "ok", considère l'intention comme "yes"
            - Si le texte contient des mots comme "non", "pas", "ne pas", considère l'intention comme "no"
            - Si le texte mentionne le RSA de façon positive, ajoute l'entité "rsa" = true
            - Si le texte mentionne le RSA de façon négative, ajoute l'entité "rsa" = false
            - Si le texte inclut un âge, extrait-le comme entité "age"
            
            Retourne UNIQUEMENT un objet JSON avec le format suivant:
            {{
                "intent": "l'intention principale (provide_info, yes, no, ask_question, etc.)",
                "entities": {{
                    "age": nombre si présent,
                    "city": ville si mentionnée,
                    "rsa": true/false si mentionné,
                    "schooling": true/false si mentionné
                }},
                "sentiment": "positif/neutre/négatif",
                "confidence": valeur entre 0 et 1,
                "text": le texte original
            }}
            """

            # Prepare the request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            data = {
                "model": "gpt-4",
                "messages": [
                    {
                        "role": "system",
                        "content": "Tu es un assistant spécialisé dans l'analyse de texte et l'extraction d'entités. Tu dois être particulièrement attentif aux intentions affirmatives (oui) et négatives (non), ainsi qu'aux mentions du RSA.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.3,
            }

            # Make the request
            response = requests.post(self.api_url, headers=headers, json=data)

            # Process the response
            if response.status_code == 200:
                result = response.json()
                content = (
                    result.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "{}")
                )

                try:
                    # Parse the JSON response
                    parsed_result = json.loads(content)
                    # Add the original text
                    parsed_result["text"] = text

                    # Fallback detection for yes/no intents and RSA entity
                    lower_text = text.lower()

                    # Override intent for clear yes/no cases if not already detected
                    if parsed_result.get("intent") not in ["yes", "no"]:
                        yes_keywords = [
                            "oui",
                            "yes",
                            "ok",
                            "d'accord",
                            "bien sûr",
                            "certainement",
                            "absolument",
                        ]
                        no_keywords = ["non", "no", "nope", "pas"]

                        if any(kw in lower_text for kw in yes_keywords):
                            parsed_result["intent"] = "yes"
                            print(f"Intent override: 'yes' detected in: '{text}'")
                        elif any(kw in lower_text for kw in no_keywords):
                            parsed_result["intent"] = "no"
                            print(f"Intent override: 'no' detected in: '{text}'")

                    # Detect RSA if not already present in entities
                    if "rsa" not in parsed_result.get("entities", {}):
                        if "rsa" in lower_text or "revenu de solidarité" in lower_text:
                            if any(
                                neg in lower_text for neg in ["non", "pas", "ne pas"]
                            ):
                                parsed_result.setdefault("entities", {})["rsa"] = False
                                print(
                                    f"Entity override: 'rsa'=False detected in: '{text}'"
                                )
                            else:
                                parsed_result.setdefault("entities", {})["rsa"] = True
                                print(
                                    f"Entity override: 'rsa'=True detected in: '{text}'"
                                )

                    return parsed_result
                except json.JSONDecodeError:
                    # Fallback if the response isn't valid JSON
                    return {
                        "intent": "unknown",
                        "entities": {},
                        "sentiment": "neutral",
                        "confidence": 0.5,
                        "text": text,
                    }
            else:
                raise Exception(f"API error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Analysis error: {str(e)}")
            # Return a default response in case of error
            return {
                "intent": "unknown",
                "entities": {},
                "sentiment": "neutral",
                "confidence": 0.5,
                "text": text,
            }
