import discord

from command import Command
from db import DB
from seal import Seal


class CommandServeur(Command):
    async def _process(self, ronanda):
        message = ronanda.message
        user_tag = message.author
        args = message.content.split(' ')
        required = ['server']
        if len(args) > len(required):
            server = args[1]
            if 'lrp' not in server and 'gtaw' not in server:
                await ronanda.answer(
                    "Le serveur `{}` n'est pas pris en charge. Choisissez entre `gtaw` et `lrp`.".format(server))
                return
            DB().update_user(user_tag, server=server)
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":white_check_mark: Changement de serveur effectué",
                description="{user_tag} a correctement changé son serveur.".format(user_tag=user_tag)
            )
            embed.add_field(name="Votre serveur",
                            value="```{}```".format(server), inline=False)
            embed.set_thumbnail(url=str(Seal.LSPD))
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Cette commande sert à changer votre serveur pour générer les formulaires adéquats."
            )
            embed.set_thumbnail(url=str(Seal.LSPD))
            embed.add_field(name="Syntaxe",
                            value="```#serveur <serveur>```",
                            inline=False)
            embed.add_field(name="Valeurs possibles",
                            value="`lrp` `gtaw`",
                            inline=False)
            embed.add_field(name="Exemple",
                            value="```#serveur gtaw```",
                            inline=False)
            embed.add_field(name="Votre serveur actuel",
                            value="`{}`".format(DB().get_user(user_tag)['server']),
                            inline=False)
            await message.channel.send(embed=embed)
