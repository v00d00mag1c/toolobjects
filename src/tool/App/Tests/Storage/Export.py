from App.Objects.Test import Test
from App import app
from App.Storage.Movement.Export import Export as RealExport
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Storage.Item.StorageItem import StorageItem
from Media.Text.Text import Text

class Export(Test):
    async def _implementation(self, i):
        return await RealExport().execute({
            'items': ObjectsList(items = [
                Text(value = ';/'),
                Text(value = ';)'),
                Text(value = ';()'),
                self.log(';;( ;;)')
            ]),
            'dir': str(app.app.storage.joinpath('tmpstrg')),
        })
