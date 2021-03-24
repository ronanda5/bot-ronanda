import time

import discord

from commands.command import Command
from law import Law
from seal import Seal


class CommandLaw(Command):

    def __init__(self):
        super().__init__()
        self.law = Law()
        self.required = ['mot-clé']

    async def process(self, ronanda):
        message = ronanda.message
        args = message.content.split(' ')

        if len(args) > len(self.required):

            requested_charge = ' '.join(args[1:])
            laws = self.law.find(requested_charge)

            if len(laws) > 0:

                await ronanda.answer("Article(s) de loi trouvé(s) : **{}**".format(len(laws)))

                if len(laws) > 20:
                    await ronanda.answer("Le nombre d'articles trouvés est trop élevé, soyez plus précis.")
                    return

                for title, content in laws.items():
                    embed = discord.Embed(
                        colour=discord.Colour.from_rgb(210, 190, 100),
                        title=":book: {}".format(title),
                        description="```{}```".format(content)
                    )
                    embed.set_thumbnail(url=str(Seal.SA))
                    try:
                        await message.channel.send(embed=embed)
                    except discord.errors.HTTPException:
                        await ronanda.answer("L'article {} est trop long pour être affiché.".format(title))
                    time.sleep(0.5)

            else:
                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(210, 190, 100),
                    title=":information_source: Aucun résultat",
                    description="Aucun résultat n'a été trouvé dans les textes de lois."
                )
                embed.add_field(name="Votre recherche :",
                                value="`{}`".format(requested_charge),
                                inline=False)
                embed.set_thumbnail(url=str(Seal.SA))
                await message.channel.send(embed=embed)

        else:

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Rechercher un texte dans la loi à partir d'un mot clé."
            )
            embed.add_field(name="Syntaxe", value="```!loi <mot-clé>```",
                            inline=False)
            embed.add_field(name="Exemple", value="```!loi meurtre```",
                            inline=False)
            embed.add_field(name="Catégories de peines", value="```!loi 449```",
                            inline=False)
            embed.set_thumbnail(url=str(Seal.SA))
            await message.channel.send(embed=embed)
