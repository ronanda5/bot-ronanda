from commands.command import Command, EnumCommand
from form import Form
from seal import Seal


class CommandTir(Command):

    async def process(self, ronanda):
        character = ronanda.db.get_character(name=ronanda.message.author.nick)
        messages, embed = Form(
            EnumCommand.FIRE,
            ronanda.message.content,
            seal=Seal.INTERNAL_AFFAIRS,
            character=character
        ).generate()
        await ronanda.answer(":printer:")
        for message in messages:
            await ronanda.message.channel.send("```{}```".format(message))
        await ronanda.message.channel.send(embed=embed)
