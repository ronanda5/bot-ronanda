import discord

from command import Command
from common import get_assignation
from db import DB
from seal import Seal


class CommandAssignation(Command):
    async def _process(self, ronanda):
        message = ronanda.message
        officer = message.author.nick
        args = message.content.split(' ')
        required = ['assignation']
        if len(args) > len(required):
            assignation_request = ' '.join(args[1:]).strip()
            DB().update_character(name=message.author.nick, assignation=assignation_request)
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":white_check_mark: Changement d'assignation effectué",
                description="Changement d'assignation de {officier}".format(officier=officer)
            )
            embed.add_field(name="Nouvelle assignation",
                            value="```{}```".format(get_assignation(message.author.nick)),
                            inline=False)
            embed.set_thumbnail(url=str(Seal.LSPD))
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Modifier son assignation."
            )
            embed.set_thumbnail(url=str(Seal.LSPD))
            embed.add_field(name="Syntaxe",
                            value="```#assignation <assignation>```",
                            inline=False)
            embed.add_field(name="Exemple",
                            value="```#assignation Bureau des Opérations Spéciales```",
                            inline=False)
            embed.add_field(name="Votre assignation actuelle ({})".format(message.author.nick),
                            value="`{}`".format(get_assignation(message.author.nick)),
                            inline=False)
            await message.channel.send(embed=embed)
