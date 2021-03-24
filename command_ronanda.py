import discord

from command import Command
from seal import Seal


class CommandRonanda(Command):
    async def common(self, ronanda, server):
        message = ronanda.message
        officer = message.author.nick
        await ronanda.check_signature(officer)
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(210, 190, 100),
            title=":desktop: Administration de la paperasse",
        )
        embed.set_thumbnail(url=str(Seal.CITY_OF_LS))
        embed.add_field(name="Serveur : `{}`".format(server),
                        value="Les commandes disponibles pour ce serveur sont affichées ci-dessous, "
                              "tapez `#serveur` pour en changer", inline=False)
        embed.add_field(name="\u200b\n**#serveur** *nouveau !*",
                        value="Changer de serveur pour utiliser les bons formulaires",
                        inline=False)
        embed.add_field(name="**#infos** *nouveau !*", value="Voir vos informations et vos personnages", inline=False)
        embed.add_field(name="**#signature**", value="Modifier la signature de ses formulaires", inline=False)
        embed.add_field(name="**#grade**", value="Modifier son grade", inline=False)
        embed.add_field(name="**#assignation**", value="Modifier son assignation", inline=False)
        embed.add_field(name="**#matricule**", value="Modifier son matricule", inline=False)
        return embed

    async def _process(self, ronanda):
        embed = await self.common(ronanda, "LRP")
        embed.add_field(name="\u200b\n`#arrestation` :oncoming_police_car:",
                        value="Impression d'un formulaire d'enregistrement en détention", inline=False)
        embed.add_field(name="`#saisie` :moneybag:", value="Impression d'un formulaire de dépôt de saisie",
                        inline=False)
        embed.add_field(name="`#mea` :man_judge:", value="Impression d'une mise en accusation",
                        inline=False)
        embed.add_field(name="`#fourrière` :construction:",
                        value="Impression d'un formulaire de placement en fourrière", inline=False)
        embed.add_field(name="`#ddf` :rotating_light:",
                        value="Impression d'un formulaire de signalement de délit de fuite", inline=False)
        embed.add_field(name="`#vol` :helicopter:", value="Impression d'un rapport de vol", inline=False)
        embed.add_field(name="`#india` :oncoming_police_car:", value="Impression d'un rapport INDIA",
                        inline=False)
        embed.add_field(name="`#charge` :book:",
                        value="Rechercher une charge dans le livre des peines à partir de mots-clés", inline=False)
        embed.add_field(name="`#article` :book:",
                        value="Trouver l'énoncé d'un article dans les codes de lois à partir de son numéro",
                        inline=False)
        embed.add_field(name="`#caution` :dollar:",
                        value="Rechercher une caution à partir de mots-clés", inline=False)
        await ronanda.message.channel.send(embed=embed)

    async def _process_gtaw(self, ronanda):
        embed = await self.common(ronanda, "GTAW")
        embed.add_field(name="\u200b\n`#loi` *nouveau !*",
                        value="Rechercher un texte dans la loi à partir d'un mot-clé", inline=False)
        embed.add_field(name="`#arrestation` *nouveau !*",
                        value="Rapport d'arrestation & MEA", inline=False)
        embed.add_field(name="`#saisie` *nouveau !*",
                        value="Rapport de saisie", inline=False)
        embed.add_field(name="`#cadavre` *nouveau !*",
                        value="Rapport de découverte de cadavre", inline=False)
        embed.add_field(name="`#tir` *nouveau !*",
                        value="Rapport de tir", inline=False)
        embed.add_field(name="`#incident` *nouveau !*",
                        value="Rapport d'incident", inline=False)
        await ronanda.message.channel.send(embed=embed)
