from enum import Enum


class EnumCommand(Enum):
    HELP = "help"

    INFOS = "infos"
    RANK = "grade"
    SIGNATURE = "signature"
    SERIAL = "matricule"

    ARREST = "arrestation"
    SEIZURE = "saisie"
    INCIDENT = "incident"
    CORPSE = "cadavre"
    FIRE = "tir"

    LAW = "loi"


class Command:

    async def process(self, ronanda):
        await ronanda.answer("Cette commande n'est pas encore implémentée.")
