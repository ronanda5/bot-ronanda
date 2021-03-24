from command import Command


class CommandTufumes(Command):
    def __init__(self):
        super().__init__()
        self.required = []

    async def process(self, ronanda, server):
        await ronanda.answer("Ah Batard tu fumes ? https://www.youtube.com/watch?v=3FTqjyDa4AI")
