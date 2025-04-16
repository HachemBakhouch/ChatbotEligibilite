"""
Module contenant les variantes des noms de villes pour aider à la détection
dans les réponses des utilisateurs du chatbot d'éligibilité.

Ce fichier est conçu pour être placé dans le dossier:
decision_tree_service/data/city_variants.py
"""

CITY_VARIANTS = {
    "saint-denis": [
        # Orthographes standard
        "saint-denis",
        "saint denis",
        "st-denis",
        "st denis",
        # Codes postaux
        "93200",
        "93 200",
        "93.200",
        "932 00",
        "93-200",
        "93200 saint denis",
        "93200 st denis",
        # Nombres écrits en toutes lettres
        "quatre-vingt-treize deux cents",
        "quatre vingt treize deux cents",
        # Variantes orthographiques et fautes courantes
        "sint deni",
        "sent denis",
        "sant denis",
        "sain denis",
        "sain deni",
        "saintdnis",
        "saiint denis",
        "saind denis",
        "saint-denys",
        "st.denis",
        "denis",
        "san denis",
        "san-denis",
        "sain denys",
        "s-denis",
        "saintenis",
        "saint_denis",
        "st_denis",
        "st.dénis",
        "s-d",
        "ville saint denis",
        "commune de saint denis",
        "st-dns",
        "sain-denis",
        "sen denis",
        "sndenis",
        "snt-denis",
        "snt denis",
        "sain dnis",
        "s.denis",
        "snt.denis",
        "sint-dnis",
        "sin deni",
        "sen deni",
        "sent-dns",
        "saintdénis",
        "st dénis",
        "saint dénis",
        "st. dénis",
        "saintdénys",
        # Nouvelles variantes
        "sdenis",
        "st-deni",
        "saintedenis",
        "st denis 93",
        "saint-denis 93",
        "saint-denis93",
        "st-denis93",
        "saint-denis seine saint denis",
        "st denis ssd",
        "saint-denis ssd",
        "sd",
        "std",
        "st-denis cedex",
        "saint denis cedex",
        "93200 cedex",
        "saint denis 93200",
        "st denis 93200",
        "ssaint denis",
        "saint dennis",
        "saint-dennis",
        "saint-deni",
        "saint deni",
        "saint denis ville",
        "stade de france",
        "la plaine",
        "la plaine saint denis",
        "la plaine st denis",
        "plaine saint denis",
        "plaine st denis",
        "ville de saint denis",
        "mairie de saint denis",
        "hotel de ville saint denis",
        "93 saint denis",
        "93 st denis",
        "sainr-denis",  # t/r adjacents sur clavier
        "saintt denis",  # double lettre par erreur
        "saibt-denis",  # n/b adjacents
        "szint-denis",  # a/z adjacents
        "saint-denid",  # s/d adjacents
        "saint-denia",  # a/s adjacents
        "xaint-denis",  # s/x adjacents
        "saint-demis",  # n/m adjacents
        "saint-denie",  # s/e adjacents
        "saint-denus",  # i/u adjacents
        "saijt-denis",  # n/j adjacents
        "sainh-denis",  # t/h adjacents
        "saint-denkis",  # i/k adjacents
        "sawnt-denis",  # i/w adjacents
        "saint-deniss",  # double s par erreur
        "dsaint-denis",  # inversion première lettre
        "aint-denis",  # oubli première lettre
        "saint-deni",  # oubli dernière lettre
        "saint-denisz",  # ajout z en fin
        "siant-denis",  # inversion ia
        "sain-tdenis",  # espace mal placé
        "saintd-enis",  # espace mal placé
        "saint-dnis",  # omission d'une lettre
        "saint-deis",  # omission d'une lettre
        "saint-deniz",  # s/z confusion sonore
        "saint-deni5",  # s/5 confusion visuelle
        "sainr deni5",  # plusieurs erreurs combinées
        "93ooo",  # confusion visuelle 0/2
        "93 saint denis",  # code postal + ville
        "sainte-denise",  # féminisation
        "saint-denise",  # féminisation
        "saint-denys",  # orthographe ancienne
        "st-dennys",  # orthographe variante
        "93200 saintdenis",  # code postal sans espace
        "st-deniiss",  # duplication lettre
        "93200sd",  # code postal + initiales
        "saint-denns",  # lettre manquante
        "saindennis",  # lettre manquante et duplication
        "saintednise",  # inversion de lettres
        "saintdienis",  # inversion de lettres
        "seintdenise",  # variation orthographique
        "sein denis",  # confusion avec "seine"
        "saintden",  # abréviation
        "sdns",  # acronyme
        "s-d-93",  # acronyme avec code
        "93st-d",  # code postal avec initiales
        "stdennis93",  # forme contractée avec code postal
        "93denis",  # code postal avec partie du nom
        "saint-denis9320",  # code postal incomplet
        "saintd93",  # forme contractée avec partie du code
        "saint-denis-93200",  # forme avec tirets
        "st-dni",  # abréviation extrême
        "s.denis.93",  # ponctuation alternative
    ],
    "stains": [
        # Orthographes standard
        "stains",
        # Codes postaux
        "93240",
        "93 240",
        "93.240",
        "932 40",
        "93-240",
        "93240 stains",
        # Nombres écrits en toutes lettres
        "quatre-vingt-treize deux cent quarante",
        "quatre vingt treize deux cent quarante",
        # Variantes orthographiques et fautes courantes
        "stins",
        "stain",
        "staine",
        "staïns",
        "staiin",
        "stains-sur-seine",
        "sains",
        "stane",
        "stenez",
        "staans",
        "stns",
        "st-ains",
        "st.ains",
        "stainz",
        "staines",
        "s-taine",
        "stainns",
        "stains93",
        "ville stains",
        "stns 93",
        "staens",
        "stans",
        "stainez",
        "s.tains",
        "staints",
        "stainzz",
        "staen",
        "stainez",
        "staings",
        "st.in",
        "st_ains",
        "stn.s",
        "staints93",
        "sta-in",
        "s-tains",
        "commune stains",
        "quartier stains",
        "ville de stains",
        "st1ns",
        "stzns",
        # Nouvelles variantes
        "stainnes",
        "stain sur seine",
        "estains",
        "esstains",
        "93 stains",
        "stains 93240",
        "stains ville",
        "commune de stains",
        "stay",
        "stain 93",
        "stains seine saint denis",
        "stains ssd",
        "stain ssd",
        "stain-sur-seine",
        "city of stains",
        "steins",
        "staains",
        "sténs",
        "93240 cedex",
        "stins 93",
        "stains cedex",
        "mairie de stains",
        "hotel de ville stains",
        "dtains",  # s/d adjacents
        "staind",  # inversion in/nd
        "staibs",  # n/b adjacents
        "srains",  # t/r adjacents
        "staint",  # s/t confusion fin de mot
        "staims",  # n/m adjacents
        "staunss",  # i/u adjacents et double s
        "staihs",  # n/h adjacents
        "sztains",  # s/z adjacents
        "stains2",  # ajout chiffre
        "staons",  # i/o adjacents
        "sstains",  # double s initial
        "stains93240",  # nom + code postal complet
        "93etains",  # début par code département
        "stain93",  # nom partiel + département
        "staims 93",  # erreur lettre + département
        "93ztains",  # code + erreur de frappe
        "stins93",  # abbreviation + département
        "staains",  # double a par erreur
        "tsains",  # inversion premières lettres
        "tains",  # omission du s initial
        "stain s",  # espace mal placé
        "s tains",  # espace mal placé
        "sta1ns",  # i/1 confusion visuelle
        "5tains",  # s/5 confusion visuelle
        "stainz93",  # s/z sonore + département
        "stainsss",  # triple s par insistance
        "stainsse",  # ajout e final silencieux
        "staîns",  # accent circonflexe par erreur
        "estaîns",  # ajout e initial et accent
        "stins9324",  # abréviation + code tronqué
        "sta-ins",  # séparation avec tiret inhabituel
        "sthains",  # ajout h muet
        "steins93",  # variante orthographique + département
        "staines93",  # variante anglicisée + département
        "stannes",  # variante phonétique
        "stannz",  # variante phonétique avec z
        "stayn",  # variante anglicisée
        "93240stns",  # code postal + abréviation
        "staiin",  # double i erreur de frappe
        "estains93",  # e préfixe + département
        "staingz",  # ajout g et z phonétiques
        "stns93240",  # abréviation extrême + code postal
        "stnssd",  # abréviation + ssd (Seine-Saint-Denis)
        "st6ns",  # substitution chiffre pour phonétique
        "staynes",  # orthographe fantaisiste
        "staiines",  # double i erreur
        "staeens",  # substitution ae pour ai
        "9324stains",  # code postal incomplet + ville
        "stain.93",  # avec ponctuation
        "s.t.n.s",  # acronyme ponctué
    ],
    "pierrefitte": [
        # Orthographes standard
        "pierrefitte",
        "pierrefitte sur seine",
        "pierrefitte-sur-seine",
        # Variantes orthographiques et fautes courantes
        "pierrefite",
        "pierfitte",
        "pierre fitte",
        "pierre-fit",
        "pierefitte",
        "pierfet",
        "pierrette",
        "pierreffite",
        "pierre fite",
        "perrefitte",
        "pirefite",
        "pirrefitte",
        "pierrefit",
        "peirrefitte",
        "peirefit",
        "pierre fitte sur seine",
        "pierre fit sur seine",
        "pierrefitte seine",
        "pierrefitte-seine",
        "pierrefitte-sur-saine",
        "pierrefitte su sein",
        "pierre fite seine",
        "pierfit",
        "pierfit-sur-seine",
        "pierrefit-sur-seine",
        "prrfitt",
        "pierfftte",
        "pierrephitte",
        "pierffite",
        "pierrfite",
        "pierfait",
        "pierfitt",
        "pierfit sur seine",
        "pierre-fitte-sur-seine",
        "pierrafitte",
        "pyerrefitte",
        "piere fitte",
        # Codes postaux
        "93380",
        "93 380",
        "93.380",
        "933 80",
        "93-380",
        "93380 pierrefitte",
        # Nombres écrits en toutes lettres
        "quatre-vingt-treize trois cent quatre-vingts",
        "quatre vingt treize trois cent quatre vingts",
        # Nouvelles variantes
        "pierrefitte93",
        "pierrefitte 93",
        "pierrefitte-93",
        "p-fitte",
        "pfitte",
        "p fitte",
        "pierre-fitte",
        "93 pierrefitte",
        "pierrefitte seine saint denis",
        "pierrefitte ssd",
        "pierrefitte s seine",
        "pierrefitte s/seine",
        "pierrefitte/seine",
        "pierrefitte sur s",
        "p sur seine",
        "pierre sur seine",
        "pierrefitte 93380",
        "93380 pierrefitte sur seine",
        "pierre-fitte s/ seine",
        "pfit",
        "pier fit",
        "piehr fit",
        "pier fhit",
        "piehr fhit",
        "piehrr fit",
        "pfitte sur seine",
        "Pierre Fitt",
        "Pierre Fitz",
        "Pire fit",
        "pierre fitte commune",
        "commune de pierrefitte",
        "ville de pierrefitte",
        "mairie de pierrefitte",
        "pierre-fittes",
        "pierrefittte",
        "pierre-sur-seine",
        "pierrefitte cedex",
        "pir-fit",
        "hotel de ville pierrefitte",
        "puerrefitte",  # i/u adjacents
        "pierrefirte",  # t/r adjacents
        "pierrefitte93",  # nom + département
        "piertefitte",  # r/t adjacents
        "pierrecitte",  # f/c adjacents
        "pierrefirre",  # t/r adjacents
        "pierrefitye",  # t/y adjacents
        "pierrefittr",  # e/r adjacents
        "piwrrefitte",  # e/w adjacents
        "pierrefitte9338",  # nom + code postal incomplet
        "93pierrefitte",  # département + nom
        "pierdefitte",  # r/d adjacents
        "puerrefitte93",  # erreur frappe + département
        "pierrefitte s s",  # sur seine abrégé avec espaces
        "pierreditte",  # f/d confusion sonore
        "pierrefitte/s",  # sur abrégé avec slash
        "pierrefit",  # abréviation sans doublement de t et e final
        "pierrefitt",  # omission e final
        "pierrefitte-93380",  # avec code postal et tiret
        "p-fitte93",  # abréviation + département
        "pfitte93380",  # abréviation + code postal
        "pierrefittes",  # ajout s final
        "pyerrefit",  # i/y substitution
        "pierrefite93",  # simplification consonnes + département
        "piierfitte",  # double i erreur frappe
        "pierrefitre",  # t/r confusion
        "pierrefihte",  # t/h adjacents
        "pierrefilte",  # t/l adjacents
        "pîerrefitte",  # ajout accent circonflexe
        "pierrefittee",  # double e final
        "pierefite",  # simplification r et t
        "pierefitte93380",  # simplification r + code postal
        "pierreephitte",  # insertion eh
        "peirrefite",  # inversion ei
        "piereffitte",  # inversion re/ef
        "pierrefitte93ssd",  # nom + code + département abrégé
        "pierrefitesurseine",  # sans espaces ni tirets
        "pierrefite-sseine",  # abréviation avec tiret
        "pierrefitt-ss",  # abréviation extrême
        "pierre-fitte93",  # forme avec tiret + département
        "pierrefit9338",  # abréviation + code tronqué
        "pierrefitte 93 380",  # espaces dans code postal
        "pierrefitte9",  # abréviation extrême
        "pierre-fite93",  # simplification + tiret + département
        "pierrefit-93",  # abréviation + tiret + département
        "pfitte-surseine",  # abréviation début + forme complète fin
        "pierrephite",  # insertion ph pour f
        "pierrefit.93",  # abréviation + point + département
        "p.f.93380",  # initiales ponctuées + code postal
        "pierrefitteseine",  # sans sur
        "pfit93",  # abréviation extrême + département
        "9338pfitte",  # code postal tronqué + abréviation
    ],
    "saint-ouen": [
        # Orthographes standard
        "saint-ouen",
        "saint ouen",
        "st-ouen",
        "st ouen",
        "saint-ouen-sur-seine",
        # Codes postaux
        "93400",
        "93 400",
        "93.400",
        "934 00",
        "93-400",
        "93400 saint ouen",
        # Nombres écrits en toutes lettres
        "quatre-vingt-treize quatre cents",
        "quatre vingt treize quatre cents",
        # Variantes orthographiques et fautes courantes
        "sint ouen",
        "sant ouen",
        "sent ouen",
        "sain ouen",
        "saintowen",
        "saint ouane",
        "saintouen",
        "st-ouan",
        "st-ouane",
        "stouen",
        "snt-ouen",
        "snt ouen",
        "st_ouen",
        "saint_oen",
        "saint-oen",
        "ouen",
        "oüen",
        "saint0uen",
        "saint-ouén",
        "saint-owen",
        "saint-ouan",
        "saint-ouèn",
        "s-ouen",
        "st-ouèn",
        "s.ouen",
        "saint-ouin",
        "saintowène",
        "saint.ouen",
        "sntouen",
        "stouèn",
        "ouène",
        "ouan",
        "commune saint ouen",
        "ville de saint ouen",
        "quartier saint ouen",
        # Nouvelles variantes
        "saint-ouen93",
        "saint ouen 93",
        "st-ouen93",
        "st ouen 93",
        "93 saint ouen",
        "93 st ouen",
        "saintouen sur seine",
        "st-ouen sur seine",
        "saint ouen sur seine",
        "saintouen/seine",
        "st-ouen/seine",
        "stoven",
        "saint owen",
        "st owen",
        "souen",
        "st owen sur seine",
        "saint owen sur seine",
        "saint-ouen ville",
        "st-ouen ville",
        "ouene",
        "saint ouen 93400",
        "st ouen 93400",
        "93400 saint ouen sur seine",
        "93400 st ouen sur seine",
        "sowen",
        "stoen",
        "saint ouen seine saint denis",
        "st ouen seine saint denis",
        "saint ouen ssd",
        "st ouen ssd",
        "mairie de saint ouen",
        "mairie de st ouen",
        "hotel de ville saint ouen",
        "hotel de ville st ouen",
        "saint ouen cedex",
        "st ouen cedex",
        "sainr-ouen",  # t/r adjacents
        "saint-iuen",  # o/i adjacents
        "saint-oien",  # u/i adjacents
        "saint-ourn",  # e/r adjacents
        "saijt-ouen",  # n/j adjacents
        "saintoiem",  # u/i adjacents et n/m adjacents
        "saint-oueb",  # n/b adjacents
        "szint-ouen",  # a/z adjacents
        "saint-ouenn",  # double n erreur
        "saint-ouej",  # n/j adjacents
        "saibt-ouen",  # n/b adjacents
        "saintouen93",  # sans tiret ni espace + département
        "saitn-ouen",  # inversion tn
        "saint-oune",  # inversion un/ne
        "saint-ouin",  # e/i adjacents
        "saintouen93400",  # sans séparateur + code postal
        "st-ouen93400",  # abréviation + code postal
        "saint-ouen 93 400",  # espaces dans code postal
        "93saintouen",  # département + nom sans séparateur
        "saint0uen",  # substitution o/0
        "sain-touen",  # tiret mal placé
        "saintou-en",  # tiret mal placé
        "5t-ouen",  # s/5 confusion visuelle
        "st-0uen",  # o/0 confusion visuelle
        "saint-ouen9",  # ajout chiffre
        "saintouen/s",  # sur abrégé avec slash
        "saint-owen93",  # variante orthographique + département
        "saintouen s/seine",  # abréviation avec slash
        "stoen93",  # abréviation extrême + département
        "sainto93",  # abréviation + début code
        "st-o93",  # abréviation extrême + département
        "saint-ouenssd",  # nom + département abréviation
        "saint-ouen-surseine",  # tout attaché avec tirets
        "s-ouen-93400",  # abréviation + tiret + code postal
        "saintouen-93",  # sans espace + tiret + département
        "snt-ouen93",  # abréviation + département
        "st-ouenseine",  # abréviation + seine sans séparateur
        "saintouen seine",  # sans tiret + espace seine
        "saimt-ouen",  # n/m adjacents
        "saint-ouem",  # n/m adjacents
        "sainttouen",  # double t erreur frappe
        "xaint-ouen",  # s/x adjacents
        "saint-ouën",  # ajout tréma
        "s.ouen.93",  # ponctuation alternative + département
        "st.o.93",  # ponctuation abréviation + département
        "saint-ouen-sur-s",  # sur-seine abrégé
        "st-ouen-s-s",  # abréviation extrême
        "stoen",  # abréviation sans trait d'union
        "saintouen-s/s",  # abréviation avec slash
        "st-ouen9340",  # abréviation + code postal tronqué
        "saint-ouen-93-400",  # tirets partout
    ],
    "épinay-sur-seine": [
        # Orthographes standard
        "epinay",
        "épinay",
        "épiniay",
        "ipinay",
        "ipiniay",
        "epinay-sur-seine",
        "épinay-sur-seine",
        # Codes postaux
        "93800",
        "93 800",
        "93.800",
        "938 00",
        "93-800",
        "93800 epinay",
        # Nombres écrits en toutes lettres
        "quatre-vingt-treize huit cents",
        "quatre vingt treize huit cents",
        # Variantes orthographiques et fautes courantes
        "epinaï",
        "epiny",
        "epinai",
        "epiné",
        "epinaye",
        "epinae",
        "epinaye-sur-seine",
        "epinay sur seine",
        "epinay/Seine",
        "epinaÿ",
        "epinnay",
        "epinny",
        "epny",
        "epinaiy",
        "epinau",
        "epinnaï",
        "epinhe",
        "epenaï",
        "epnay",
        "e.pinay",
        "epin_ai",
        "epin.ai",
        "epin",
        "épiné",
        "epinai-sur-seine",
        "epinnaye",
        "épinaÿ-sur-seine",
        "epinay-sur-senne",
        "epinay-sur-scène",
        "epynay",
        "epinné",
        "epigny",
        "epinets",
        "commune epinay",
        "ville epinay",
        "quartier epinay",
        # Nouvelles variantes
        "epinay93",
        "épinay93",
        "epinay 93",
        "épinay 93",
        "93 epinay",
        "93 épinay",
        "epinay/seine",
        "épinay/seine",
        "epinay s/seine",
        "épinay s/seine",
        "epinay s seine",
        "épinay s seine",
        "epinay seine",
        "épinay seine",
        "epinay-s-seine",
        "épinay-s-seine",
        "93800 epinay sur seine",
        "93800 épinay sur seine",
        "epinay 93800",
        "épinay 93800",
        "epinay-seine",
        "épinay-seine",
        "epinay sur s",
        "épinay sur s",
        "epinay-s",
        "épinay-s",
        "epinay seine saint denis",
        "épinay seine saint denis",
        "epinay ssd",
        "épinay ssd",
        "epine",
        "épine",
        "epinaysurseine",
        "épinaysurseine",
        "commune de epinay",
        "commune d'epinay",
        "commune de épinay",
        "commune d'épinay",
        "ville de epinay",
        "ville d'epinay",
        "ville de épinay",
        "ville d'épinay",
        "mairie de epinay",
        "mairie d'epinay",
        "mairie de épinay",
        "mairie d'épinay",
        "epinay cedex",
        "épinay cedex",
        "hotel de ville epinay",
        "hotel de ville épinay",
        "epunay",  # i/u adjacents
        "epinzy",  # a/z adjacents
        "epinqy",  # a/q adjacents
        "epinsy",  # a/s adjacents
        "épinzy",  # a/z adjacents avec accent
        "epitay",  # n/t adjacents
        "épinat",  # y/t adjacents
        "epinay93",  # nom + département
        "épinay93800",  # nom accentué + code postal
        "ep1nay",  # i/1 confusion visuelle
        "ép1nay",  # i/1 confusion visuelle avec accent
        "epimay",  # n/m adjacents
        "epinaysurseine93",  # tout attaché + département
        "epinaysurseine",  # tout attaché sans tirets
        "épinaysurseine",  # tout attaché avec accent
        "epinay-s-s",  # abréviation extrême
        "epinay-s/s",  # abréviation avec slash
        "epinzy-sur-seine",  # a/z adjacents + complet
        "93800epinay",  # code postal + nom sans espace
        "938epinay",  # code postal tronqué + nom
        "epinqy-sur-seine",  # a/q adjacents + complet
        "3pinay",  # e/3 confusion visuelle
        "épiney",  # a/e adjacents
        "épinnay",  # double n erreur
        "épinai-sur-seine",  # variante orthographique
        "epinaysaine",  # erreur seine/saine
        "epinay/seine",  # avec slash
        "epiné/seine",  # variante orthographique + slash
        "epinay-seime",  # n/m adjacents
        "epinay-siene",  # inversion ie
        "epinaysur-seine",  # attaché partiel
        "èpinay",  # accent grave erreur
        "êpinay",  # accent circonflexe erreur
        "epinau",  # y/u erreur phonétique
        "épinau",  # y/u erreur phonétique avec accent
        "epinai93",  # variante orthographique + département
        "epinays",  # ajout s final
        "3p1nay",  # e/3 et i/1 confusion visuelle
        "épinay-s-seine",  # abréviation partielle
        "epynaie",  # variation orthographique créative
        "épynaie",  # variation orthographique créative avec accent
        "epynai-sur-seine",  # variation orthographique + complet
        "epynay",  # i/y substitution
        "epinayssd",  # nom + département abrégé
        "épiné93",  # variante + département
        "epiné-sur-seine",  # variante orthographique
        "épinai-s-s",  # variante + abréviation
        "epinay.93",  # nom + point + département
        "epinay.sur.seine",  # ponctuation alternative
        "e.s.s93",  # initiales + département
        "epinayseine",  # omission du sur
    ],
    "villetaneuse": [
        # Orthographes standard
        "villetaneuse",
        "ville tanneuse",
        "ville-tanneuse",
        "ville taneuse",
        # Codes postaux
        "93430",
        "93 430",
        "93.430",
        "934 30",
        "93-430",
        "93430 villetaneuse",
        # Nombres écrits en toutes lettres
        "quatre-vingt-treize quatre cent trente",
        "quatre vingt treize quatre cent trente",
        # Variantes orthographiques et fautes courantes
        "viltaneuse",
        "villetaneus",
        "villetanuse",
        "villetneuse",
        "villetanus",
        "villetaneze",
        "villetaneuz",
        "villetaneuse93",
        "villetaneusse",
        "villetanusz",
        "viltneuse",
        "viltenause",
        "villetaineuse",
        "villetaneusé",
        "villetannes",
        "villetaneause",
        "villetaneusze",
        "viltanuse",
        "villetanése",
        "villetnaeuse",
        "vltaneuse",
        "vilta-neuse",
        "v.neuse",
        "villetanues",
        "ville-neuse",
        "vltneuse",
        "vltneuze",
        "vltaneuse93",
        "villetneuze",
        "vilta_neuse",
        "commune villetaneuse",
        "quartier villetaneuse",
        "ville de villetaneuse",
        "villetann",
        "vltaneus",
        # Nouvelles variantes
        "vtaneuse",
        "v taneuse",
        "ville-t",
        "v-taneuse",
        "villetanse",
        "villetaneuse 93",
        "villetaneuse-93",
        "93 villetaneuse",
        "villetaneuse 93430",
        "93430 villetaneuse",
        "villetaneuze",
        "ville-taneuse",
        "ville.taneuse",
        "villet",
        "villetaneuze",
        "villetanuese",
        "villetaneuse ssd",
        "villetaneuse seine saint denis",
        "vile taneuse",
        "villetaneuse commune",
        "commune de villetaneuse",
        "vill-taneuse",
        "villataneuse",
        "villa taneuse",
        "villetaneuse cedex",
        "vt",
        "mairie de villetaneuse",
        "hotel de ville villetaneuse",
        "villeraneuse",  # t/r adjacents
        "villetabeuse",  # n/b adjacents
        "villetameuse",  # n/m adjacents
        "villetaneise",  # u/i adjacents
        "villetaneude",  # s/d adjacents
        "villetaneuxe",  # s/x adjacents
        "villetaneuze",  # s/z adjacents
        "villetaneuss",  # e/s adjacents
        "villrtaneuse",  # e/r adjacents
        "villetanzuse",  # e/z adjacents
        "villetaneyse",  # u/y adjacents
        "villetane7se",  # u/7 confusion visuelle
        "v1lletaneuse",  # i/1 confusion visuelle
        "villetaneu5e",  # s/5 confusion visuelle
        "villetaneuse93",  # nom + département
        "villetaneuse93430",  # nom + code postal
        "93villetaneuse",  # département + nom
        "villetaneuze93",  # variante + département
        "villetaneus93",  # omission e final + département
        "villetaneus-93430",  # omission e final + tiret + code
        "villetaneusee",  # double e erreur
        "villetanneusse",  # double n et double s erreur
        "villletaneuse",  # triple l erreur
        "viletaneuse",  # omission l
        "vilettaneuse",  # inversion ll/le
        "villetaneusessd",  # nom + département abrégé
        "villetaneusess",  # confusion finale
        "villetaneus.93",  # omission e final + point + département
        "villetaneuze.93",  # variante + point + département
        "villetaneuse-93",  # nom + tiret + département
        "villetaneuse 93 430",  # espaces dans code postal
        "villetaneuz",  # omission e final + z phonétique
        "villetaneusse",  # ajout s phonétique
        "93430vtaneuse",  # code postal + abréviation
        "vtnse",  # abréviation extrême
        "viletan",  # abréviation
        "villetanssd",  # abréviation + département abrégé
        "villetaneuse9",  # ajout chiffre
        "villetameuse93",  # n/m adjacents + département
        "villetaneusd",  # e/d confusion
        "v-taneuse93",  # abréviation avec tiret + département
        "v.t.93430",  # initiales + code postal
        "v.taneuse",  # abréviation avec point
        "villetaneuse seine saint denis",  # nom complet département
        "villetaneuse 93ssd",  # mélange codes
        "villtaneuse",  # omission e
        "villtanuse",  # omissions multiples
        "vil-taneuse",  # abréviation avec tiret
        "villetaneuze93430",  # variante phonétique + code postal
        "villetaneuse9343",  # code postal tronqué
        "villtaneuse93",  # omission e + département
    ],
    "île-saint-denis": [
        # Orthographes standard
        "ile-saint-denis",
        "île-saint-denis",
        "ile saint denis",
        "île saint denis",
        # Codes postaux
        "93450",
        "93 450",
        "93.450",
        "934 50",
        "93-450",
        "93450 ile saint denis",
        # Nombres écrits en toutes lettres
        "quatre-vingt-treize quatre cent cinquante",
        "quatre vingt treize quatre cent cinquante",
        # Variantes orthographiques et fautes courantes
        "ile st denis",
        "isle saint denis",
        "île st denis",
        "isle-st-denis",
        "ile de saint denis",
        "isle de saint denis",
        "ile_saint_denis",
        "île_saint_denis",
        "ilestdenis",
        "ilestdénis",
        "île-st-denis",
        "ile-st-denis",
        "île_saintdenis",
        "island saint denis",
        "ile de st denis",
        "île de st denis",
        "i.s.denis",
        "isd",
        "i s d",
        "île denis",
        "isle denis",
        "île saint-dénis",
        "île-st.denis",
        "ile st.denis",
        "île sd",
        "île93",
        "île-seine93",
        "denis île",
        "stdenis-île",
        "commune île-saint-denis",
        "ville île st denis",
        "quartier île st denis",
        # Nouvelles variantes
        "lile saint denis",
        "l'ile saint denis",
        "l'île saint denis",
        "l'isle saint denis",
        "lile-saint-denis",
        "l'ile-saint-denis",
        "l'île-saint-denis",
        "ilesaintdenis",
        "îlesaintdenis",
        "93 ile saint denis",
        "93 île saint denis",
        "ile saint denis 93",
        "île saint denis 93",
        "ile-st-d",
        "île-st-d",
        "isd93",
        "île-saint-denis93",
        "ile-saint-denis93",
        "i-s-d",
        "i.st.d",
        "isle st denis",
        "ile saint denis 93450",
        "île saint denis 93450",
        "93450 ile saint denis",
        "93450 île saint denis",
        "île saint denis ssd",
        "ile saint denis ssd",
        "île saint denis seine saint denis",
        "ile saint denis seine saint denis",
        "isd ssd",
        "ile st denis 93",
        "île st denis 93",
        "l'ile st denis",
        "l'île st denis",
        "commune de l'ile saint denis",
        "commune de l'île saint denis",
        "ville de l'ile saint denis",
        "ville de l'île saint denis",
        "mairie de l'ile saint denis",
        "mairie de l'île saint denis",
        "ile st denis cedex",
        "île st denis cedex",
        "hotel de ville ile saint denis",
        "hotel de ville île saint denis",
        "ile-sainr-denis",  # t/r adjacents
        "ile-saint-demis",  # n/m adjacents
        "ile-sainr-demis",  # erreurs multiples t/r et n/m
        "ile-saibt-denis",  # n/b adjacents
        "ile-saint-denia",  # s/a adjacents
        "ile-saint-deniz",  # s/z substitution phonétique
        "ile-saint-deni5",  # s/5 confusion visuelle
        "ile-sa1nt-denis",  # i/1 confusion visuelle
        "ile-saint-deni",  # omission s final
        "ile-saint-dennnis",  # triple n erreur
        "ile-sain-denis",  # omission t
        "ile-ssaint-denis",  # double s initial
        "ile-saint-ddenis",  # double d erreur
        "ile-saintdennis",  # sans tiret + double n
        "ilesaintdenis93",  # tout attaché + département
        "ilesaintdenis93450",  # tout attaché + code postal
        "93ilesaintdenis",  # département + tout attaché
        "isd93450",  # acronyme + code postal
        "i-s-d93",  # acronyme avec tirets + département
        "ile.saint.denis",  # ponctuation alternative
        "ile.st.denis",  # abréviation + ponctuation alternative
        "ile-st-denis93",  # abréviation + département
        "ile-stdenis",  # abréviation sans second tiret
        "ile saintdenis",  # sans second tiret
        "ile-saintdenis93",  # sans second tiret + département
        "isldenis",  # contraction + erreur sur isle
        "îsldenis",  # contraction avec accent
        "isle denis",  # variante orthographique ancienne
        "îsle st denis",  # variante ancienne avec accent et abréviation
        "île de st denis",  # formulation avec de
        "ile st denis 93",  # abréviation + espace + département
        "isle de saint denis",  # formulation ancienne avec de
        "ile s denis",  # abréviation extrême
        "ile-snt-denis",  # abréviation saint
        "ile std",  # abréviation extrême
        "ilsd",  # acronyme alternatif
        "il-st-ds",  # abréviation extrême avec tirets
        "iles-d",  # abréviation extrême
        "ilesd93",  # abréviation + département
        "ile93",  # abréviation extrême + département
        "isle93",  # variante ancienne + département
        "ill st denis",  # double l erreur
        "ile sd 93450",  # abréviation + espace + code postal
        "ile-st-d93450",  # abréviation + département + code postal
        "ilesdssd",  # abréviation + département abrégé
        "ile-st-denis seine",  # abréviation + seine seul
        "ile st denis sseine",  # abréviation + seine sans tiret
        "ile-s-d-93450",  # abréviation extrême avec tirets + code
        "ilesaintdenis/93",  # tout attaché + slash + département
        "isle-saint-denis93",  # variante ancienne + département
        "l'ile-s-d",  # avec apostrophe + abréviation extrême
    ],
    "aubervilliers": [
        # Orthographes standard
        "aubervilliers",
        # Codes postaux
        "93300",
        "93 300",
        "93.300",
        "933 00",
        "93-300",
        "93300 aubervilliers",
        # Nombres écrits en toutes lettres
        "quatre-vingt-treize trois cents",
        "quatre vingt treize trois cents",
        # Variantes orthographiques et fautes courantes
        "auberville",
        "aubervilier",
        "auberviliers",
        "aubervillier",
        "aubervilleirs",
        "auber",
        "aubrvilliers",
        "auberv",
        "aubervilliere",
        "aubervillé",
        "aubrville",
        "aubrviller",
        "aubervilles",
        "aubr",
        "aubervilles93",
        "aubrvile",
        "aubervillières",
        "aubvervilliers",
        "aubervillies",
        "aubrvilles",
        "aubervlliers",
        "auber-villiers",
        "auber_villiers",
        "aub-villiers",
        "aubervil",
        "aubrvilez",
        "aubervillieur",
        "aubervillez",
        "aubr-ville",
        "aubervillièrs",
        "auberviilers",
        "aubrvllrs",
        "aubrvillrs",
        "aubrvillr",
        "aubervilliére",
        "aubrvlrs",
        "aubervillee",
        "commune aubervilliers",
        "ville aubervilliers",
        "quartier aubervilliers",
        # Nouvelles variantes
        "aubervilier",
        "aubervillers",
        "aubervillié",
        "auberviliez",
        "aubervilliés",
        "aubervilié",
        "auberv.",
        "a.villiers",
        "avilliers",
        "avillier",
        "aubervil",
        "aubervilliers 93",
        "aubervilliers-93",
        "aubervilliers93",
        "93 aubervilliers",
        "aubervilliers 93300",
        "93300 aubervilliers",
        "aub",
        "aubville",
        "ville d'aubervilliers",
        "commune d'aubervilliers",
        "aubervilliers ssd",
        "aubervilliers seine saint denis",
        "auber 93",
        "auber 93300",
        "aubervilliers cedex",
        "commune de aubervilliers",
        "mairie de aubervilliers",
        "mairie d'aubervilliers",
        "auber ville",
        "auber-ville",
        "obrville",
        "hotel de ville aubervilliers",
        "zubervilliers",  # a/z adjacents
        "qubervilliers",  # a/q adjacents
        "aubervilluers",  # i/u adjacents
        "aubervilkers",  # l/k adjacents
        "aubervillirrs",  # e/r adjacents
        "aubervilliees",  # r/e adjacents
        "aubervillierd",  # s/d adjacents
        "aubervilliere",  # s/e adjacents
        "aubervilliees",  # double e erreur
        "aubeevilliers",  # double e erreur
        "aubervillliers",  # triple l erreur
        "aubervvilliers",  # double v erreur
        "auberviliiers",  # omission l + double i
        "aubervilliers93",  # nom + département
        "aubervilliers93300",  # nom + code postal
        "93aubervilliers",  # département + nom
        "93300aubervilliers",  # code postal + nom
        "aubervillierz",  # s/z substitution phonétique
        "aubervillier5",  # s/5 confusion visuelle
        "auberv1lliers",  # i/1 confusion visuelle
        "aubervi11iers",  # l/1 confusion visuelle
        "aubervillier",  # omission s final
        "aubervillie",  # omission rs final
        "aubrvilliers",  # omission e
        "auberviliés",  # variante phonétique
        "aubervilers",  # omission li
        "aub.vill",  # abréviation avec point
        "a-villiers",  # abréviation avec tiret
        "aub-vill93",  # abréviation avec tiret + département
        "aubervilier-93",  # simplifié + tiret + département
        "aubervilliers-ssd",  # nom + tiret + département abrégé
        "aubervillers93300",  # simplifié + code postal
        "aubervillierseine",  # nom + seine sans séparateur
        "aubervil93",  # abréviation + département
        "aubersvilliers",  # insertion s erreur
        "aubervilliers 93 300",  # espaces dans code postal
        "auberv-93",  # abréviation extrême + département
        "a.v.93",  # initiales + département
        "aubervil.93",  # abréviation + point + département
        "auberville93",  # variante + département
        "aubervilier93300",  # simplifié + code postal
        "aubervilliers9",  # ajout chiffre
        "aubervillierrsz",  # double r + z final
        "aubervilliersz",  # ajout z final
        "auberviliers-93300",  # simplifié + tiret + code postal
        "auvervil",  # b/v substitution + abréviation
        "oberviliers",  # a/o substitution
        "auberviliers-ssd",  # simplifié + département abrégé
        "aubervillier.93",  # omission s + point + département
        "aubervilliers/93",  # nom + slash + département
        "auber93",  # abréviation extrême + département
    ],
    "la-courneuve": [
        # Orthographes standard
        "la courneuve",
        "la-courneuve",
        # Codes postaux
        "93120",
        "93 120",
        "93.120",
        "931 20",
        "93-120",
        "93120 la courneuve",
        # Nombres écrits en toutes lettres
        "quatre-vingt-treize cent vingt",
        "quatre vingt treize cent vingt",
        # Variantes orthographiques et fautes courantes
        "courneuve",
        "lacourneuve",
        "la-courneu",
        "la courneu",
        "la-courneuv",
        "lacourneu",
        "lacourneuv",
        "la corneuve",
        "la cournev",
        "la corneu",
        "l-courneuve",
        "courneu",
        "courneuv",
        "courneuve93",
        "la courneuve 93",
        "la cournve",
        "la.courneuve",
        "l.courneuve",
        "la_courneuve",
        "la courneuvez",
        "la corneuv",
        "lacorneuve",
        "courneuve ville",
        "commune la courneuve",
        "quartier la courneuve",
        "lacour_neuve",
        "la-cour.nueve",
        "la courneuvez",
        "lacournev",
        "la curneve",
        "la courneuive",
        "la courneuvve",
        "la couneuve",
        "la cou-neuve",
        "la cour-neuve",
        # Nouvelles variantes
        "lacourneuve93",
        "la-courneuve93",
        "la courneuve93",
        "la courneuve-93",
        "la courneuve 93120",
        "la-courneuve 93120",
        "93 la courneuve",
        "93120 la-courneuve",
        "lcourneuve",
        "l-c-n",
        "l.c.n",
        "lcn",
        "la courneuve seine saint denis",
        "la courneuve ssd",
        "la-courneuve ssd",
        "la c",
        "la courneuve commune",
        "la-courneuve commune",
        "commune de la courneuve",
        "ville de la courneuve",
        "la kurneuve",
        "la kourneuve",
        "la cournoeuv",
        "la courneuve cedex",
        "la-courneuve cedex",
        "mairie de la courneuve",
        "hotel de ville la courneuve",
        "la ciurneuve",  # o/i adjacents
        "la courbeuve",  # n/b adjacents
        "la courneyve",  # u/y adjacents
        "la cournruve",  # e/r adjacents
        "la courneufe",  # v/f adjacents
        "la courneuvr",  # e/r adjacents
        "la courneuced",  # v/c adjacents et e/d adjacents
        "la courmeuve",  # n/m adjacents
        "la courneuce",  # v/c adjacents
        "la courneuvee",  # double e erreur
        "la courneuvve",  # double v erreur
        "la ccourneuve",  # double c erreur
        "la cournneuve",  # double n erreur
        "la courneuve93",  # nom + département
        "lacourneuve93",  # sans espace + département
        "la-courneuve93",  # avec tiret + département
        "la courneuve93120",  # nom + code postal
        "lacourneuve93120",  # sans espace + code postal
        "la-courneuve93120",  # avec tiret + code postal
        "93lacourneuve",  # département + nom sans espace
        "93120lacourneuve",  # code postal + nom sans espace
        "la courneuv",  # omission e final
        "la corneuve",  # omission u
        "la courneuvz",  # e/z substitution phonétique
        "la courneuv3",  # e/3 confusion visuelle
        "la c0urneuve",  # o/0 confusion visuelle
        "la courneueve",  # insertion e erreur
        "la cournuve",  # omission e médian
        "la courneuve-ssd",  # nom + département abrégé
        "la courneuve-93",  # nom + tiret + département
        "lcnve",  # abréviation extrême
        "la cnve93",  # abréviation + département
        "la courneuv.93",  # abréviation + point + département
        "la courneuve 93 120",  # espaces dans code postal
        "la coroneuv",  # inversion lettres + omission finale
        "la cournoeuve",  # insertion o erreur
        "la courneuve9",  # ajout chiffre
        "l-courneuve",  # abréviation article + tiret
        "la courneuve-seine",  # nom + seine sans sur
        "la courneuve seine saint denis",  # nom + département complet
        "la courneuve ssd",  # nom + département abrégé
        "la-courne",  # abréviation extrême
        "la.crn.93",  # abréviation avec ponctuation + département
        "la-c-93120",  # abréviation extrême + code postal
        "lacourneuvessd",  # tout attaché + département abrégé
        "la cournneuv",  # double n + omission finale
        "la courneuveseine",  # tout attaché avec seine
        "lacourneuve seine",  # sans espace début + espace seine
        "la courneuf",  # v/f substitution phonétique
        "la-courneuf",  # avec tiret + v/f substitution
        "la courneuve/93",  # nom + slash + département
        "la-crn93",  # abréviation extrême + département
    ],
}


# Fonction utilitaire pour rechercher une ville à partir d'une chaîne de texte
def find_city_from_text(text):
    """
    Recherche une ville correspondante à partir d'un texte.

    Args:
        text (str): Texte à analyser pour trouver une ville

    Returns:
        str or None: Nom normalisé de la ville trouvée ou None si aucune correspondance
    """
    if not text:
        return None

    text_lower = text.lower().strip()

    # Vérifier les codes postaux
    postal_code_mapping = {
        "93200": "saint-denis",
        "93240": "stains",
        "93380": "pierrefitte",
        "93400": "saint-ouen",
        "93800": "épinay-sur-seine",
        "93430": "villetaneuse",
        "93450": "île-saint-denis",
        "93300": "aubervilliers",
        "93120": "la-courneuve",
    }

    # Recherche de code postal dans le texte
    import re

    postal_code_match = re.search(r"93\s*[0-9]{3}", text_lower)
    if postal_code_match:
        postal_code = postal_code_match.group().replace(" ", "")
        if postal_code in postal_code_mapping:
            return postal_code_mapping[postal_code]

    # Recherche par variantes
    for city_key, variants in CITY_VARIANTS.items():
        for variant in variants:
            if variant in text_lower or variant.replace("-", " ") in text_lower:
                return city_key

    return None


# Fonction pour normaliser le nom d'une ville
def normalize_city_name(city_name):
    """
    Normalise le nom d'une ville en le convertissant en clé standard.

    Args:
        city_name (str): Nom de ville à normaliser

    Returns:
        str or None: Clé normalisée de la ville ou None si non reconnue
    """
    if not city_name:
        return None

    city_lower = city_name.lower().strip()

    # Vérifier si c'est déjà une clé
    if city_lower in CITY_VARIANTS:
        return city_lower

    # Chercher dans les variantes
    for city_key, variants in CITY_VARIANTS.items():
        if city_lower in variants or city_lower.replace("-", " ") in variants:
            return city_key

    # Essayer de trouver dans le texte complet
    return find_city_from_text(city_lower)
