from App.Objects.Act import Act
from App.Storage.Item.StorageItem import StorageItem
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.Boolean import Boolean
from App import app

class Mount(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'item',
                orig = StorageItem,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'to_config',
                orig = Boolean,
                default = True
            )
        ])

    async def _implementation(self, i):
        _item = i.get('item')
        _check_storage = app.Storage.get(_item.name)

        assert _check_storage == None, 'storage item with this name is already mounted'

        app.Storage.append(_item)

        if i.get('to_config'):
            _conf_val = app.Config.getItem().get('storage.items', raw = True)
            if _conf_val == None:
                _conf_val = []
            _conf_val.append(_item.to_minimal_json())
            app.Config.getItem().set('storage.items', _conf_val)
