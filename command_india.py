from datetime import datetime

import discord

from command import Command
from common import *


class CommandIndia(Command):
    async def _process(self, ronanda):
        message = ronanda.message
        officer = message.author.nick
        args = message.content.split(' ')
        required = ['debut', 'fin', 'chef', 'operateurs', 'vehicules', 'interventions']
        if len(args) > len(required):

            debut = args[1]
            fin = args[2]
            chef = args[3].replace('_', ' ').upper()
            operateurs = args[4].replace(',', ', ').upper()
            vehicules = args[5].replace(',', ', ').upper()

            interventions = ""
            informations = None
            is_interventions = True
            is_informations = False
            for arg in args[6:]:
                if arg.find('=') != -1:
                    is_interventions = False
                    if arg.find('informations') != -1:
                        is_informations = True
                        informations = arg.split('=')[1]
                elif is_interventions:
                    interventions = '{} {}'.format(interventions, arg)
                elif is_informations:
                    informations = '{} {}'.format(informations, arg)
            if informations is not None:
                informations = "\n".join([information.strip() for information in informations.split(';')])
            interventions = "\n".join([intervention.strip() for intervention in interventions.split(';')])

            impressions = self.build_india(officer, debut, fin, chef, operateurs, vehicules, interventions, informations)
            for impression in impressions:
                await message.channel.send("```{}```".format(impression))

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":helicopter: Rapport INDIA",
                description="Nouveau rapport INDIA généré par {officer}\nFait le {date}".format(
                    date=datetime.now().strftime('%d/%m/%Y'), officer=officer)
            )
            embed.set_thumbnail(url="https://www.zupimages.net/up/19/32/cagn.png")
            embed.add_field(name="A soumettre ici",
                            value="https://lspd-online.forumactif.com/t8398-swat-pole-administratif-patrouilles-india",
                            inline=False)
            embed.set_footer(text="Voilà pour vous !")
            await message.channel.send(embed=embed)

            await ronanda.check_signature(officer)

        else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Impression d'un rapport INDIA."
            )
            embed.set_thumbnail(url="https://www.zupimages.net/up/19/32/cagn.png")
            embed.add_field(name="Syntaxe",
                            value="```#india <début> <fin> <chef> <opérateurs> <véhicules> <interventions> "
                                  "<informations (optionnel)>```", inline=False)
            embed.add_field(name="Exemple",
                            value="```#india 20:00 20:30 Baker Roberts,Morgans,Torrance Huntley,Enforcer "
                                  "Retranchement sur Idlewood;Soutien FBI "
                                  "informations=2 suspects arrêtés;1 saisie d'armes```", inline=False)
            await message.channel.send(embed=embed)

    def build_india(self, officer, debut, fin, chef, operateurs, vehicules, interventions, informations=None):
        var = {
            'officier': officer,
            'date': datetime.now().strftime('%d/%m/%Y'),
            'debut': debut,
            'fin': fin,
            'chef': chef,
            'operateurs': operateurs,
            'vehicules': vehicules,
            'interventions': interventions,
            'informations': informations if informations is not None else "N/A",
            'signature': get_signature(officer)
        }
        impression = instantiate_template('india', var)
        return [impression]