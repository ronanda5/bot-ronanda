from commands.command_arrestation import CommandArrestation
from commands.command_cadavre import CommandCadavre
from commands.command_grade import CommandGrade
from commands.command_incident import CommandIncident
from commands.command_law import CommandLaw
from commands.command_infos import CommandInfos
from commands.command_matricule import CommandMatricule
from commands.command_help import CommandHelp
from commands.command_saisie import CommandSaisie
from commands.command_signature import CommandSignature
from commands.command_tir import CommandTir
from commands.command import EnumCommand


class Ronanda:

    commands = {
        EnumCommand.HELP: CommandHelp(),

        EnumCommand.INFOS: CommandInfos(),
        EnumCommand.SIGNATURE: CommandSignature(),
        EnumCommand.RANK: CommandGrade(),
        EnumCommand.SERIAL: CommandMatricule(),

        EnumCommand.ARREST: CommandArrestation(),
        EnumCommand.SEIZURE: CommandSaisie(),
        EnumCommand.CORPSE: CommandCadavre(),
        EnumCommand.FIRE: CommandTir(),
        EnumCommand.INCIDENT: CommandIncident(),

        EnumCommand.LAW: CommandLaw(),
    }

    def __init__(self, message, db):
        self.message = message
        self.db = db

    async def answer(self, text, embed=None):
        await self.message.channel.send("> {author} {text}".format(author=self.message.author.mention, text=text),
                                        embed=embed)

    def load_or_create_user(self):
        tag = self.message.author
        user = self.db.get_user(tag)
        if user is None:
            self.db.create_user(tag=tag)
            user = self.db.get_user(tag=tag)
        character_name = self.message.author.nick
        character = self.db.get_character(name=character_name)
        if character is None:
            self.db.create_character(name=character_name, user_id=user['id'])
        else:
            if character['user_id'] != user['id']:
                raise ValueError("Le personnage `{}` ne vous appartient pas.".format(character['name']))
        return user

    async def check_signature(self, officer):
        if self.get_signature(officer) == officer:
            await self.answer(
                "Par défaut, vos formulaires sont signés : `{}`\n"
                "`!signature` pour modifier la signature de vos formulaires :person_tipping_hand:".format(officer))

    def get_signature(self, officer):
        character = self.db.get_character(name=officer)
        if character.get('signature') is None:
            del character['signature']
        return character.get('signature', officer)

    def get_grade(self, officer):
        character = self.db.get_character(name=officer)
        if character.get('grade') is None:
            del character['grade']
        return character.get('grade', 'Aucun')

    def get_matricule(self, officer):
        character = self.db.get_character(name=officer)
        if character.get('matricule') is None:
            del character['matricule']
        return character.get('matricule', '#')

    async def increment_user_stats(self, user_tag):
        stats = self.db.get_user(tag=user_tag)['stats'] + 1
        self.db.update_user(tag=user_tag, stats=stats)

    async def help(self):
        await self.commands[EnumCommand.HELP].process(self)

    async def process(self, command=None):
        if self.message.author.nick is None:
            await self.answer("Changez votre pseudo discord local pour mettre le `Prénom Nom` de votre personnage.")
            return

        try:
            self.load_or_create_user()
        except ValueError as e:
            await self.answer(e)
            return

        try:
            enum_command = EnumCommand(command)
        except ValueError:
            await self.answer("La commande *%s* n'existe pas. Mentionnez moi pour obtenir de l'aide." % command)
            return

        await self.commands[enum_command].process(self)
