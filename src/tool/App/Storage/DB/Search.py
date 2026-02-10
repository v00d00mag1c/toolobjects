from App.Objects.Act import Act
from App.Arguments.ArgumentDict import ArgumentDict
from App.Responses.ObjectsList import ObjectsList
from App.Storage.Storage import StorageArgument
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion

class Search(Act):
    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            StorageArgument(
                name = 'storage',
                assertions = [NotNoneAssertion()]
            ),
        ])

    async def implementation(self, i) -> ObjectsList:
        _objects = ObjectsList(items = [])

        return _objects
