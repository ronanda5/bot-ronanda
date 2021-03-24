import discord

from command import Command
from common import *


class CommandCaution(Command):
    async def _process(self, ronanda):
        message = ronanda.message
        args = message.content.split(' ')
        required = ['mots-clés']

        if len(args) > len(required):

            requested_caution = ' '.join(args[1:])
            cautions = find_caution(requested_caution)

            if len(cautions) > 0:

                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(210, 190, 100),
                    title=":book: Résultat de la recherche",
                    description="Voici la ou les caution(s) trouvée(s)."
                )
                for caution in cautions:
                    embed.add_field(name="Caution trouvée", value="```{}```".format(caution), inline=False)
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
                                value="Aucune caution trouvée pour les mots-clés `{}`".format(requested_caution),
                                inline=False)
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/689355937466548237/700726187135205506/ZiYDsGM.png")
                await message.channel.send(embed=embed)

        else:

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Rechercher une caution à partir de mots-clés."
            )
            embed.add_field(name="Syntaxe", value="```#caution <numéro ou mots-clés>```",
                            inline=False)
            embed.add_field(name="Exemple", value="```#caution conduite```",
                            inline=False)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/689355937466548237/700726187135205506/ZiYDsGM.png")
            await message.channel.send(embed=embed)
