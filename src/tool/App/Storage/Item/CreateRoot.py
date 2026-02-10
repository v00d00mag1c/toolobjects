from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Storage.Item.StorageItem import StorageItem
from Data.Primitives.Collections.Collection import Collection
from App import app

class CreateRoot(Act):
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
        item = i.get('item')
        coll = Collection()
        coll.flush(item)
        coll.save()

        item.root_uuid = coll.getDbIds()

        # Updating config
        _conf_val = app.Config.getItem().get('storage.items', raw = True)
        if _conf_val == None:
            _conf_val = []
        for iterate in _conf_val:
            if iterate.get('name') == item.name:
                iterate['root_uuid'] = coll.getDbIds()

        app.Config.getItem().set('storage.items', _conf_val)
