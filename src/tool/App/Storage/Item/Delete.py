from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Storage.Item.StorageItem import StorageItem
from App import app

class Delete(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'storage',
                orig = StorageItem,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        storage = i.get('storage')
        storage.is_export = True

        storage.delete()

        #app.Storage.remove(storage)
