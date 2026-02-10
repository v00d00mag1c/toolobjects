from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Storage.Item.StorageItem import StorageItem

class Clear(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'storage',
                default = 'tmp',
                orig = StorageItem
            )
        ])

    async def _implementation(self, i):
        _storage = i.get('storage')
        _storage.storage_adapter.clear()
