import discord

from command import Command
from common import get_grade
from db import DB
from seal import Seal


class CommandGrade(Command):
    async def _process(self, ronanda):
        message = ronanda.message
        officer = message.author.nick
        args = message.content.split(' ')
        required = ['grade']
        if len(args) > len(required):
            grade_request = ' '.join(args[1:]).strip()
            DB().update_character(name=message.author.nick, grade=grade_request)
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":white_check_mark: Changement de grade effectué",
                description="Changement du grade de {officier}".format(officier=officer)
            )
            embed.add_field(name="Nouveau grade",
                            value="```{}```".format(get_grade(message.author.nick)),
                            inline=False)
            embed.set_thumbnail(url=str(Seal.LSPD))
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Modifier son grade."
            )
            embed.set_thumbnail(url=str(Seal.LSPD))
            embed.add_field(name="Syntaxe",
                            value="```#grade <grade>```",
                            inline=False)
            embed.add_field(name="Exemple",
                            value="```#grade Officier II```",
                            inline=False)
            embed.add_field(name="Votre grade actuel ({})".format(message.author.nick),
                            value="`{}`".format(get_grade(message.author.nick)),
                            inline=False)
            await message.channel.send(embed=embed)
