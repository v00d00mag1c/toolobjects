from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Storage.Item.StorageItem import StorageItem
from App import app

class MountToConfig(Act):
    '''
    Mounts StorageItem that was mounted in app, but not in config
    '''

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'item',
                orig = StorageItem,
                assertions = [NotNone()]
            )
        ])

    def _implementation(self, i):
        _item = i.get('item')
        _conf_name = 'storage.items'
        _conf_val = app.Config.getItem().get(_conf_name, raw = True)

        assert _conf_val != None and type(_conf_val) == list, 'invalid value'

        for item in _conf_val:
            assert item.get('name') != _item.name, "already in config"
            assert _item.name not in app.Storage.default_names, "already in config"

        _conf_val.append(_item.to_minimal_json())
        app.Config.getItem().set(_conf_name, _conf_val)
