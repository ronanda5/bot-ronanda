import discord

from commands.command import Command
from seal import Seal


class CommandMatricule(Command):

    async def process(self, ronanda):
        message = ronanda.message
        officer = message.author.nick
        args = message.content.split(' ')
        required = ['matricule']
        if len(args) > len(required):
            matricule_request = args[1]
            ronanda.db.update_character(name=message.author.nick, matricule=matricule_request)
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":white_check_mark: Changement du matricule effectué",
                description="Changement du matricule de {officier}".format(officier=officer)
            )
            embed.add_field(name="Nouveau matricule",
                            value="```{}```".format(ronanda.get_matricule(message.author.nick)),
                            inline=False)
            embed.set_thumbnail(url=str(Seal.LSPD))
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Modifier son matricule."
            )
            embed.set_thumbnail(url=str(Seal.LSPD))
            embed.add_field(name="Syntaxe",
                            value="```#matricule <matricule>```",
                            inline=False)
            embed.add_field(name="Exemple",
                            value="```#matricule 777```",
                            inline=False)
            embed.add_field(name="Votre matricule actuel ({})".format(message.author.nick),
                            value="`{}`".format(ronanda.get_matricule(message.author.nick)),
                            inline=False)
            await message.channel.send(embed=embed)
