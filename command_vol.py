from datetime import datetime

import discord

from command import Command
from common import *


class CommandVol(Command):
    async def _process(self, ronanda):
        message = ronanda.message
        officer = message.author.nick
        args = message.content.split(' ')
        required = ['debut', 'fin', 'interventions']
        if len(args) > len(required):

            debut = args[1]
            fin = args[2]
            interventions = "\n".join([intervention.strip() for intervention in ' '.join(args[3:]).split(';')])

            impressions = self.build_vol(officer, debut, fin, interventions, get_signature(officer))
            for impression in impressions:
                await message.channel.send("```{}```".format(impression))

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":helicopter: Rapport de vol",
                description="Nouveau rapport de vol généré par {officer}\nFait le {date}".format(
                    date=datetime.now().strftime('%d/%m/%Y'), officer=officer)
            )
            embed.set_thumbnail(url="https://i.gyazo.com/e1e62e5f6132392f92d8c140e88fbf48.png")
            embed.add_field(name="A soumettre ici", value="https://lspd-online.forumactif.com/t6847-rapports-de-vol",
                            inline=False)
            embed.set_footer(text="Voilà pour vous !")
            await message.channel.send(embed=embed)

            await ronanda.check_signature(officer)

        else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Impression d'un rapport de vol."
            )
            embed.set_thumbnail(url="https://i.gyazo.com/e1e62e5f6132392f92d8c140e88fbf48.png")
            embed.add_field(name="Syntaxe",
                            value="```#vol <début> <fin> <interventions>```", inline=False)
            embed.add_field(name="Exemple",
                            value="```#vol 20h00 21h00 Refus d'obtempérer sur "
                                  "Idlewood;Soutien retranchement sur Jefferson```", inline=False)
            await message.channel.send(embed=embed)

    def build_vol(self, officier, debut, fin, interventions, signature):
        var = {
            'officier': officier,
            'date': datetime.now().strftime('%d/%m/%Y'),
            'debut': debut,
            'fin': fin,
            'interventions': interventions,
            'signature': signature
        }
        impression = instantiate_template('vol', var)
        return [impression]
