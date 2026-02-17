from App.Objects.Act import Act
from App.Storage.Item.StorageItem import StorageItem
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.String import String
from Data.Types.Boolean import Boolean
from App import app

class Unmount(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'name',
                orig = String,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'to_config',
                orig = Boolean,
                default = True
            )
        ])

    async def _implementation(self, i):
        name = i.get('name')
        item = app.Storage.get(name)

        assert item != None, 'not found storage with name {0}'.format(name)

        app.Storage.remove(item)

        if i.get('to_config'):
            _conf_val = app.Config.getItem().get('storage.items', raw = True)
            if _conf_val == None or type(_conf_val) != list:
                _conf_val = []

            new_vals = list()
            for item in _conf_val:
                if item.get('name') == name:
                    continue

                new_vals.append(item)

            app.Config.getItem().set('storage.items', new_vals)
