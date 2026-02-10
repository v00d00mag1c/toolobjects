from App.Objects.Test import Test
from App import app

class DownloadTest(Test):
    async def implementation(self, i):
        storage = app.Storage.get('tmp')
        _url = "https://i.ibb.co/4gZHtNKL/image.png"
        _unit = storage.getStorageUnit()

        item = app.DownloadManager.addURL(_url, _unit, 'image.png')
        await item.start()
