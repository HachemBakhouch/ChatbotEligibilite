import requests
import json
import time

# URL du service Chatbot
BASE_URL = "http://192.168.100.104:5001"  # Adresse où votre service est disponible


def test_scenario(age, rsa, scolarise, ville, resultat_attendu):
    """Test un scénario d'éligibilité étape par étape"""
    print(
        f"\n=== Test : Âge {age}, RSA {rsa}, Scolarisé {scolarise}, Ville {ville} ==="
    )
    print(f"Résultat attendu : {resultat_attendu}")

    # Démarrer une conversation
    start_response = requests.post(
        f"{BASE_URL}/conversation",
        json={"user_id": f"test_{age}_{rsa}_{scolarise}_{ville}"},
    )

    if start_response.status_code != 200:
        print(
            f"ERREUR: Impossible de démarrer la conversation ({start_response.status_code})"
        )
        return False

    conversation_id = start_response.json().get("conversation_id")
    print(f"Conversation ID: {conversation_id}")

    # Accepter le consentement
    consent_response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": "Oui, j'accepte"},
    )

    if consent_response.status_code != 200:
        print(
            f"ERREUR: Problème lors de l'envoi du consentement ({consent_response.status_code})"
        )
        return False

    # Envoyer l'âge
    age_response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": f"J'ai {age} ans"},
    )

    if age_response.status_code != 200:
        print(f"ERREUR: Problème lors de l'envoi de l'âge ({age_response.status_code})")
        return False

    # Si l'âge est hors limites, vérifier le résultat directement
    if age < 16 or age >= 62:
        time.sleep(1)
        conversation_response = requests.get(
            f"{BASE_URL}/conversation/{conversation_id}"
        )
        eligibility_result = conversation_response.json().get("eligibility_result")

        if eligibility_result == "Non éligible (âge)":
            print("✅ TEST RÉUSSI: Non éligible par âge")
            return True
        else:
            print(
                f"❌ TEST ÉCHOUÉ: Attendu 'Non éligible (âge)', obtenu '{eligibility_result}'"
            )
            return False

    # Envoyer le statut RSA
    rsa_text = (
        "Oui, je suis bénéficiaire du RSA"
        if rsa
        else "Non, je ne suis pas bénéficiaire du RSA"
    )
    rsa_response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": rsa_text},
    )

    # Envoyer le statut de scolarisation
    scolarise_text = (
        "Oui, je suis scolarisé" if scolarise else "Non, je ne suis pas scolarisé"
    )
    scolarise_response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": scolarise_text},
    )

    # Si jeune, non RSA et scolarisé, vérifier le résultat directement
    if age <= 25.5 and not rsa and scolarise:
        time.sleep(1)
        conversation_response = requests.get(
            f"{BASE_URL}/conversation/{conversation_id}"
        )
        eligibility_result = conversation_response.json().get("eligibility_result")

        if eligibility_result == "Non éligible (scolarisation)":
            print("✅ TEST RÉUSSI: Non éligible par scolarisation")
            return True
        else:
            print(
                f"❌ TEST ÉCHOUÉ: Attendu 'Non éligible (scolarisation)', obtenu '{eligibility_result}'"
            )
            return False

    # Envoyer la ville
    ville_response = requests.post(
        f"{BASE_URL}/process",
        json={"conversation_id": conversation_id, "text": f"J'habite à {ville}"},
    )

    # Attendre le traitement
    time.sleep(2)

    # Vérifier le résultat final
    conversation_response = requests.get(f"{BASE_URL}/conversation/{conversation_id}")
    eligibility_result = conversation_response.json().get("eligibility_result")

    print(f"Résultat obtenu: {eligibility_result}")
    if eligibility_result == resultat_attendu:
        print("✅ TEST RÉUSSI")
        return True
    else:
        print(
            f"❌ TEST ÉCHOUÉ: Attendu '{resultat_attendu}', obtenu '{eligibility_result}'"
        )
        return False


def run_tests():
    tests = [
        # Cas limite d'âge
        {
            "age": 15,
            "rsa": True,
            "scolarise": True,
            "ville": "Saint-Denis",
            "attendu": "Non éligible (âge)",
        },
        {
            "age": 62,
            "rsa": True,
            "scolarise": False,
            "ville": "Saint-Denis",
            "attendu": "Non éligible (âge)",
        },
        # Jeunes (16-25.5) avec RSA
        {
            "age": 22,
            "rsa": True,
            "scolarise": True,
            "ville": "Saint-Denis",
            "attendu": "ALI",
        },
        {
            "age": 22,
            "rsa": True,
            "scolarise": False,
            "ville": "Saint-Denis",
            "attendu": "ALI",
        },
        {
            "age": 22,
            "rsa": True,
            "scolarise": True,
            "ville": "Aubervilliers",
            "attendu": "Non éligible (ville)",
        },
        # Jeunes (16-25.5) sans RSA
        {
            "age": 22,
            "rsa": False,
            "scolarise": True,
            "ville": "Saint-Denis",
            "attendu": "Non éligible (scolarisation)",
        },
        {
            "age": 22,
            "rsa": False,
            "scolarise": False,
            "ville": "Saint-Denis",
            "attendu": "ML",
        },
        {
            "age": 22,
            "rsa": False,
            "scolarise": False,
            "ville": "Épinay",
            "attendu": "ML",
        },
        # Adultes (>25.5) avec RSA
        {
            "age": 30,
            "rsa": True,
            "scolarise": True,
            "ville": "Saint-Denis",
            "attendu": "ALI",
        },
        {
            "age": 30,
            "rsa": True,
            "scolarise": False,
            "ville": "Stains",
            "attendu": "ALI",
        },
        # Adultes (>25.5) sans RSA
        {
            "age": 30,
            "rsa": False,
            "scolarise": True,
            "ville": "Saint-Denis",
            "attendu": "PLIE",
        },
        {
            "age": 30,
            "rsa": False,
            "scolarise": False,
            "ville": "Aubervilliers",
            "attendu": "PLIE",
        },
    ]

    resultats = []
    for i, test in enumerate(tests):
        print(f"\n==================== TEST {i+1}/{len(tests)} ====================")
        success = test_scenario(
            test["age"], test["rsa"], test["scolarise"], test["ville"], test["attendu"]
        )
        resultats.append(success)
        time.sleep(2)

    # Résumé
    reussis = resultats.count(True)
    echoues = resultats.count(False)
    print("\n\n========== RÉSUMÉ DES TESTS ==========")
    print(
        f"Tests réussis: {reussis}/{len(resultats)} ({reussis/len(resultats)*100:.2f}% si > 0)"
    )
    print(
        f"Tests échoués: {echoues}/{len(resultats)} ({echoues/len(resultats)*100:.2f}% si > 0)"
    )


if __name__ == "__main__":
    print("Démarrage des tests d'arbre décisionnel...\n")
    run_tests()
