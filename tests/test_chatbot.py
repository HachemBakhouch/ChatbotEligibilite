import requests
import json

# URL du service Chatbot
BASE_URL = "http://192.168.100.104:5001"  # Utilisez l'adresse IP correcte

def test_start_conversation():
    """Test démarrage d'une conversation"""
    response = requests.post(
        f"{BASE_URL}/conversation",
        json={"user_id": "test_user_001"}
    )
    
    print("Status code:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))
    
    return response.json().get("conversation_id")

def test_process_message(conversation_id, message):
    """Test envoi d'un message"""
    print(f"Sending message: {message}")
    response = requests.post(
        f"{BASE_URL}/process",
        json={
            "conversation_id": conversation_id,
            "text": message
        }
    )
    
    print("Status code:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))
    
    return response.json()

def main():
    # Démarrer une conversation
    print("=== Test démarrage conversation ===")
    conversation_id = test_start_conversation()
    
    if not conversation_id:
        print("Erreur: Impossible de démarrer la conversation")
        return
    
    # Test avec un message d'âge très simple
    print("\n=== Test envoi âge ===")
    test_process_message(conversation_id, "22 ans")
    
    # Test avec un message RSA très simple
    print("\n=== Test envoi RSA ===")
    test_process_message(conversation_id, "Oui RSA")
    
    # Test avec un message scolarisation très simple
    print("\n=== Test envoi scolarisation ===")
    test_process_message(conversation_id, "Non scolarisé")
    
    # Test avec un message ville très simple
    print("\n=== Test envoi ville ===")
    test_process_message(conversation_id, "Saint-Denis")

if __name__ == "__main__":
    main()