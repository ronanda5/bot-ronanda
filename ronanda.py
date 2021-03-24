from command_arrestation import CommandArrestation
from command_article import CommandArticle
from command_assignation import CommandAssignation
from command_cadavre import CommandCadavre
from command_caution import CommandCaution
from command_charge import CommandCharge
from command_ddf import CommandDDF
from command_fourriere import CommandFourriere
from command_grade import CommandGrade
from command_incident import CommandIncident
from command_law import CommandLaw
from command_india import CommandIndia
from command_infos import CommandInfos
from command_matricule import CommandMatricule
from command_mea import CommandMEA
from command_ronanda import CommandRonanda
from command_saisie import CommandSaisie
from command_serveur import CommandServeur
from command_signature import CommandSignature
from command_tir import CommandTir
from command_tufumes import CommandTufumes
from command_vol import CommandVol

import discord

from common import get_signature
from db import DB
from seal import Seal


class Ronanda:

    commands = {
        "hall": CommandRonanda(),
        "secrétariat-a": CommandRonanda(),
        "secrétariat-b": CommandRonanda(),
        "secrétariat-c": CommandRonanda(),

        "tufumes": CommandTufumes(),

        "signature": CommandSignature(server_required=False),
        "grade": CommandGrade(server_required=False),
        "assignation": CommandAssignation(server_required=False),
        "matricule": CommandMatricule(server_required=False),
        "serveur": CommandServeur(server_required=False),
        "infos": CommandInfos(server_required=False),

        "arrestation": CommandArrestation(),
        "mea": CommandMEA(),
        "fourrière": CommandFourriere(),
        "ddf": CommandDDF(),
        "vol": CommandVol(),
        "india": CommandIndia(),
        "saisie": CommandSaisie(),
        "cadavre": CommandCadavre(),
        "tir": CommandTir(),
        "incident": CommandIncident(),

        "charge": CommandCharge(),
        "article": CommandArticle(),
        "caution": CommandCaution(),

        "loi": CommandLaw(),
    }

    def __init__(self, message):
        self.message = message

    async def answer(self, text, embed=None):
        await self.message.channel.send("> {author} {text}".format(author=self.message.author.mention, text=text),
                                        embed=embed)

    def load_or_create_user(self):
        tag = self.message.author
        user = DB().get_user(tag)
        if user is None:
            DB().create_user(tag=tag)
            user = DB().get_user(tag=tag)
        character_name = self.message.author.nick
        character = DB().get_character(name=character_name)
        if character is None:
            DB().create_character(name=character_name, user_id=user['id'])
        else:
            if character['user_id'] != user['id']:
                raise ValueError("Le personnage `{}` ne vous appartient pas.".format(character['name']))
        return user

    async def check_signature(self, officer):
        if get_signature(officer) == officer:
            await self.answer(
                "Par défaut, vos formulaires sont signés : `{}`\n"
                "`#signature` pour modifier la signature de vos formulaires :person_tipping_hand:".format(officer))

    async def increment_user_stats(self, user_tag):
        stats = DB().get_user(tag=user_tag)['stats'] + 1
        DB().update_user(tag=user_tag, stats=stats)

    @staticmethod
    async def welcome(member, channel):
        await channel.send(
            f"Bienvenue dans le département d'administration de la paperasse {member.mention} :person_tipping_hand:")

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(210, 190, 100),
            title=":desktop: Administration de la paperasse",
            description="Je suis là pour vous faire gagner du temps sur l'envoi de vos formulaires. "
                        "Pour cela, il suffit de m'interpeller en me taguant avec `@Ronanda`. "
                        "Rendez-vous dans le `#secrétariat` !"
        )
        embed.set_thumbnail(url=str(Seal.CITY_OF_LS))
        await channel.send(embed=embed)

    async def process(self, command=None, help=False):
        if self.message.author.nick is None:
            await self.answer("Changez votre pseudo discord local pour mettre le `Prénom Nom` de votre personnage.")
            return

        try:
            user = self.load_or_create_user()
        except ValueError as e:
            await self.answer(e)
            return

        if command is not None:
            await self.commands[command].process(self, user.get('server'))
            return

        if help:
            await self.commands["secrétariat-a"].process(self, user.get('server'))
            return

        await self.commands[command].process(self, user.get('server'))
