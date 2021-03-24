from command import Command
from gtaw.form import Form
from seal import Seal


class CommandIncident(Command):

    async def _process_gtaw(self, ronanda):
        messages, embed = Form(
            "incident",
            ronanda.message.content,
            seal=Seal.LSPD,
            officer=ronanda.message.author.nick
        ).generate()
        await ronanda.answer(":printer:")
        for message in messages:
            await ronanda.message.channel.send("```{}```".format(message))
        await ronanda.message.channel.send(embed=embed)
