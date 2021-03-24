import os
import logging
from dotenv import load_dotenv

from commands.command import EnumCommand

logging.basicConfig(level=logging.INFO)


class Config:

    COMMAND_PREFIX = "!"

    forms = {
        EnumCommand.SEIZURE: {
            "template_filepath": "forms/saisie",
            "template_args": [
                "casier", "lieu", "categories", "types", "quantites", "suspect", "contexte", "photo"
            ],
            "command_example": "\"101\" \"Legion Square\" \"Drogues, armes\" \"Fusil d'assaut AK-47\" \"1\" \"Karim Cassidy\" \"Fouille après arrestation\" \"EL/XY/XY + lien screen\"",
            "instructions": [
                {
                    "name": "A soumettre ici",
                    "value": "https://pd.gta.world/posting.php?mode=reply&f=17&t=34"
                }
            ]
        },

        EnumCommand.CORPSE: {
            "template_filepath": "forms/cadavre",
            "template_args": [
                "lieu", "contexte", "victime", "causes", "temoins", "inspecteur", "medecin", "preuves"
            ],
            "command_example": "\"Legion Square\" \"Patrouille standard\" \"Klark Krause\" \"Non identifiées\" \"Aucun\" \"Inspecteur III Alfredo Bigo\" \"Dr Docteur\" \"EL/XY/XY\"",
            "instructions": [
                {
                    "name": "A soumettre ici",
                    "value": "https://pd.gta.world/posting.php?mode=reply&f=17&t=350"
                }
            ]
        },

        EnumCommand.FIRE: {
            "template_filepath": "forms/tir",
            "template_args": [
                "lieu", "arme", "cartouches", "douilles", "inspecteur", "contexte", "victime", "preuves"
            ],
            "command_example": "\"Legion Square\" \"Pistolet\" \"6\" \"0\" \"Inspecteur II Heather Conower\" \"Fusillade\" \"Sosmu Sabanic, décédé\" \"EL/XY/XY\"",
            "instructions": [
                {
                    "name": "A soumettre ici",
                    "value": "https://pd.gta.world/posting.php?mode=reply&f=17&t=33"
                }
            ]
        },

        EnumCommand.INCIDENT: {
            "template_filepath": "forms/incident",
            "template_args": [
                "lieu", "contexte", "preuves"
            ],
            "command_example": "\"Legion Square\" \"Collision civile lors d'une poursuite\" \"EL/XY/XY\"",
            "instructions": [
                {
                    "name": "A soumettre ici",
                    "value": "https://pd.gta.world/posting.php?mode=reply&f=17&t=32"
                }
            ]
        },

        EnumCommand.ARREST: {
            "template_filepath": "forms/arrestation",
            "template_args": [
                "lieu", "suspect", "description", "dashcam", "agents", "preuves", "plaidoirie"
            ],
            "command_example": "\"Legion Square\" \"Karim Cassidy\" \"description\" \"description dashcam\" \"Inspecteur Javier Cueto, Officier Edwin Park\" \"EL/XY/XY\" \"Non-Coupable avec commis d'office\"",
            "instructions": [
                {
                    "name": "A mettre dans le MDC ici (Actions > Créer un casier > Type = Rapport d'arrestation)",
                    "value": "https://mdc-fr.gta.world/record/{suspect_name_url}"
                }, {
                    "name": "MEA **Copiez le texte que vous avez collé dans le MDC, ici**",
                    "value": "https://forum-fr.gta.world/index.php?/forum/201-demandes-de-mise-en-accusation/&do=add"
                }, {
                    "name": "Titre de la MEA",
                    "value": "```Demande de mise en accusation - {suspect_name}```"
                }
            ]
        },
    }

    def __init__(self):
        load_dotenv()

        self.TOKEN = os.getenv('DISCORD_TOKEN')
        self.MYSQL_HOST = os.getenv('MYSQL_HOST')
        self.MYSQL_USER = os.getenv('MYSQL_USER')
        self.MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
        self.MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
