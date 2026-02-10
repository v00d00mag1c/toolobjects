from App.Objects.Test import Test
from Media.Images.Image import Image
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Storage.StorageUnitLink import StorageUnitLink
from App import app
from Data.JSON import JSON

class StorageLinkTest(Test):
    async def _implementation(self, i):
        storage = app.Storage.get('content')
        '''

        _url = ""
        _unit = storage.get_storage_adapter().get_storage_unit()

        item = app.DownloadManager.addURL(_url, _unit, 'image.png')
        await item.start()

        _img = Image()
        _lnk = _img.link(_unit)
        _img.storage_unit = StorageUnitLink(
            path = 'image.png',
            insertion = _lnk.toInsert()
        )

        _img.flush(storage)
        '''

        _item = storage.get_db_adapter().ObjectAdapter.getById(7410302706075697152)

        _json = JSON(data = _item.toPython().to_json(only_class_fields = False))

        self.log_raw(_json.dump(indent = 4))
        return ObjectsList(items = [_item.toPython()])
