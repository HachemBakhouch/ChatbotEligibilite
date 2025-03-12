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
            "eligibility_result": None
        }
        
        return conversation_id
    
    def get_welcome_message(self):
        """Return the welcome message to start the conversation"""
        return "Bonjour, je suis un chatbot qui peut vous aider à déterminer votre éligibilité aux programmes sociaux. Commençons par quelques questions. Quel est votre âge ?"
    
    def process_message(self, conversation_id, text):
        """Process user message and advance the conversation"""
        if conversation_id not in self.conversations:
            raise Exception("Conversation not found")
            
        conversation = self.conversations[conversation_id]
        
        # Add user message to history
        conversation["messages"].append({
            "role": "user",
            "content": text,
            "timestamp": datetime.now().isoformat()
        })
        
        # Process with NLP service
        nlp_response = self._process_with_nlp(text)
        print(f"NLP Response: {json.dumps(nlp_response)}")
        
        # Get next step from decision tree
        decision_response = self._process_with_decision_tree(
            conversation_id, 
            conversation["current_state"], 
            nlp_response
        )
        
        # Update conversation state
        conversation["current_state"] = decision_response.get("next_state", conversation["current_state"])
        
        if "eligibility_result" in decision_response:
            conversation["eligibility_result"] = decision_response["eligibility_result"]
        
        # Add bot response to history
        conversation["messages"].append({
            "role": "bot",
            "content": decision_response.get("message", "Je n'ai pas compris. Pouvez-vous répéter ?"),
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "message": decision_response.get("message"),
            "conversation_id": conversation_id,
            "is_final": decision_response.get("is_final", False)
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
            age_match = re.search(r'\d+', text)
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
            cities = ['saint-denis', 'stains', 'pierrefitte', 'saint-ouen', 'épinay', 'villetaneuse', 
                     'île-saint-denis', 'aubervilliers', 'épinay-sur-seine', 'la courneuve']
            for city in cities:
                if city in text.lower() or city.replace('-', ' ') in text.lower():
                    entities["city"] = city
                    break
            
            # Déterminer l'intention
            intent = "provide_info"
            if "?" in text:
                intent = "ask_question"
            elif "oui" in text.lower() or "yes" in text.lower():
                intent = "yes"
            elif "non" in text.lower() or "no" in text.lower():
                intent = "no"
            
            return {
                "intent": intent,
                "entities": entities,
                "text": text,
                "sentiment": "neutral",
                "confidence": 0.8
            }
        except Exception as e:
            print(f"Error processing with NLP: {str(e)}")
            return {"intent": "unknown", "entities": {}}
    
    def _process_with_decision_tree(self, conversation_id, current_state, nlp_data):
        """Get next step from decision tree service"""
        try:
            print(f"Calling decision tree service with: state={current_state}, nlp_data={json.dumps(nlp_data)}")
            
            # Tenter d'appeler le service d'arbre décisionnel réel
            try:
                decision_tree_url = f"{Config.DECISION_TREE_SERVICE_URL}/evaluate"
                print(f"Sending request to: {decision_tree_url}")
                
                payload = {
                    "conversation_id": conversation_id,
                    "current_state": current_state,
                    "nlp_data": nlp_data
                }
                print(f"Payload: {json.dumps(payload)}")
                
                response = requests.post(
                    decision_tree_url,
                    json=payload
                )
                
                print(f"Decision tree response status: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"Decision tree result: {json.dumps(result)}")
                    return result
                else:
                    print(f"Decision tree service returned an error: {response.status_code} - {response.text}")
                    # Continue with fallback
            except Exception as api_error:
                print(f"Failed to call decision tree service: {str(api_error)}")
                # Continue with fallback
            
            # Simulation comme plan de secours
            print("Using fallback decision tree logic")
            if current_state == "initial":
                return {
                    "next_state": "age_verification",
                    "message": "Pourriez-vous confirmer votre âge, s'il vous plaît ?",
                    "is_final": False
                }
            elif current_state == "age_verification":
                return {
                    "next_state": "rsa_verification",
                    "message": "Êtes-vous bénéficiaire du RSA ?",
                    "is_final": False
                }
            else:
                return {
                    "next_state": "final",
                    "message": "Basé sur vos réponses, vous pourriez être éligible au programme ALI. Voulez-vous que je génère un rapport détaillé ?",
                    "is_final": True,
                    "eligibility_result": "ALI"
                }
        except Exception as e:
            print(f"Error processing with decision tree: {str(e)}")
            return {
                "next_state": current_state,
                "message": "Je suis désolé, mais j'ai rencontré un problème. Pouvez-vous réessayer ?",
                "is_final": False
            }