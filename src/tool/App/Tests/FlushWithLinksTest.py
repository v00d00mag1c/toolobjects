from App.Objects.Test import Test
from Data.Text.Text import Text
from App import app

class FlushWithLinksTest(Test):
    async def implementation(self, i):
        items = [Text(value='123456'),Text(value='asdfghjkl')]
        lnk = self.log('linking test')
        for item in items:
            lnk.link(item)

        self.log('flushingg to dbb')
        _storage = app.Storage.get('content')
        _item = lnk.flush(_storage)

        self.log_raw(lnk.getLinkedItems())
