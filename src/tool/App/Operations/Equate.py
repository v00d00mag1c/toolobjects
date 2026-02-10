from App.Executables.Act import Act
from Data.DictList import DictList
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Arguments.Objects.Same import Same

class Equate(Act):
    def getArguments(self) -> ArgumentsDict:
        return ArgumentsDict.fromList([
            Same(
                name = 'link'
            ),
            Same(
                name = 'to'
            )
        ])

    async def implementation(self, i: ArgumentsDict) -> None:
        i.items['link'].current = i.get('to')
