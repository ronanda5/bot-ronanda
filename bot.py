from commands.command import EnumCommand
from config import logging
import discord

from ronanda import Ronanda


class Bot(discord.Client):

    def __init__(self, command_prefix, db):
        super().__init__()

        self.command_prefix = command_prefix
        self.db = db

    async def on_ready(self):
        # add help on how to interact with the bot
        await self.change_presence(activity=discord.Game("@Ronanda"))

        logging.info("Ronanda is now listening !")

    async def on_message(self, message):
        # do not process message if message is from a bot
        if message.author.bot:
            return

        ronanda = Ronanda(message, self.db)

        # display help if bot is mentioned
        is_bot_mentioned = f'<@!{self.user.id}>' in message.content
        if is_bot_mentioned:
            await ronanda.help()

        # process request if command name is specified
        command_name = self.get_command_from_discord_message(message)
        if command_name is not None:
            await ronanda.process(command=command_name)

    def get_command_from_discord_message(self, message):
        # check if user message starts with the command prefix
        if not message.content.startswith(self.command_prefix):
            return

        # parse string to get command name
        return message.content.split(" ")[0].replace(self.command_prefix, "")
