from App.Objects.Test import Test
from App import app
from App.Storage.Movement.Export import Export
from App.Responses.ObjectsList import ObjectsList
from App.Storage.StorageItem import StorageItem
from Data.Text import Text

class ExportTest(Test):
    async def implementation(self, i):
        return await Export().execute({
            'items': ObjectsList(items = [
                Text(text = ';/'),
                Text(text = ';)'),
                Text(text = ';()'),
                self.log(';;( ;;)')
            ]),
            'dir': str(app.app.storage.joinpath('tmpstrg')),
        })
