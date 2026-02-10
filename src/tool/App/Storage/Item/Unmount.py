from App.Objects.Act import Act
from App.Storage.Item.StorageItem import StorageItem
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.String import String
from App import app

class Unmount(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'name',
                orig = String,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        name = i.get('name')
        item = app.Storage.get(name)

        assert item != None, 'not found storage with name {0}'.format(name)

        app.Storage.remove(item)
