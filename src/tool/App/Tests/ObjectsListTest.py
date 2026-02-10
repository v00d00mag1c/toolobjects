from App.Objects.Test import Test
from App.Storage.StorageItem import StorageItem
from Data.Random.GetRandomInt import GetRandomInt
from App.Objects.Responses.ObjectsList import ObjectsList
from App import app

class ObjectsListTest(Test):
    async def implementation(self, i):
        _store = StorageItem(
            name = 'objs',
            db_type = 'objects_list',
            db = {
                'file': str(app.app.storage.joinpath('crazy.json')),
                'auto_commit': False
            }
        )
        _store._init_hook()

        _vals = ObjectsList(items = [])
        for item in range(0, 200):
            _vals.join(await GetRandomInt().execute({'min': 0, 'max': max(item - 1, 1)}))

        _i = 0
        for item in _vals.getItems():
            item.flush(_store)

            if _i > 2:
                _vals.items[_i - 1].link(item)

            _i += 1

        _store.adapter.commit()

        return _vals
