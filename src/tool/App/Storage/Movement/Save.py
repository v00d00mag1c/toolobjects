from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Responses.AnyResponse import AnyResponse
from App.Storage.StorageItem import StorageItem
from App.Storage.StorageUUID import StorageUUID
from Data.Int import Int
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
            ListArgument(
                name = 'link_to',
                orig = StorageUUID
            ),
            Argument(
                name = 'link_max_depth',
                orig = Int,
                default = cls.getOption('app.db.linking.depth.default')
            )
        ])

    async def implementation(self, i):
        results = 0
        link_to = list()
        for item in i.get('link_to'):
            link_to.append(item.toPython())

        for storage in i.get('storage'):
            assert storage != None, "storage not founb" #f"storage {storage.name} not found"
            assert storage.hasAdapter(), f"storage {storage.name} does not contains db connection"

            for item in i.get('items').getItems():
                item.flush(storage, link_max_depth = i.get('link_max_depth'))

                self.log(f"flushed item to db {storage.name}, uuid: {item.getDbId()}")
                results += 1

                for link_item in link_to:
                    link_item.link(item)

                    self.log(f"saving: linked {item.getDbId()} to {link_item.getDbId()}")

        return AnyResponse(data = results)
