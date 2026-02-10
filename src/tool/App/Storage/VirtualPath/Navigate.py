from App.Objects.Executable import Executable
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.String import String

from App.Storage.VirtualPath.Path import Path as VirtualPath

class Navigate(Executable):
    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'path',
                assertions = [NotNoneAssertion()],
                orig = String
            )
        ])

    async def implementation(self, i):
        path = VirtualPath.fromStr(i.get('path'))

        return path.getContent()
