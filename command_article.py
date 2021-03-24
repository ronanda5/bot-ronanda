import discord

from command import Command
from common import *


class CommandArticle(Command):
    async def _process(self, ronanda):
        message = ronanda.message
        args = message.content.split(' ')
        required = ['mots-clés']

        if len(args) > len(required):

            requested_article = ' '.join(args[1:])
            articles = find_article(requested_article)

            if len(articles) > 0:

                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(210, 190, 100),
                    title=":book: Résultat de la recherche", description="Voici la ou les article(s) trouvé(s).")
                for article in articles:
                    embed.add_field(name="Article trouvé", value="```{}```".format(article), inline=False)
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/689355937466548237/700726187135205506/ZiYDsGM.png")
                try:
                    await message.channel.send(embed=embed)
                except discord.errors.HTTPException:
                    await message.channel.send("> Il y a trop de résultats. Il faut affiner la recherche.")

            else:
                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(210, 190, 100),
                    title=":information_source: Aucun résultat",
                    description="J'ai rien trouvé"
                )
                embed.add_field(name="Message",
                                value="Aucun article trouvé avec le numéro `{}`".format(requested_article),
                                inline=False)
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/689355937466548237/700726187135205506/ZiYDsGM.png")
                await message.channel.send(embed=embed)

        else:

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Trouver l'énoncé d'un article dans les codes de lois à partir de son numéro."
            )
            embed.add_field(name="Syntaxe", value="```#article <numéro ou mots-clés>```",
                            inline=False)
            embed.add_field(name="Exemple", value="```#article 237-5```",
                            inline=False)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/689355937466548237/700726187135205506/ZiYDsGM.png")
            await message.channel.send(embed=embed)
