import discord

from datetime import datetime

from command import Command
from common import *
from gtaw.form import Form
from seal import Seal


class CommandArrestation(Command):
    async def _process(self, ronanda):
        message = ronanda.message
        officer = message.author.nick
        args = message.content.split(' ')
        required = ['suspect', 'peines']

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
                embed.set_thumbnail(url=str(Seal.LSPD))
                await message.channel.send(embed=embed)
                return

            suspect = args[1].replace('_', ' ').title()

            requested_charges = args[2:]
            charges = []
            livre = get_livre()
            for code_charge in requested_charges:
                if code_charge in livre:
                    charge = code_charge + livre[code_charge]
                    charges.append(charge)
                else:
                    embed = discord.Embed(
                        colour=discord.Colour.dark_red(),
                        title=":no_entry_sign: Erreur de traitement",
                        description="Il y a un soucis avec votre demande"
                    )
                    embed.add_field(name="Message",
                                    value="L'identifiant pénal `{}` n'existe pas.\n"
                                          "Utilisez `#charge` pour faire une recherche.".format(code_charge),
                                    inline=False)
                    embed.set_thumbnail(url=str(Seal.LSPD))
                    await message.channel.send(embed=embed)
                    return
            charges = ''.join(charges)
            title, impressions = self.build_arrestation(suspect, charges, get_signature(officer))

            for impression in impressions:
                await message.channel.send("```{}```".format(impression))

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":oncoming_police_car: Formulaire d'enregistrement en détention",
                description="Enregistrement de {suspect} par {officer}\nFait le {date}".format(
                    suspect=suspect, date=datetime.now().strftime('%d/%m/%Y'), officer=officer)
            )
            embed.set_thumbnail(url=str(Seal.LSPD))
            embed.add_field(name="A soumettre ici",
                            value="https://lspd-online.forumactif.com/post?f=10&mode=newtopic", inline=False)
            embed.add_field(name="Titre", value="```{}```".format(title), inline=False)
            embed.add_field(name="Casier LRP",
                            value="https://www.leroleplay.fr/job_db.php?jobid=1&character=704&section=casier&action=add"
                            .format(title), inline=False)
            embed.set_footer(text="Voilà pour vous !")
            await message.channel.send(embed=embed)

            await ronanda.check_signature(officer)

        else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Impression d'un formulaire d'enregistrement en détention."
            )
            embed.set_thumbnail(url=str(Seal.LSPD))
            embed.add_field(name="Syntaxe", value="```#arrestation <suspect> <identifiants pénaux>```",
                            inline=False)
            embed.add_field(name="Exemple", value="```#arrestation Sosmu_Sabanic 2311-1 312-1```", inline=False)
            await message.channel.send(embed=embed)

    def build_arrestation(self, suspect, charges, signature):
        title = "{suspect} ({date})".format(suspect=suspect, date=datetime.now().strftime('%d/%m/%Y'))

        vars_1 = {}
        vars_2 = {
            'suspect': suspect,
        }
        vars_3 = {
            'charges': charges,
            'date': datetime.now().strftime('%d/%m/%Y'),
            'signature': signature
        }
        impression_1 = instantiate_template('arrestation1', vars_1)
        impression_2 = instantiate_template('arrestation2', vars_2)
        impression_3 = instantiate_template('arrestation3', vars_3)
        return title, [impression_1, impression_2, impression_3]

    async def _process_gtaw(self, ronanda):
        messages, embed = Form(
            "arrestation",
            ronanda.message.content,
            officer=ronanda.message.author.nick
        ).generate()
        await ronanda.answer(":printer:")
        for message in messages:
            await ronanda.message.channel.send("```{}```".format(message))
        await ronanda.message.channel.send(embed=embed)
