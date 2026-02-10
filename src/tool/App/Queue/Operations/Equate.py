from App.Objects.Act import Act
from App.Objects.Misc.DictList import DictList
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument

class Equate(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items=[
            Argument(
                name = 'equate_this',
                orig = None
            ),
            Argument(
                name = 'to',
                orig = None
            )
        ])

    async def implementation(self, i) -> None:
        i.values['equate_this'].current = i.get('to')
