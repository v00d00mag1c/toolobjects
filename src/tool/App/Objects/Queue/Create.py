from App.Objects.Extractor import Extractor
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Types.Dict import Dict
from App.Objects.Queue.Queue import Queue

class Create(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'prestart',
                orig = Dict,
            ),
            Argument(
                name = 'items',
                orig = Dict,
            ),
            Argument(
                name = 'output',
                orig = Dict,
            )
        ])

    def _implementation(self, i):
        item = Queue()
        item.prestart = i.get('prestart')
        item.items = i.get('items')
        item.output = i.get('output')

        self.append(item)
