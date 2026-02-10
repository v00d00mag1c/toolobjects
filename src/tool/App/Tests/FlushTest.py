from App.Tests.Test import Test
from Data.Text import Text
from App import app

class FlushTest(Test):
    async def implementation(self, i):
        self.log('creating models')

        items = [Text(text='123456'),Text(text='asdfghjkl')]

        print(items)

        _storage = app.Storage.get('content')
        _db = _storage.db
        _db.connection.passObject(items[0])
