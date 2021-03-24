import logging

logging.basicConfig(level=logging.INFO)


class Config:

    TOKEN = "ODE4MTU1ODE2Mzg5NDQzNjE0.YET8-w.ES8B-KZ2SsaNKKSrbAVo2kdS6TM"

    forms = {
        "saisie": {
            "template_filepath": "gtaw/saisie",
            "template_args": [
                "casier", "lieu", "categories", "types", "quantites", "suspect", "contexte"
            ],
            "template_optional_args": [
                {"photo": "EL/XX/XX"}
            ],
            "template_link": "https://pd.gta.world/posting.php?mode=reply&f=17&t=34",
            "command_example": "\"101\" \"Legion Square\" \"Drogues, armes\" \"Fusil d'assaut AK-47\" \"1\" \"Karim Cassidy\" \"Fouille après arrestation\" photo=\"EL/XY/XY + lien screen\"",
        },

        "cadavre": {
            "template_filepath": "gtaw/cadavre",
            "template_args": [
                "lieu", "contexte", "victime", "causes", "temoins", "inspecteur", "medecin",
            ],
            "template_optional_args": [
                {"preuves": "EL/XX/XX"}
            ],
            "template_link": "https://pd.gta.world/posting.php?mode=reply&f=17&t=350",
            "command_example": "\"Legion Square\" \"Patrouille standard\" \"Klark Krause\" \"Non identifiées\" \"Aucun\" \"Inspecteur III Alfredo Bigo\" \"Dr Docteur\" preuves=\"EL/XY/XY\"",
        },

        "tir": {
            "template_filepath": "gtaw/tir",
            "template_args": [
                "lieu", "arme", "cartouches", "douilles", "inspecteur", "contexte", "victime",
            ],
            "template_optional_args": [
                {"preuves": "EL/XX/XX"}
            ],
            "template_link": "https://pd.gta.world/posting.php?mode=reply&f=17&t=33",
            "command_example": "\"Legion Square\" \"Pistolet\" \"6\" \"0\" \"Inspecteur II Heather Conower\" \"Fusillade\" \"Sosmu Sabanic, décédé\" preuves=\"EL/XY/XY\"",
        },

        "incident": {
            "template_filepath": "gtaw/incident",
            "template_args": [
                "lieu", "contexte",
            ],
            "template_optional_args": [
                {"preuves": "EL/XX/XX"}
            ],
            "template_link": "https://pd.gta.world/posting.php?mode=reply&f=17&t=32",
            "command_example": "\"Legion Square\" \"Collision civile lors d'une poursuite\" preuves=\"EL/XY/XY\"",
        },

        "arrestation": {
            "template_filepath": "gtaw/arrestation",
            "template_args": [
                "lieu", "suspect", "description", "dashcam", "agents"
            ],
            "template_optional_args": [
                {"preuves": "EL/XX/XX"},
                {"plaidoirie": "Coupable sans commis d'office"}
            ],
            "template_link": "https://forum-fr.gta.world/index.php?/forum/201-demandes-de-mise-en-accusation/&do=add",
            "command_example": "\"Legion Square\" \"Karim Cassidy\" \"description\" \"description dashcam\" \"Inspecteur Javier Cueto, Officier Edwin Park\" preuves=\"EL/XY/XY\" plaidoirie=\"Non-Coupable avec commis d'office\"",
        },
    }
