import discord

from command import Command
from common import *


class CommandCharge(Command):
    async def _process(self, ronanda):
        message = ronanda.message
        args = message.content.split(' ')
        required = ['mots-clés']

        if len(args) > len(required):

            requested_charge = ' '.join(args[1:])
            charges = find_charge(requested_charge)

            if len(charges) > 0:

                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(210, 190, 100),
                    title=":book: Résultat de la recherche",
                    description="Voici la ou les charge(s) trouvée(s). Vous pouvez saisir leur code dans `#arrestation`"
                )
                for charge in charges:
                    embed.add_field(name="Charge trouvée", value="```{}```".format(charge), inline=False)
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
                                value="Aucune peine trouvée pour les mots-clés `{}`".format(requested_charge),
                                inline=False)
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/689355937466548237/700726187135205506/ZiYDsGM.png")
                await message.channel.send(embed=embed)

        else:

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Rechercher une charge dans le livre des peines à partir de mots-clés."
            )
            embed.add_field(name="Syntaxe", value="```#charge <numéro ou mots-clés>```",
                            inline=False)
            embed.add_field(name="Exemple", value="```#charge refus d'obtempérer```",
                            inline=False)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/689355937466548237/700726187135205506/ZiYDsGM.png")
            await message.channel.send(embed=embed)
