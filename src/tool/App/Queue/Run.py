from App.Executables.Act import Act
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Arguments.Objects.List import List
from Data.DictList import DictList
from .Item import Item
from .Queue import Queue

class Run(Act):
    @classmethod
    def getArguments(cls) -> ArgumentsDict:
        return ArgumentsDict.fromList([
            List(
                name = 'prestart',
                orig = Item
            ),
            List(
                name = 'items',
                orig = Item
            ),
            List(
                name = 'output',
                orig = Item
            )
        ])

    async def implementation(self, i: ArgumentsDict):
        prestart = i.get('prestart')
        items = i.get('items')
        output = i.get('output')

        queue = Queue(output = output)
        iterator = 0
        for i in range(0, len(prestart)):
            item = items[i]
            predicate = item.getPredicate()
            arguments = item.getArguments()

            item.execute()

        for i in range(0, len(items)):
            item = items[i]
            predicate = item.getPredicate()
            arguments = item.getArguments()

            item.execute()

        return queue.getOutput()
