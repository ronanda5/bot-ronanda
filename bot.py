from config import logging
import re
import discord

from db import DB
from ronanda import Ronanda


class Bot(discord.Client):

    channel_ids = {}

    def __init__(self):
        super().__init__()
        DB()

    async def setup(self):
        pass

    def get_command(self, message):
        args = message.content.split(' ')
        channel = None
        matches = re.match("<#([0-9]*)>", args[0])
        if matches:
            channel = self.get_channel(int(matches.group(1)))
        command = None
        if channel is not None:
            command, args[0] = channel.name, channel.name
        return command

    async def on_ready(self):
        await self.setup()
        await self.change_presence(activity=discord.Game("@Ronanda"))
        logging.info('Ronanda is ready')

    async def on_member_join(self, member):
        channel = discord.utils.get(self.get_all_channels(), name="hall")
        await Ronanda.welcome(member, channel)

    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith("!"):
            await Ronanda(message).answer(
                "J'évolue ! Les commandes commencent par **#** et non plus par **!**."
                "\nTaggez moi avec {} pour afficher toutes les commandes disponibles.".format(self.user.mention))
            return

        mentioned = f'<@!{self.user.id}>' in message.content
        command = self.get_command(message)
        if mentioned or command is not None:
            await Ronanda(message).process(command=command, help=mentioned)
