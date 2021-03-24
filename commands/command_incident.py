from commands.command import Command, EnumCommand
from forms.form import Form
from seal import Seal


class CommandIncident(Command):

    async def process(self, ronanda):
        character = ronanda.db.get_character(name=ronanda.message.author.nick)
        messages, embed = Form(
            EnumCommand.INCIDENT,
            ronanda.message.content,
            seal=Seal.LSPD,
            character=character
        ).generate()
        await ronanda.answer(":printer:")
        for message in messages:
            await ronanda.message.channel.send("```{}```".format(message))
        await ronanda.message.channel.send(embed=embed)
