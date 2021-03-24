import discord

from command import Command
from common import *
from gtaw.form import Form
from seal import Seal


class CommandSaisie(Command):
    async def _process(self, ronanda):
        message = ronanda.message
        officer = message.author.nick
        args = message.content.split(' ')
        required = ['suspect', 'contexte', 'saisies']

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
            contexte = ''
            autre = None
            saisies = {}
            is_contexte = True
            is_autre = False
            for arg in args[2:]:
                if arg.find('=') != -1:
                    is_contexte = False
                    if arg.find('autre') != -1:
                        is_autre = True
                        autre = arg.split('=')[1]
                    else:
                        quality = arg.split('=')[0]
                        quantity = arg.split('=')[1]
                        saisies[quality] = quantity
                elif is_contexte:
                    contexte = '{} {}'.format(contexte, arg)
                elif is_autre:
                    autre = '{} {}'.format(autre, arg)
            if autre is not None:
                saisies['autre'] = autre.strip()
            preuves = None
            if message.attachments:
                attachments = []
                screenshot_template = '[img]{url}[/img]'
                for attachment in message.attachments:
                    attachments.append(screenshot_template.format(url=attachment.url))
                preuves = '\n'.join(attachments)
            impressions = self.build_saisie(suspect, contexte.strip(), preuves, **saisies)
            for impression in impressions:
                await message.channel.send("```{}```".format(impression))
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":moneybag: Formulaire de dépôt de saisie",
                description="Dépôt de saisie fait par {officer}".format(officer=officer)
            )
            embed.set_thumbnail(url=str(Seal.LSPD))
            embed.add_field(name="**BI** A soumettre ici",
                            value="https://lspd-online.forumactif.com/post?t=2881&mode=reply", inline=False)
            embed.add_field(name="**BC** A soumettre ici",
                            value="https://lspd-online.forumactif.com/post?t=2880&mode=reply", inline=False)
            embed.add_field(name="**BOS** A soumettre ici",
                            value="https://lspd-online.forumactif.com/post?t=2882&mode=reply", inline=False)
            embed.set_footer(text="Voilà pour vous !")
            await message.channel.send(embed=embed)

            await ronanda.check_signature(officer)

        else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Impression d'un formulaire de dépôt de saisie."
            )
            embed.set_thumbnail(url=str(Seal.LSPD))
            embed.add_field(name="Syntaxe", value="```#saisie <suspect> <contexte> <saisies>```",
                            inline=False)
            embed.add_field(name="Exemple",
                            value="```#saisie Karim_Cassidy Fouille après arrestation canna=9 meth=101 colt=1 "
                                  "autre=Tournevis, batte```", inline=False)
            embed.add_field(name="Options drogues", value="`meth` `coke` `canna` `stero` `hero`", inline=False)
            embed.add_field(name="Options armes",
                            value="`colt` `silencieux` `deagle` `shotgun` `uzi` `mp5` `ak47` `m4` `tec9` `rifle` "
                                  "`sniper` `rpg`", inline=False)
            embed.add_field(name="Autres options", value="`autre`", inline=False)
            embed.add_field(name="Screens", value="Vous pouvez joindre 1 screen directement à la commande pour "
                                                  "l'intégrer aux preuves OOC", inline=False)
            await message.channel.send(embed=embed)

    def build_saisie(self, suspect, contexte, preuves=None, meth=0, coke=0, canna=0, stero=0, hero=0,
                     colt=0, silencieux=0, deagle=0, shotgun=0, uzi=0, mp5=0, ak47=0, m4=0, tec9=0, rifle=0, sniper=0,
                     rpg=0, autre='N/A'):

        vars_1 = {
            'suspect': suspect,
            'contexte': contexte,
            'meth': saisie_to_str(meth),
            'coke': saisie_to_str(coke),
            'canna': saisie_to_str(canna),
            'steroide': saisie_to_str(stero),
            'heroine': saisie_to_str(hero)
        }
        vars_2 = {
            'colt': saisie_to_str(colt),
            'silencieux': saisie_to_str(silencieux),
            'deagle': saisie_to_str(deagle),
            'shotgun': saisie_to_str(shotgun),
            'uzi': saisie_to_str(uzi),
            'mp5': saisie_to_str(mp5),
            'ak47': saisie_to_str(ak47),
            'm4': saisie_to_str(m4),
            'tec9': saisie_to_str(tec9),
            'rifle': saisie_to_str(rifle),
            'sniper': saisie_to_str(sniper),
            'rpg': saisie_to_str(rpg),
            'autre': autre,
            'preuves': 'Joindre vos screens/logs prouvant la saisie.'
        }
        if preuves is not None:
            vars_2['preuves'] = preuves
        impression_1 = instantiate_template('saisie1', vars_1)
        impression_2 = instantiate_template('saisie2', vars_2)
        return [impression_1, impression_2]

    async def _process_gtaw(self, ronanda):
        messages, embed = Form(
            "saisie",
            ronanda.message.content,
            officer=ronanda.message.author.nick
        ).generate()
        await ronanda.answer(":printer:")
        for message in messages:
            await ronanda.message.channel.send("```{}```".format(message))
        await ronanda.message.channel.send(embed=embed)
