class Command:
    def __init__(self, server_required=True):
        self.server_required = server_required

    async def process(self, ronanda, server):
        if self.server_required and server is None:
            await ronanda.answer("Sélectionnez le serveur sur lequel vous jouez en tapant "
                                 "`#serveur gtaw` ou `#serveur lrp`.")
            return
        if not self.server_required or server == 'lrp':
            await self._process(ronanda)
        elif server == 'gtaw':
            await self._process_gtaw(ronanda)
        if self.server_required:
            await ronanda.increment_user_stats(ronanda.message.author)

    async def _process(self, ronanda):
        await ronanda.answer("Cette commande n'est pas disponible pour le serveur LRP."
                             "\nSi vous pensez qu'il s'agit d'une erreur, faites le savoir.")

    async def _process_gtaw(self, ronanda):
        await ronanda.answer("Cette commande n'est pas disponible pour le serveur GTAW."
                             "\nSi vous pensez qu'il s'agit d'une erreur, faites le savoir.")
