from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from Data.Int import Int
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Responses.ObjectsList import ObjectsList
from App.Responses.AnyResponse import AnyResponse
from App.Storage.StorageItem import StorageItem
from App import app

class Save(Act):
    '''
    Saves entries to StorageItem by name
    '''

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'items',
                orig = ObjectsList
            ),
            ListArgument(
                name = 'storage',
                assertions = [NotNoneAssertion()],
                orig = StorageItem
            ),
            Argument(
                name = 'link_to',
                orig = Int
            ),
            Argument(
                name = 'link_max_depth',
                orig = Int,
                default = 10 # TODO move to const
            )
        ])

    async def implementation(self, i):
        results = 0

        for storage in i.get('storage'):
            link_to = i.get('link_to')

            assert storage != None, f"storage {storage.name} not found"
            assert storage.hasAdapter(), f"storage {storage.name} does not contains db connection"

            for item in i.get('items').getItems():
                item.flush(storage,
                        link_max_depth = i.get('link_max_depth'))

                self.log(f"flushed item to db {storage.name}, uuid: {item.getDbId()}")
                results += 1

        return AnyResponse(data = results)
