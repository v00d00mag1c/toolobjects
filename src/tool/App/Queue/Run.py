from App.Executables.Act import Act
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Arguments.Objects.List import List
from App.Arguments.Objects.Orig import Orig
from App.Data.DictList import DictList
from .Item import Item
from .Queue import Queue

class Run(Act):
    '''
    Queue's entrypoint
    '''

    @classmethod
    def getArguments(cls) -> ArgumentsDict:
        return ArgumentsDict.fromList([
            List(
                name = 'prestart',
                orig = Orig(
                    name = 'prestart_item',
                    orig = Item
                )
            ),
            List(
                name = 'items',
                orig = Orig(
                    name = 'items_item',
                    orig = Item
                )
            ),
            List(
                name = 'output',
                orig = Orig(
                    name = 'output_item',
                    orig = Item
                )
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
            predicate = item.getPredicate(**item.getArguments())

            queue.prestart.append(predicate)

        for i in range(0, len(items)):
            item = items[i]
            predicate = item.getPredicate()
            arguments = item.getArguments()

            queue.items.append(item.execute())

        return queue.getOutput()
