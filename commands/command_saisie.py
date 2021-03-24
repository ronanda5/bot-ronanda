from commands.command import Command, EnumCommand
from forms.form import Form


class CommandSaisie(Command):

    async def process(self, ronanda):
        character = ronanda.db.get_character(name=ronanda.message.author.nick)
        messages, embed = Form(
            EnumCommand.SEIZURE,
            ronanda.message.content,
            character=character
        ).generate()
        await ronanda.answer(":printer:")
        for message in messages:
            await ronanda.message.channel.send("```{}```".format(message))
        await ronanda.message.channel.send(embed=embed)
