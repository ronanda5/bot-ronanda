import discord

from commands.command import Command, EnumCommand
from seal import Seal


class CommandHelp(Command):

    async def process(self, ronanda):
        message = ronanda.message
        officer = message.author.nick
        await ronanda.check_signature(officer)
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(210, 190, 100),
            title=":desktop: Administration de la paperasse",
        )
        embed.set_thumbnail(url=str(Seal.CITY_OF_LS))
        embed.add_field(name="**!infos**", value="Voir vos informations et vos personnages", inline=False)
        embed.add_field(name="**!signature**", value="Modifier la signature de ses formulaires", inline=False)
        embed.add_field(name="**!grade**", value="Modifier son grade", inline=False)
        embed.add_field(name="**!matricule**", value="Modifier son matricule", inline=False)
        embed.add_field(name="\u200b\n`!loi`",
                        value="Rechercher un texte dans la loi à partir d'un mot-clé", inline=False)
        embed.add_field(name="`!arrestation`",
                        value="Rapport d'arrestation & MEA", inline=False)
        embed.add_field(name="`!saisie`",
                        value="Rapport de saisie", inline=False)
        embed.add_field(name="`!cadavre`",
                        value="Rapport de découverte de cadavre", inline=False)
        embed.add_field(name="`!tir`",
                        value="Rapport de tir", inline=False)
        embed.add_field(name="`!incident`",
                        value="Rapport d'incident", inline=False)
        await ronanda.message.channel.send(embed=embed)
