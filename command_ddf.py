from datetime import datetime

import discord

from command import Command
from common import *
from seal import Seal


class CommandDDF(Command):
    async def _process(self, ronanda):
        message = ronanda.message
        officer = message.author.nick
        args = message.content.split(' ')
        required = ['type', 'modele', 'plaque', 'lieu', 'contexte']

        if len(args) > len(required):
            type_veh = args[1]
            try:
                type_veh = int(type_veh)
                if not (type_veh == 2 or type_veh == 4):
                    raise AttributeError
            except AttributeError:
                embed = discord.Embed(
                    colour=discord.Colour.dark_red(),
                    title=":no_entry_sign: Erreur de traitement",
                    description="Il y a un soucis avec votre demande"
                )
                embed.add_field(name="Message", value="Le type de véhicule `{}` n'existe pas. Seules les valeurs "
                                                      "`2` et `4` sont acceptées pour désigner respectivement un "
                                                      "véhicule de type deux-roues ou quatre-roues.".format(type_veh),
                                inline=False)
                embed.set_thumbnail(url=str(Seal.LSPD))
                await message.channel.send(embed=embed)
                return
            modele = args[2]
            plaque = args[3]
            lieu = args[4]

            contexte = ""
            commentaire = None
            is_contexte = True
            is_commentaire = False
            for arg in args[5:]:
                if arg.find('=') != -1:
                    is_contexte = False
                    if arg.find('commentaire') != -1:
                        is_commentaire = True
                        commentaire = arg.split('=')[1]
                elif is_contexte:
                    contexte = '{} {}'.format(contexte, arg)
                elif is_commentaire:
                    commentaire = '{} {}'.format(commentaire, arg)
            if commentaire is not None:
                commentaire = commentaire.strip()

            title, impression = self.build_ddf(officer, type_veh, modele, plaque, lieu, contexte.strip(), commentaire)
            await message.channel.send("```{}```".format(impression))
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":rotating_light: Formulaire de signalement de délit de fuite",
                description="Signalement de DDF fait par {officer}".format(officer=officer)
            )
            embed.set_thumbnail(url=str(Seal.LSPD))
            embed.add_field(name="A soumettre ici",
                            value="https://lspd-online.forumactif.com/post?f=65&mode=newtopic", inline=False)
            embed.add_field(name="Titre", value="```{}```".format(title), inline=False)
            embed.set_footer(text="Voilà pour vous !")
            await message.channel.send(embed=embed)

            if get_grade(officer) == "":
                await message.channel.send(
                    "> Ce formulaire demande un grade, par défaut rien n'a été mis.\n"
                    "`#grade` pour les modifier :person_tipping_hand:")

        else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Impression d'un formulaire de signalement de délit de fuite."
            )
            embed.set_thumbnail(url=str(Seal.LSPD))
            embed.add_field(name="Syntaxe", value="```#ddf <type_veh (`2` ou `4` roues)> <modele>"
                                                  "<plaque> <lieu> <contexte> <commentaire (optionnel)>```",
                            inline=False)
            embed.add_field(name="Exemple",
                            value="```#ddf 4 Tampa 1AB23 Idlewood Accident au Golden Residence "
                                  "commentaire=Suspect armé```",
                            inline=False)
            embed.add_field(name="Option", value="`commentaire` : ajouter un commentaire", inline=False)
            await message.channel.send(embed=embed)

    def build_ddf(self, officer_name, type_veh, modele, plaque, lieu, contexte, commentaire):
        title = "(Signalement de délit de fuite) {modele} - {plaque} ({date})".format(modele=modele, plaque=plaque,
                                                                                      date=datetime.now()
                                                                                      .strftime('%d/%m/%Y'))

        var = {
            'officier': officer_name,
            'grade': get_grade(officer_name),
            'deuxroues': "X" if type_veh == 2 else " ",
            'quatreroues': "X" if type_veh == 4 else " ",
            'modele': modele,
            'plaque': plaque,
            'contexte': contexte,
            'lieu': lieu,
            'date': datetime.now().strftime('%d/%m/%Y'),
            'commentaire': commentaire if commentaire is not None else "N/A"
        }
        impression = instantiate_template('ddf', var)
        return title, impression