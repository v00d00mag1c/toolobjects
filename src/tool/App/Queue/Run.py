from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from .Item import Item
from .OutputItem import OutputItem
from .Queue import Queue
from App.Responses.Response import Response

class Run(Act):
    '''
    Queue's entrypoint
    '''

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items=[
            Argument(
                name = 'prestart',
                is_multiple = True,
                orig = Item
            ),
            Argument(
                name = 'items',
                is_multiple = True,
                orig = Item
            ),
            Argument(
                name = 'output',
                is_multiple = True,
                orig = OutputItem
            )
        ])

    async def implementation(self, i):
        queue = Queue()
        queue.output = i.get('output')

        await queue.run(i.get('prestart'), i.get('items'))

        return queue.getOutput()
