"""
Module pour la détection et le filtrage des mots interdits dans les conversations du chatbot.
Ce module surveille les messages des utilisateurs, détecte les mots vulgaires ou inappropriés,
et peut terminer une conversation si les règles sont violées plusieurs fois.
"""

import re
import json
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("banned_words_filter")


class BannedWordsFilter:
    """
    Filtre les mots interdits dans les conversations utilisateur
    et fournit des mécanismes d'avertissement et de terminaison de conversation.
    """

    def __init__(self, banned_words_file=None, max_violations=2):
        """
        Initialise le filtre de mots interdits.

        Args:
            banned_words_file (str, optional): Chemin vers le fichier contenant les mots à bannir.
                                             Par défaut: None, dans ce cas utilise la liste intégrée.
            max_violations (int, optional): Nombre maximum de violations avant terminaison.
                                          Par défaut: 2.
        """
        self.max_violations = max_violations
        self.user_violations = (
            {}
        )  # Dictionnaire pour suivre les violations par conversation

        # Liste par défaut des mots à bannir
        self.banned_words = [
            # Insultes
            "connard",
            "salopard",
            "enculé",
            "pute",
            "tepu",
            "merde",
            "trou du cul",
            "trou de balle",
            "bâtard",
            "batarde",
            "chien",
            "chienne",
            "nègre",
            "négro",
            "goudou",
            "lesboss",
            "travelo",
            "retardé",
            # Violence
            "tuer",
            "hitler",
            "haïr",
            "haine",
            "meurtre",
            "détruire",
            "agression",
            # Sexuel
            "sexe",
            "pornographie",
            "porno",
            "viol",
            "violer",
            "pédophile",
            # Drogues
            "drogue",
            "shit",
            "cocaïne",
            "héroïne",
            "pétard",
            "proto",
            "cannabis",
            "gandja",
            "moulaga",
            "moula",
            "rata",
            # Activités illégales
            "escroquerie",
            "arnaque",
            "mensonge",
            "mytho",
            "myto",
            # Argot
            "wesh",
            "nique",
            "téma",
            "bico",
            "rebeu",
            "renoi",
            "feuj",
            "gadji",
            "boloss",
            "bédave",
            "zbeul",
            "frelos",
            "tocard",
            "crari",
            "yomb",
            "poto",
            "binks",
            "kichta",
            "pélo",
            "gova",
            "bicrave",
            "charo",
            "pointeur",
            "faya",
            "la mif",
            "tiser",
            "teubé",
            "scred",
            # Expressions grossières
            "nique ta mère",
            "nique ta race",
            "j'vais t'défoncer",
            "ferme-la",
            "ftg",
            "j'vais t'enculer",
            "grosse merde",
            "espèce d'abruti",
            "dégage connard",
            "sale fils de pute",
            "connasse",
            "salope",
            "lopsa",
            "salaud",
            "fils de pute",
            "fdp",
            "fils de chien",
            "bordel",
            "ta gueule",
            "tg",
            "ferme ta gueule",
            "gros con",
            "grosse conne",
            "va te faire foutre",
            "enculeur",
            "pédé",
            "sale race",
            "bouffon",
            "débile",
            "mongol",
            "raté",
            "idiot",
            "crétin",
            "abruti",
            # Prostitution
            "escort",
            "tchoin",
            "crasseuse",
            "tapin",
            "hustler",
            "mac",
            "bicraveuse",
            "bicraveur",
            # Argent illégal
            "jnoun",
            "liasse",
            "biff",
            "flouze",
            "flouz",
            "oseille",
            "tuner",
            "zeyo",
            "placard",
            "business sale",
            "onlyfan",
            "mym",
            # Sexuel / Anatomie
            "zeubi",
            "zebi",
            "zob",
            "zboub",
            "imbécile",
            "ma gueule",
            "putain",
            "casses-toi",
            "je t'emmerde",
            "barre-toi",
            "fait-chier",
            "catin",
            "tapin",
            "bamboula",
            "biatch",
            "bitch",
            "bite",
            "teub",
            "zgeg",
            "zizi",
            "bouffone",
            "branleur",
            "casse-couille",
            # Armes
            "arme",
            "kalash",
            "couteau",
            # Autres insultes
            "ta race",
            "garce",
            "baise",
            "baiser",
            "je m'en fou",
            "je m'en fiche",
            "nique ta grand-mère",
            "nique ton père",
            "nique ta sœur",
            "nique ton frère",
            "nique tes morts",
            "mort",
            "meurtre",
            "tuer",
            "assassinat",
            "homicide",
            "féminicide",
            "blaireau",
            "coquin",
            "coquine",
            "boucaque",
            "boukak",
            "bougnoul",
            "bounioul",
            "casos",
            "ksos",
            "chintoc",
            "chintok",
            "cochon",
            "cochonne",
            "kouakoubé",
            "quoicoubé",
            "dégénéré",
            "sous-merde",
            "débilos",
            "pauv' con",
            "pov' type",
            "bougnoule",
            "grosse vache",
            "boudin",
            "clochard",
            "clocharde",
            "cul-terreux",
            "foiré",
            "pourriture",
            "raté",
            "ratée",
            "sombre merde",
            "tocard",
            "tocarde",
            "va mourir",
            "nul à chier",
            "pédé comme un phoque",
            "pleurnicheur",
            "pleureuse",
            "putréfié",
            "putréfiée",
            "sac à merde",
            "raton",
            "chinetoque",
            "youpin",
            "youpine",
            "tarlouze",
            "tafiolle",
            "gouine",
            "pédé",
            "pd",
            "bouffeur de porc",
            "bouffeur de chien",
            "niaquoué",
            "fouteux de merde",
            "face de craie",
            "michto",
            "michtonneuse",
            "j'vais t'exploser",
            "j'vais t'buter",
            "crève",
            "écraser",
            "défonce",
            "marave",
            "tabasser",
            "étriper",
            "buter",
            "égorger",
            "flinguer",
            "pisser sur ta tombe",
            "empoisonner",
            "pendaison",
            "pendre",
            "génocide",
            "exterminer",
            # Sites pornographiques
            "gang bang",
            "brazzers",
            "redtube",
            "pornhub",
            "choper",
            "se faire sucer",
            "pipe",
            "branlette",
            "fellation",
            "débauche",
            "dévergondée",
            "escort boy",
            "milf",
            "cougar",
            "nympho",
            "nymphomane",
            "sodomie",
            "xhamster",
            "xvideos",
            "pornstar",
            "film x",
            "actrice x",
            # Drogues spécifiques
            "lsd",
            "ecsta",
            "ecstasy",
            "champis",
            "meth",
            "méthamphétamine",
            "kétamine",
            "crack",
            "opium",
            "speed",
            "ghb",
            "codeine",
            "lean",
            "purple drank",
            "xanax",
            # Crime organisé
            "racket",
            "trafiquant",
            "magouille",
            "dealer",
            "passeur",
            "yakuza",
            "mafia",
            "cartel",
            "braquage",
            "cagoulé",
            "go fast",
            "suceuse",
            "suceur",
            "femelle",
            "gouïne",
            "tapette",
            "hataille",
            "rataille",
            # Variantes orthographiques / fautes sur "connard"
            "conar",
            "konard",
            "konar",
            "conard",
            "konnaard",
            "connar",
            "connnard",
            "connerd",
            "konnard",
            "konnar",
            "conardd",
            "connaaard",
            "connhard",
            "connarde",
            "konhard",
            # "enculé" variations
            "encule",
            "enculler",
            "encullé",
            "encullée",
            "enqulé",
            "enku",
            "encu",
            "enculer",
            "enculle",
            "enquler",
            "enculéé",
            "encuulé",
            "encculé",
            "encull",
            "enkulé",
            "enqqulé",
            # "pute" variations
            "putte",
            "poute",
            "putain",
            "putin",
            "puute",
            "pouta",
            "poutre",
            "poutte",
            "poutay",
            "putch",
            "put3",
            "pu7e",
            "pu*e",
            "pouteuh",
            "poutasse",
            "putinasse",
            "puten",
            "ptn",
            # "merde" variations
            "merd",
            "mairde",
            "marde",
            "m3rd",
            "m3rde",
            "mherde",
            "merdde",
            "m@erde",
            "merdasse",
            # "bâtard" variations
            "batard",
            "battard",
            "baattard",
            "bat@rd",
            "batar",
            "baatar",
            "btard",
            "btrd",
            "bataar",
            # "trou du cul"
            "trouduk",
            "trou2cul",
            "trooduku",
            "troudec",
            "troudkul",
            "troudk",
            "trouducul",
            "trouducul",
            # "chien/chienne"
            "chienneuh",
            "ch1enne",
            "chyen",
            "chi1en",
            "chiène",
            "chienn",
            "chian",
            "tchien",
            "shien",
            # "salopard"
            "salopar",
            "saloparde",
            "salaupar",
            "salopehard",
            "saloperd",
            "saleopard",
            "zalopard",
            # "pédé"
            "pd",
            "pédéé",
            "peday",
            "pedey",
            "peedé",
            "p3dé",
            "pedeuh",
            "pedu",
            "péddé",
            "pedy",
            # "nique"
            "nik",
            "niq",
            "niquer",
            "niqu",
            "niqu3",
            "n1que",
            "n1k",
            "n*que",
            "niik",
            "niqque",
            # "salope"
            "salop",
            "saloope",
            "saloppe",
            "saloopp",
            "salopeuh",
            "saalope",
            "salaupe",
            "saleoppe",
            # "tg" / "ta gueule"
            "ta guele",
            "tgueule",
            "t@gueule",
            "tgule",
            "t@g",
            "tgu",
            "ta g",
            "fermetag",
            "t'as gueule",
            # "bite" / "zgeg" / "zizi"
            "bitt",
            "byt",
            "biite",
            "zgeeg",
            "zgegg",
            "zize",
            "ziizi",
            "z1z1",
            "zigzeg",
            "b!te",
            "bizzy",
            # "teub"
            "tbeu",
            "tub",
            "t3ub",
            "teubb",
            "t@ub",
            "teuub",
            "tbeub",
            "teubé",
            "t3uub",
            "teuube",
            # "branleur"
            "branleurrr",
            "branleure",
            "branleu",
            "branleureuh",
            "branlheure",
            "brenleur",
            "brenloeur",
            # "salope" combiné
            "sale chienne",
            "grosse salope",
            "pute de merde",
            "sale garce",
            "vieille pute",
            "grosse chienne",
            "vieille salope",
            "sale tepu",
            "salope finie",
            "truie humaine",
            "garce finie",
            "sale catin",
            # "fuck" / "foutre"
            "fuk",
            "f*ck",
            "fout",
            "vaffanculo",
            "fooutre",
            "faque",
            "fawk",
            "phoque",
            "fuque",
            "fuq",
            # Générations avec lettres substituées
            "c0nn4rd",
            "encul3",
            "p*te",
            "sh1t",
            "fdp",
            "s@lope",
            "m3rd3",
            "b@t@rd",
            "s4l0p3",
            "n1qu3",
            "v@f",
            "tr0uduc",
            "s4l0p@rd",
            "ch1enne",
            "bat@rd",
            "m3uf",
            "b1atch",
            "s3x",
            "f0utre",
            # "mongol", "débile"
            "mongole",
            "mongolien",
            "débilos",
            "debilous",
            "debile",
            "d3bile",
            "d3bilos",
            "débyle",
            # "haine / tuer"
            "haïss",
            "tue-le",
            "massacrer",
            "detruir",
            "tueurs",
            "kille",
            "tuee",
            "destruction",
            "assassins",
            # "pédé" déguisé
            "pedok",
            "p3do",
            "p3dé",
            "pédéstyle",
            "petay",
            "pédézouz",
            "pdy",
            "peydé",
            "pedei",
            # "porno"
            "p0rn",
            "pornn",
            "pourn",
            "porny",
            "p*rn",
            "pr0n",
            "pounrn",
            "pornos",
            "pornni",
            "xxvideos",
            # "violer / viol"
            "viole",
            "violay",
            "violle",
            "vyolet",
            "vyoler",
            "v1ol",
            "violate",
            "raper",
            "rapay",
            # Divers déguisés ou allongés
            "connnnaard",
            "coooonard",
            "salauddd",
            "enccuuulé",
            "bittttte",
            "puttttt",
            "tgklm",
            "fdppp",
            "tgms",
            "tgconnard",
            "tgpd",
            "mgtg",
            "niksa",
            "niquezvous",
            "niquez",
            "niklm",
            "enculax",
            "niklamerde",
            "enculord",
            "saleconard",
            "ptnms",
            "ptnm",
            "tgfdp",
            "fermelagueule",
            "connasseuh",
            "saleenculé",
            "batar",
            "nickyou",
            "fayaaa",
            "nicklamer",
            # Variation de nombres / l33t
            "c0n",
            "sh1t",
            "s3x",
            "p0rn0",
            "n1k",
            "3ncule",
            "c4nnard",
            "t3ub",
            "f0utre",
            "0seill",
            "b1tc",
            "s4l3",
            "t1z",
            "k1chta",
        ]

        # Charger les mots depuis un fichier si spécifié
        if banned_words_file:
            try:
                self.load_banned_words(banned_words_file)
            except Exception as e:
                logger.error(
                    f"Erreur lors du chargement du fichier de mots interdits: {e}"
                )
                logger.info("Utilisation de la liste de mots interdits par défaut")

    def load_banned_words(self, filepath):
        """
        Charge la liste des mots interdits depuis un fichier.

        Args:
            filepath (str): Chemin vers le fichier contenant les mots interdits.
                          Peut être un fichier texte (un mot par ligne) ou JSON.

        Raises:
            FileNotFoundError: Si le fichier n'existe pas.
            ValueError: Si le format du fichier n'est pas reconnu ou valide.
        """
        logger.info(f"Chargement des mots interdits depuis {filepath}")

        if filepath.endswith(".json"):
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    self.banned_words = [word.lower() for word in data]
                elif isinstance(data, dict) and "words" in data:
                    self.banned_words = [word.lower() for word in data["words"]]
                else:
                    raise ValueError(
                        "Format JSON invalide. Attendu: liste ou dict avec clé 'words'"
                    )
        elif filepath.endswith(".txt") or filepath.endswith(".docx"):
            # Pour .docx, cela suppose que le contenu a été extrait au préalable
            words = []
            with open(filepath, "r", encoding="utf-8") as file:
                for line in file:
                    word = line.strip()
                    if word and not word.startswith("#"):  # Ignorer les commentaires
                        words.append(word.lower())
            self.banned_words = words
        else:
            raise ValueError(f"Format de fichier non pris en charge: {filepath}")

        logger.info(f"Chargé {len(self.banned_words)} mots interdits")

    def check_message(self, conversation_id, message):
        """
        Vérifie si un message contient des mots interdits et met à jour le compteur de violations.

        Args:
            conversation_id (str): Identifiant unique de la conversation.
            message (str): Message à vérifier.

        Returns:
            dict: Résultat contenant:
                - 'contains_banned_words' (bool): True si des mots interdits sont détectés
                - 'banned_words_found' (list): Liste des mots interdits trouvés
                - 'should_warn' (bool): True si un avertissement devrait être émis
                - 'should_terminate' (bool): True si la conversation devrait être terminée
                - 'violation_count' (int): Nombre actuel de violations
        """
        if not message or not isinstance(message, str):
            return {
                "contains_banned_words": False,
                "banned_words_found": [],
                "should_warn": False,
                "should_terminate": False,
                "violation_count": self.user_violations.get(conversation_id, 0),
            }

        # Convertir en minuscules pour une comparaison insensible à la casse
        message_lower = message.lower()
        banned_words_found = []

        # Vérifier chaque mot interdit
        for word in self.banned_words:
            # Correspondance de mot entier avec des limites de mots
            pattern = r"\b" + re.escape(word) + r"\b"
            if re.search(pattern, message_lower):
                banned_words_found.append(word)

        contains_banned_words = len(banned_words_found) > 0

        # Mettre à jour le compteur de violations si des mots interdits sont trouvés
        if contains_banned_words:
            if conversation_id not in self.user_violations:
                self.user_violations[conversation_id] = 0
            self.user_violations[conversation_id] += 1

        violation_count = self.user_violations.get(conversation_id, 0)
        should_warn = contains_banned_words and violation_count == 1
        should_terminate = violation_count >= self.max_violations

        return {
            "contains_banned_words": contains_banned_words,
            "banned_words_found": banned_words_found,
            "should_warn": should_warn,
            "should_terminate": should_terminate,
            "violation_count": violation_count,
        }

    def get_warning_message(self):
        """
        Retourne un message d'avertissement pour l'utilisateur.

        Returns:
            str: Message d'avertissement.
        """
        return (
            "⚠️ Attention ! Ton message contient un mot non autorisé. "
            "Pour garantir un échange respectueux et convivial, merci de reformuler ta question sans mots interdits. 😊"
            "Si cela se reproduit, notre échange devra être interrompu."
        )

    def get_termination_message(self):
        """
        Retourne un message de fin de conversation.

        Returns:
            str: Message de fin de conversation.
        """
        return (
            "⚠️ Attention ! Votre conversation est interrompue en raison d'un langage inapproprié répété. "
            "Notre service vise à maintenir un environnement respectueux et convivial. "
            "Vous pouvez réessayer ultérieurement en respectant nos conditions d'utilisation."
        )

    def reset_violations(self, conversation_id):
        """
        Réinitialise le compteur de violations pour une conversation donnée.

        Args:
            conversation_id (str): Identifiant de la conversation.
        """
        if conversation_id in self.user_violations:
            del self.user_violations[conversation_id]
            logger.info(
                f"Réinitialisation des violations pour la conversation {conversation_id}"
            )


# Exemple d'utilisation
if __name__ == "__main__":
    # Créer une instance du filtre
    word_filter = BannedWordsFilter()

    # Tester avec quelques messages
    test_messages = [
        "Bonjour, comment puis-je vous aider ?",
        "Je ne comprends pas pourquoi ce con ne me répond pas",
        "Allez-vous faire foutre avec votre service",
    ]

    test_conversation_id = "test-123"

    for msg in test_messages:
        print(f"\nMessage: {msg}")
        result = word_filter.check_message(test_conversation_id, msg)
        print(f"Contient des mots interdits: {result['contains_banned_words']}")
        if result["contains_banned_words"]:
            print(f"Mots trouvés: {result['banned_words_found']}")
        print(f"Violations: {result['violation_count']}")

        if result["should_warn"]:
            print(f"AVERTISSEMENT: {word_filter.get_warning_message()}")

        if result["should_terminate"]:
            print(f"TERMINAISON: {word_filter.get_termination_message()}")
