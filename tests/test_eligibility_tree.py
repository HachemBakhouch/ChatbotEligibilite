import requests
import json
import time
import sys

# URL du service Chatbot - modifiée pour utiliser l'adresse correcte
BASE_URL = "http://192.168.100.104:5001"  # Adresse où votre service est disponible


def test_eligibility_flow(age, rsa_status, schooling_status, city, expected_result):
    """Teste un scénario complet avec une combinaison spécifique de réponses"""
    # Démarrer une conversation
    print(
        f"\n=== Test : Âge {age}, RSA {rsa_status}, Scolarisé {schooling_status}, Ville {city} ==="
    )
    print(f"Résultat attendu : {expected_result}")

    start_response = requests.post(
        f"{BASE_URL}/conversation",
        json={
            "user_id": f"test_user_age{age}_rsa{rsa_status}_scol{schooling_status}_city{city}"
        },
    )

    if start_response.status_code != 200:
        print(
            f"ERREUR: Impossible de démarrer la conversation ({start_response.status_code})"
        )
        return False

    conversation_id = start_response.json().get("conversation_id")
    print(f"Conversation ID: {conversation_id}")

    # Étape 1: Consentement (répondre à la première question)
    print("\n- Étape 1: Consentement")
    consent_response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": "Oui, j'accepte"},
    )

    if consent_response.status_code != 200:
        print(
            f"ERREUR: Problème lors de l'envoi du consentement ({consent_response.status_code})"
        )
        return False

    print(f"Réponse: {consent_response.json().get('message')}")

    # Étape 2: Âge
    print("\n- Étape 2: Envoi de l'âge")
    age_response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": f"J'ai {age} ans"},
    )

    if age_response.status_code != 200:
        print(f"ERREUR: Problème lors de l'envoi de l'âge ({age_response.status_code})")
        return False

    print(f"Réponse: {age_response.json().get('message')}")

    # Étape 3: RSA
    print("\n- Étape 3: Statut RSA")
    rsa_text = (
        "Oui, je suis bénéficiaire du RSA"
        if rsa_status
        else "Non, je ne suis pas bénéficiaire du RSA"
    )
    rsa_response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": rsa_text},
    )

    if rsa_response.status_code != 200:
        print(
            f"ERREUR: Problème lors de l'envoi du statut RSA ({rsa_response.status_code})"
        )
        return False

    print(f"Réponse: {rsa_response.json().get('message')}")

    # Étape 4: Scolarisation
    print("\n- Étape 4: Statut Scolarisation")
    schooling_text = (
        "Oui, je suis scolarisé"
        if schooling_status
        else "Non, je ne suis pas scolarisé"
    )
    schooling_response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": schooling_text},
    )

    if schooling_response.status_code != 200:
        print(
            f"ERREUR: Problème lors de l'envoi du statut scolarisation ({schooling_response.status_code})"
        )
        return False

    print(f"Réponse: {schooling_response.json().get('message')}")

    # Étape 5: Ville
    print("\n- Étape 5: Ville")
    city_response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": f"J'habite à {city}"},
    )

    if city_response.status_code != 200:
        print(
            f"ERREUR: Problème lors de l'envoi de la ville ({city_response.status_code})"
        )
        return False

    print(f"Réponse finale: {city_response.json().get('message')}")

    # Récupérer l'état final
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


def run_all_tests():
    """Exécute une série de tests couvrant les différents chemins de l'arbre décisionnel"""

    test_cases = [
        # Tests pour les jeunes (16-25,5 ans)
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
        # Tests pour les adultes (>25,5 ans)
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
        # Tests pour âges non éligibles
        {
            "age": 15,
            "rsa": True,
            "schooling": True,
            "city": "Saint-Denis",
            "expected": "Non éligible (âge)",
        },
        {
            "age": 62,
            "rsa": True,
            "schooling": True,
            "city": "Saint-Denis",
            "expected": "Non éligible (âge)",
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
        # Pause pour éviter de surcharger le serveur
        time.sleep(1)

    # Résumé des tests
    print("\n\n========== RÉSUMÉ DES TESTS ==========")
    passed = results.count(True)
    failed = results.count(False)
    print(f"Tests réussis: {passed}/{len(results)} ({passed/len(results)*100:.2f}%)")
    print(f"Tests échoués: {failed}/{len(results)} ({failed/len(results)*100:.2f}%)")

    if failed > 0:
        print("\nTests échoués:")
        for i, (success, test) in enumerate(zip(results, test_cases)):
            if not success:
                print(
                    f"- Test {i+1}: Âge={test['age']}, RSA={test['rsa']}, Scolarisé={test['schooling']}, Ville={test['city']}"
                )
                print(f"  Attendu: {test['expected']}")

    return passed == len(results)


if __name__ == "__main__":
    print("Démarrage des tests de l'arbre décisionnel d'éligibilité...")
    if run_all_tests():
        print("\n✅ TOUS LES TESTS ONT RÉUSSI")
        sys.exit(0)
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        sys.exit(1)
