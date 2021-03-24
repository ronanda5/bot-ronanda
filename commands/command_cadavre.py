from commands.command import Command, EnumCommand
from forms.form import Form
from seal import Seal


class CommandCadavre(Command):

    async def process(self, ronanda):
        character = ronanda.db.get_character(name=ronanda.message.author.nick)
        messages, embed = Form(
            EnumCommand.CORPSE,
            ronanda.message.content,
            seal=Seal.CORONER,
            character=character
        ).generate()
        await ronanda.answer(":printer:")
        for message in messages:
            await ronanda.message.channel.send("```{}```".format(message))
        await ronanda.message.channel.send(embed=embed)
