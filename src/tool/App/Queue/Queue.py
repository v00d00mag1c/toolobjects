from App.Objects.Object import Object

class Queue(Object):
    '''
    Class that allows to run multiple executables with his context

    Uses App.Queue.Item for "prestart" and "items".

    prestart - Items that will be executed before the "items". You can pass variables there. Things that does not has "execute()"
    items - Items that will be executed as main process
    output - Queue output format

    The results will be stored at the variables "prestart" and "items".
    You can reference results by "$" for prestart and "#" for items
    '''
    prestart: list = []
    items: list = []
    output: list = []

    def convertArguments(self):
        pass

    def getOutput(self):
        pass

    async def run(self, prestart: list, items: list):
        for item in prestart:
            _item = item.getPredicate()
            self.prestart.append(_item(**item.getBuildArguments()))

        iterator = 0
        for item in items:
            item._queue = self
            item._id = iterator

            self.items.append(await item.run())

            iterator += 1
