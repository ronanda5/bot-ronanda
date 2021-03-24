from datetime import datetime

import discord

from command import Command
from common import *


class CommandMEA(Command):
    async def _process(self, ronanda):
        message = ronanda.message
        officer = message.author.nick
        args = message.content.split(' ')
        required = ['accuse', 'statut']

        if len(args) > len(required):

            try:
                args[1].index('_')
            except ValueError:
                embed = discord.Embed(
                    colour=discord.Colour.dark_red(),
                    title=":no_entry_sign: Erreur de traitement",
                    description="Il y a un soucis avec votre demande"
                )
                embed.add_field(name="Message",
                                value="Les `Prénom_Nom` doivent inclure le séparateur `_`, sinon je ne m'y "
                                      "retrouve plus.",
                                inline=False)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/689355937466548237/701113092494590064/"
                                        "Seal_of_the_United_States_Department_of_Justice.svg.png")
                await message.channel.send(embed=embed)
                return

            accuse = args[1].replace('_', ' ').title()

            statut = args[2]

            requested_cautions = args[3:]
            cautions = []
            livre = get_cautions()
            for code_caution in requested_cautions:
                if code_caution in livre:
                    caution = code_caution + livre[code_caution]
                    cautions.append(caution)
                else:
                    embed = discord.Embed(
                        colour=discord.Colour.dark_red(),
                        title=":no_entry_sign: Erreur de traitement",
                        description="Il y a un soucis avec votre demande"
                    )
                    embed.add_field(name="Message",
                                    value="L'identifiant pénal `{}` n'existe pas.\n"
                                          "Utilisez `#caution` pour faire une recherche.".format(code_caution),
                                    inline=False)
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/689355937466548237/7"
                                            "01113092494590064/Seal_of_the_United_States_Department_of_Justice.svg.png")
                    await message.channel.send(embed=embed)
                    return
            cautions = ''.join(cautions)

            statut = statut.strip().lower()
            if statut in ["arrêt", "arret", "aret",
                          "arrêté", "arrete", "arrête", "arreté", "arêté", "arete", "arête", "areté"]:
                statut = "arrêt"
            elif statut in ["libre"]:
                statut = "libre"
            else:
                embed = discord.Embed(
                    colour=discord.Colour.dark_red(),
                    title=":no_entry_sign: Erreur de traitement",
                    description="Il y a un soucis avec votre demande"
                )
                embed.add_field(name="Message",
                                value="Le statut `{}` n'existe pas.\nLes statuts valides sont `libre` ou `arrêt`".format(
                                    statut),
                                inline=False)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/689355937466548237/701113092494590064/"
                                        "Seal_of_the_United_States_Department_of_Justice.svg.png")
                await message.channel.send(embed=embed)
                return

            title, impression = self.build_mea(officer, accuse, statut, cautions)
            await message.channel.send("```{}```".format(impression))
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":man_judge: Mise en accusation",
                description="MEA de {accuse} par {officer}\nFait le {date}".format(
                    accuse=accuse, date=datetime.now().strftime('%d/%m/%Y'), officer=officer)
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/689355937466548237/701113092494590064/Seal_"
                                    "of_the_United_States_Department_of_Justice.svg.png")
            embed.add_field(name="A soumettre ici",
                            value="https://www.leroleplay.fr/post.php?fid=118", inline=False)
            embed.add_field(name="Titre", value="```{}```".format(title), inline=False)
            embed.set_footer(text="Voilà pour vous !")
            await message.channel.send(embed=embed)

            if get_grade(officer) == "":
                await message.channel.send(
                    "> Ce formulaire demande un grade, par défaut rien n'a été mis.\n"
                    "`#grade` pour les modifier :person_tipping_hand:")

            await message.channel.send(
                "> **ATTENTION** :man_judge: : Pensez à ajouter les faits et les preuves ")

        else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Impression d'une mise en accusation."
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/689355937466548237/701113092494590064/Seal_"
                                    "of_the_United_States_Department_of_Justice.svg.png")
            embed.add_field(name="Syntaxe", value="```#mea <accusé> <statut> <cautions (optionnel)>```",
                            inline=False)
            embed.add_field(name="Exemple accusé libre", value="```#mea Steve_Maoki libre 2-3 233-1```",
                            inline=False)
            embed.add_field(name="Exemple accusé arrêté", value="```#mea Steve_Maoki arrêt 2-3 233-1```", inline=False)
            await message.channel.send(embed=embed)

    def build_mea(self, officer_name, accuse, statut, cautions):
        title = "Peuple de San Andreas c. {accuse}".format(accuse=accuse)

        profession = "Agent au département de police de Los Santos"
        if not get_grade(officer_name) == "":
            profession = get_grade(officer_name) + " au département de police de Los Santos"
        var = {
            'officier': officer_name,
            'profession': profession,
            'accuse': accuse,
            'libre': "X" if statut == "libre" else "  ",
            'arret': "X" if statut == "arrêt" else "  ",
            'date': datetime.now().strftime('%d/%m/%Y à %Hh') if statut == "arrêt" else "N/A",
            'cautions': cautions if len(cautions) > 0 else 'Aucune libération sous caution.'
        }
        impression = instantiate_template('mea', var)
        return title, impression
