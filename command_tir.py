from command import Command
from gtaw.form import Form
from seal import Seal


class CommandTir(Command):

    async def _process_gtaw(self, ronanda):
        messages, embed = Form(
            "tir",
            ronanda.message.content,
            seal=Seal.INTERNAL_AFFAIRS,
            officer=ronanda.message.author.nick
        ).generate()
        await ronanda.answer(":printer:")
        for message in messages:
            await ronanda.message.channel.send("```{}```".format(message))
        await ronanda.message.channel.send(embed=embed)
