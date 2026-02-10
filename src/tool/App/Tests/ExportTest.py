from App.Objects.Test import Test
from App.Storage.StorageItem import StorageItem
from App import app
from App.Tests.ContentLinksTest import ContentLinksTest

class ExportTest(Test):
    async def implementation(self, i):
        new_storage = StorageItem(
            name = 'tmpstorage',
            directory = str(app.app.storage.joinpath('tmpstrg')),
            db = {
                'adapter': 'sqlite'
            }
        )
        _links = await ContentLinksTest().execute({})

        for item in _links.getItems():
            item.flush(new_storage)

            self.log_raw(item)
