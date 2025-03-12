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
            
            Retourne UNIQUEMENT un objet JSON avec le format suivant:
            {{
                "intent": "l'intention principale (provide_info, confirm, deny, ask_question, etc.)",
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
                        "content": "Tu es un assistant spécialisé dans l'analyse de texte et l'extraction d'entités.",
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
