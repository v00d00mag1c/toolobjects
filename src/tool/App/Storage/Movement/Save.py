from App.Objects.Act import Act
from App.Arguments.ArgumentDict import ArgumentDict
from App.Arguments.Objects.Orig import Orig
from App.Arguments.Types.Int import Int
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Responses.ObjectsList import ObjectsList
from App.Responses.AnyResponse import AnyResponse
from App.Storage.Storage import StorageArgument
from App import app

class Save(Act):
    '''
    Saves entries to StorageItem by name
    '''

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Orig(
                name = 'items',
                orig = ObjectsList
            ),
            # Storage name
            StorageArgument(
                name = 'storage',
                assertions = [NotNoneAssertion()],
            ),
            Int(
                name = 'link_max_depth',
                default = 10 # TODO move to const
            )
        ])

    async def implementation(self, i):
        results = 0
        storage = i.get('storage')

        assert storage != None, f"storage {storage.name} not found"
        assert storage.hasAdapter(), f"storage {storage.name} does not contains db connection"

        for item in i.get('items').getItems():
            item.flush(storage,
                       link_max_depth = i.get('link_max_depth'))

            self.log(f"flushed item to db {storage.name}, uuid: {item.getDbId()}")
            results += 1

        return AnyResponse(data = results)
