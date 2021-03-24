import discord

from commands.command import Command
from seal import Seal


class CommandInfos(Command):

    async def process(self, ronanda):
        message = ronanda.message
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(210, 190, 100),
            title=":information_source: Informations & personnages de {}".format(message.author.name),
            description="Vos informations et vos personnages."
        )
        embed.set_thumbnail(url=str(Seal.LSPD))
        user = ronanda.db.get_user(tag=message.author)
        serveur = user.get('server')
        embed.add_field(name="Serveur",
                        value="```{}```".format("Aucun" if serveur is None else serveur),
                        inline=True)
        embed.add_field(name="Formulaires & recherches",
                        value="```{}```".format(user['stats']),
                        inline=True)
        characters = ronanda.db.get_characters(user_id=user['id'])
        number = 1
        for character in characters:
            embed.add_field(name="\u200b\nPersonnage #{}".format(number),
                            value="```{}```".format(character['name']),
                            inline=False)
            embed.add_field(name="Signature",
                            value="```{}```".format(
                                "Aucune" if character['signature'] is None else character['signature']),
                            inline=True)
            embed.add_field(name="Grade",
                            value="```{}```".format(
                                "Aucun" if character['grade'] is None else character['grade']),
                            inline=True)
            embed.add_field(name="Assignation",
                            value="```{}```".format(
                                "Aucune" if character['assignation'] is None else character['assignation']),
                            inline=True)
            embed.add_field(name="Matricule",
                            value="```{}```".format(
                                "Aucun" if character['matricule'] is None else character['matricule']),
                            inline=True)
            number = number + 1
        await message.channel.send(embed=embed)
