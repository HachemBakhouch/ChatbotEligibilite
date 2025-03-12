import requests
import json
import time

# URL du service Chatbot
BASE_URL = "http://192.168.100.104:5001"  # Utilisez votre adresse IP

def test_conversation_flow():
    # Démarrer une conversation
    print("=== Démarrage de la conversation ===")
    start_response = requests.post(
        f"{BASE_URL}/conversation",
        json={"user_id": "test_user_flow"}
    )
    
    conversation_id = start_response.json().get("conversation_id")
    print(f"Conversation ID: {conversation_id}")
    print(f"Message initial: {start_response.json().get('message')}")
    
    # Étape 1: Âge (en réponse directe à la première question)
    print("\n=== Étape 1: Âge ===")
    age_response = requests.post(
        f"{BASE_URL}/process",
        json={
            "conversation_id": conversation_id,
            "text": "22 ans"
        }
    )
    print(f"Question: {age_response.json().get('message')}")
    
    # Étape 2: Consentement (répondre à la question sur le consentement)
    print("\n=== Étape 2: Consentement ===")
    consent_response = requests.post(
        f"{BASE_URL}/process",
        json={
            "conversation_id": conversation_id,
            "text": "Oui, j'accepte"
        }
    )
    print(f"Question: {consent_response.json().get('message')}")
    
    # Étape 3: Âge (répondre à nouveau car le système redemande)
    print("\n=== Étape 3: Âge (confirmation) ===")
    age_confirm_response = requests.post(
        f"{BASE_URL}/process",
        json={
            "conversation_id": conversation_id,
            "text": "22 ans"
        }
    )
    print(f"Question: {age_confirm_response.json().get('message')}")
    
    # Étape 4: RSA
    print("\n=== Étape 4: RSA ===")
    rsa_response = requests.post(
        f"{BASE_URL}/process",
        json={
            "conversation_id": conversation_id,
            "text": "Oui, je suis bénéficiaire du RSA"
        }
    )
    print(f"Question: {rsa_response.json().get('message')}")
    
    # Étape 5: Scolarisation
    print("\n=== Étape 5: Scolarisation ===")
    school_response = requests.post(
        f"{BASE_URL}/process",
        json={
            "conversation_id": conversation_id,
            "text": "Non, je ne suis pas scolarisé"
        }
    )
    print(f"Question: {school_response.json().get('message')}")
    
    # Étape 6: Ville
    print("\n=== Étape 6: Ville ===")
    city_response = requests.post(
        f"{BASE_URL}/process",
        json={
            "conversation_id": conversation_id,
            "text": "J'habite à Saint-Denis"
        }
    )
    print(f"Réponse finale: {city_response.json().get('message')}")
    print(f"Final? {city_response.json().get('is_final')}")
    
    # Récupérer l'état final
    print("\n=== État final de la conversation ===")
    conversation_response = requests.get(
        f"{BASE_URL}/conversation/{conversation_id}"
    )
    
    if conversation_response.status_code == 200:
        conversation_data = conversation_response.json()
        print(f"État final: {conversation_data.get('current_state')}")
        print(f"Résultat d'éligibilité: {conversation_data.get('eligibility_result')}")
    else:
        print(f"Erreur lors de la récupération de la conversation: {conversation_response.status_code}")

if __name__ == "__main__":
    test_conversation_flow()