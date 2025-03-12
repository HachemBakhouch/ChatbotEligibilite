import requests
import json
import time

# URL du service Chatbot
BASE_URL = "http://192.168.100.104:5001"  # Adresse IP correcte

def test_conversation():
    # Démarrer une conversation
    print("=== Démarrage de la conversation ===")
    start_response = requests.post(
        f"{BASE_URL}/conversation",
        json={"user_id": "test_user_simple"}
    )
    
    conversation_id = start_response.json().get("conversation_id")
    print(f"Conversation ID: {conversation_id}")
    print(f"Message initial: {start_response.json().get('message')}")
    
    # Test séquentiel 1: Âge
    print("\n=== Test 1: Envoi de l'âge ===")
    age_response = requests.post(
        f"{BASE_URL}/process",
        json={
            "conversation_id": conversation_id,
            "text": "J'ai 22 ans"
        }
    )
    print(f"Réponse: {age_response.json().get('message')}")
    
    # Attendre un peu pour s'assurer que l'état est mis à jour
    time.sleep(1)
    
    # Test séquentiel 2: RSA
    print("\n=== Test 2: RSA ===")
    rsa_response = requests.post(
        f"{BASE_URL}/process",
        json={
            "conversation_id": conversation_id,
            "text": "Oui, je suis bénéficiaire du RSA"
        }
    )
    print(f"Réponse: {rsa_response.json().get('message')}")
    
    # Attendre un peu
    time.sleep(1)
    
    # Test séquentiel 3: Scolarisation
    print("\n=== Test 3: Scolarisation ===")
    schooling_response = requests.post(
        f"{BASE_URL}/process",
        json={
            "conversation_id": conversation_id,
            "text": "Non, je ne suis pas scolarisé"
        }
    )
    print(f"Réponse: {schooling_response.json().get('message')}")
    
    # Attendre un peu
    time.sleep(1)
    
    # Test séquentiel 4: Ville
    print("\n=== Test 4: Ville ===")
    city_response = requests.post(
        f"{BASE_URL}/process",
        json={
            "conversation_id": conversation_id,
            "text": "J'habite à Saint-Denis"
        }
    )
    print(f"Réponse: {city_response.json().get('message')}")
    
    # Récupérer la conversation complète pour vérifier l'état
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
    test_conversation()