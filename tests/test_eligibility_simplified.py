import requests
import json
import time
import sys

# URL du service Chatbot - modifiée pour utiliser l'adresse correcte
BASE_URL = "http://192.168.100.104:5001"  # Adresse où votre service est disponible


def test_eligibility_flow(age, rsa_status, schooling_status, city, expected_result):
    """Teste un scénario complet en envoyant un message unique contenant toutes les données"""
    # Démarrer une conversation
    print(
        f"\n=== Test : Âge {age}, RSA {rsa_status}, Scolarisé {schooling_status}, Ville {city} ==="
    )
    print(f"Résultat attendu : {expected_result}")

    start_response = requests.post(
        f"{BASE_URL}/conversation", json={"user_id": f"test_user_flow"}
    )

    if start_response.status_code != 200:
        print(
            f"ERREUR: Impossible de démarrer la conversation ({start_response.status_code})"
        )
        return False

    conversation_id = start_response.json().get("conversation_id")
    print(f"Conversation ID: {conversation_id}")

    # Étape 1: Envoi de l'âge
    print("\n- Envoi des informations complètes")
    text_message = f"Je suis {rsa_status and 'bénéficiaire' or 'non bénéficiaire'} du RSA, j'ai {age} ans, je suis {schooling_status and '' or 'non '}scolarisé et j'habite à {city}."
    print(f"Message envoyé: {text_message}")

    response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": text_message},
    )

    if response.status_code != 200:
        print(f"ERREUR: Problème lors de l'envoi du message ({response.status_code})")
        return False

    print(f"Réponse initiale: {response.json().get('message')}")

    # Vérifier l'état de la conversation après quelques secondes pour laisser le temps aux données d'être traitées
    time.sleep(2)

    # Récupérer l'état final
    conversation_response = requests.get(f"{BASE_URL}/conversation/{conversation_id}")

    if conversation_response.status_code != 200:
        print(
            f"ERREUR: Impossible de récupérer l'état final ({conversation_response.status_code})"
        )
        return False

    conversation_data = conversation_response.json()

    # Envoyer un second message pour finir la conversation
    second_response = requests.post(
        f"{BASE_URL}/process",
        json={
            "conversation_id": conversation_id,
            "text": "Merci pour ces informations.",
        },
    )

    if second_response.status_code != 200:
        print(
            f"ERREUR: Problème lors de l'envoi du second message ({second_response.status_code})"
        )
        return False

    print(f"Réponse finale: {second_response.json().get('message')}")

    # Récupérer l'état final après le second message
    conversation_response = requests.get(f"{BASE_URL}/conversation/{conversation_id}")

    if conversation_response.status_code != 200:
        print(
            f"ERREUR: Impossible de récupérer l'état final ({conversation_response.status_code})"
        )
        return False

    conversation_data = conversation_response.json()
    actual_result = conversation_data.get("eligibility_result")

    print(f"\nRésultat obtenu: {actual_result}")
    if actual_result == expected_result:
        print("✅ TEST RÉUSSI: Le résultat correspond à l'attendu")
        return True
    else:
        print(
            f"❌ TEST ÉCHOUÉ: Le résultat ne correspond pas à l'attendu ({actual_result} ≠ {expected_result})"
        )
        return False


def test_direct_age_cases():
    """Test spécifique pour les cas de non-éligibilité par âge"""

    # Test pour âge < 16
    print("\n=== Test direct : Âge 15 ans (trop jeune) ===")
    start_response = requests.post(
        f"{BASE_URL}/conversation", json={"user_id": "test_age_15"}
    )

    conversation_id = start_response.json().get("conversation_id")

    requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": "J'ai 15 ans"},
    )

    time.sleep(1)

    age_response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": "Oui, j'ai bien 15 ans"},
    )

    print(f"Réponse: {age_response.json().get('message')}")

    conversation_response = requests.get(f"{BASE_URL}/conversation/{conversation_id}")

    conversation_data = conversation_response.json()
    result = conversation_data.get("eligibility_result")

    print(f"Résultat: {result}")
    print("✓" if result == "Non éligible (âge)" else "✗")

    # Test pour âge >= 62
    print("\n=== Test direct : Âge 62 ans (trop âgé) ===")
    start_response = requests.post(
        f"{BASE_URL}/conversation", json={"user_id": "test_age_62"}
    )

    conversation_id = start_response.json().get("conversation_id")

    requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": "J'ai 62 ans"},
    )

    time.sleep(1)

    age_response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": "Oui, j'ai 62 ans"},
    )

    print(f"Réponse: {age_response.json().get('message')}")

    conversation_response = requests.get(f"{BASE_URL}/conversation/{conversation_id}")

    conversation_data = conversation_response.json()
    result = conversation_data.get("eligibility_result")

    print(f"Résultat: {result}")
    print("✓" if result == "Non éligible (âge)" else "✗")

    return result == "Non éligible (âge)"


def run_eligibility_tests():
    """Exécute une série de tests pour vérifier l'arbre décisionnel"""

    test_cases = [
        # Tests pour les jeunes avec RSA (16-25,5 ans)
        {
            "age": 22,
            "rsa": True,
            "schooling": True,
            "city": "Saint-Denis",
            "expected": "ALI",
        },
        {
            "age": 22,
            "rsa": True,
            "schooling": False,
            "city": "Saint-Denis",
            "expected": "ALI",
        },
        {
            "age": 22,
            "rsa": True,
            "schooling": True,
            "city": "Aubervilliers",
            "expected": "Non éligible (ville)",
        },
        # Tests pour les jeunes sans RSA (16-25,5 ans)
        {
            "age": 22,
            "rsa": False,
            "schooling": True,
            "city": "Saint-Denis",
            "expected": "Non éligible (scolarisation)",
        },
        {
            "age": 22,
            "rsa": False,
            "schooling": False,
            "city": "Saint-Denis",
            "expected": "ML",
        },
        {
            "age": 22,
            "rsa": False,
            "schooling": False,
            "city": "Épinay",
            "expected": "ML",
        },
        {
            "age": 22,
            "rsa": False,
            "schooling": False,
            "city": "Montfermeil",
            "expected": "Non éligible (ville)",
        },
        # Tests pour les adultes avec RSA (>25,5 ans)
        {
            "age": 30,
            "rsa": True,
            "schooling": True,
            "city": "Saint-Denis",
            "expected": "ALI",
        },
        {
            "age": 30,
            "rsa": True,
            "schooling": False,
            "city": "Saint-Denis",
            "expected": "ALI",
        },
        {
            "age": 30,
            "rsa": True,
            "schooling": True,
            "city": "Aubervilliers",
            "expected": "Non éligible (ville)",
        },
        # Tests pour les adultes sans RSA (>25,5 ans)
        {
            "age": 30,
            "rsa": False,
            "schooling": True,
            "city": "Saint-Denis",
            "expected": "PLIE",
        },
        {
            "age": 30,
            "rsa": False,
            "schooling": False,
            "city": "Aubervilliers",
            "expected": "PLIE",
        },
        {
            "age": 30,
            "rsa": False,
            "schooling": True,
            "city": "Villetaneuse",
            "expected": "PLIE",
        },
        {
            "age": 30,
            "rsa": False,
            "schooling": False,
            "city": "Montfermeil",
            "expected": "Non éligible (ville)",
        },
    ]

    results = []
    for i, test in enumerate(test_cases):
        print(
            f"\n==================== TEST {i+1}/{len(test_cases)} ===================="
        )
        success = test_eligibility_flow(
            test["age"], test["rsa"], test["schooling"], test["city"], test["expected"]
        )
        results.append(success)
        time.sleep(2)  # Pause entre les tests

    # Test des cas spéciaux pour l'âge
    age_test_15 = test_direct_age_cases()

    # Résumé des tests
    passed = results.count(True)
    failed = results.count(False)

    print("\n\n========== RÉSUMÉ DES TESTS ==========")
    print(
        f"Tests réussis: {passed}/{len(results)} ({passed/len(results)*100:.2f}% si > 0)"
    )
    print(
        f"Tests échoués: {failed}/{len(results)} ({failed/len(results)*100:.2f}% si > 0)"
    )

    if failed > 0:
        print("\nTests échoués:")
        for i, (success, test) in enumerate(zip(results, test_cases)):
            if not success:
                print(
                    f"- Test {i+1}: Âge={test['age']}, RSA={test['rsa']}, Scolarisé={test['schooling']}, Ville={test['city']}"
                )
                print(f"  Attendu: {test['expected']}")


if __name__ == "__main__":
    print("Démarrage des tests d'éligibilité...\n")
    run_eligibility_tests()
