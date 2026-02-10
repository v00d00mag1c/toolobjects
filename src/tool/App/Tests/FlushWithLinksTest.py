from App.Objects.Test import Test
from Data.Text import Text
from App import app

class FlushWithLinksTest(Test):
    async def implementation(self, i):
        items = [Text(text='123456'),Text(text='asdfghjkl')]
        lnk = self.log('linking test')
        for item in items:
            lnk.link(item)

        self.log('flushingg to dbb')
        _storage = app.Storage.get('content')
        _item = _storage.adapter.flush(lnk)

        print(lnk.getLinkedItems())
