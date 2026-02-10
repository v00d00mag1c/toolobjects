from App.Executables.Act import Act
from App.Data.DictList import DictList
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Arguments.Objects.Same import Same

class Equate(Act):
    @classmethod
    def getArguments(cls) -> ArgumentsDict:
        return ArgumentsDict.fromList([
            Same(
                name = 'equate_this'
            ),
            Same(
                name = 'to'
            )
        ])

    async def implementation(self, i: ArgumentsDict) -> None:
        i.items['equate_this'].current = i.get('to')
