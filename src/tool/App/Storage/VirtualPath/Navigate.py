from App.Objects.Executable import Executable
from App.Arguments.Types.String import String
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Arguments.ArgumentDict import ArgumentDict

from App.Storage.VirtualPath.Path import Path as VirtualPath

class Navigate(Executable):
    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            String(
                name = 'path',
                assertions = [NotNoneAssertion()]
            )
        ])

    async def implementation(self, i):
        path = VirtualPath.fromStr(i.get('path'))

        return path.getContent()
