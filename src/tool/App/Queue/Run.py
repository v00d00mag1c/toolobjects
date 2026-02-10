from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from .Item import Item
from .OutputItem import OutputItem
from .Queue import Queue
from App.Objects.Responses.Response import Response

class Run(Act):
    '''
    Queue's entrypoint
    '''

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items=[
            ListArgument(
                name = 'prestart',
                orig = Item
            ),
            ListArgument(
                name = 'items',
                orig = Item
            ),
            ListArgument(
                name = 'output',
                orig = OutputItem
            )
        ])

    async def _implementation(self, i):
        queue = Queue()
        queue.output = i.get('output')

        await queue.run(i.get('prestart'), i.get('items'))

        return queue.getOutput()
