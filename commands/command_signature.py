import discord

from commands.command import Command
from seal import Seal


class CommandSignature(Command):

    async def process(self, ronanda):
        message = ronanda.message
        character_name = message.author.nick
        args = message.content.split(' ')
        required = ['signature']
        if len(args) > len(required):
            signature_request = ' '.join(args[1:]).strip()
            ronanda.db.update_character(name=message.author.nick, signature=signature_request)
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":white_check_mark: Changement de signature effectué",
                description="Changement de la signature de {character_name}".format(character_name=character_name)
            )
            embed.add_field(name="Nouvelle signature",
                            value="```{}```".format(ronanda.get_signature(message.author.nick)),
                            inline=False)
            embed.set_thumbnail(url=str(Seal.LSPD))
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="Modifier la signature de ses formulaires."
            )
            embed.set_thumbnail(url=str(Seal.LSPD))
            embed.add_field(name="Syntaxe",
                            value="```!signature <signature>```",
                            inline=False)
            embed.add_field(name="Exemple 1",
                            value="```!signature K.KRAUS 12345 BI```",
                            inline=False)
            embed.add_field(name="Votre signature actuelle",
                            value="`{}`".format(ronanda.get_signature(message.author.nick)),
                            inline=False)
            await message.channel.send(embed=embed)
