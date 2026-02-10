from App.Objects.Test import Test
from Data.Text import Text
from App.Storage.StorageUnit import StorageUnit
from App.Storage.StorageItem import StorageItem
from Data.JSON import JSON
from App import app
from App.Responses.ObjectsList import ObjectsList

class ContentLinksTest(Test):
    async def implementation(self, i):
        _storage: StorageItem = app.Storage.get('tmp')

        _text = Text(text = '7777')
        _another_obj = _storage.getStorageUnit()
        __name = _another_obj.getDir().joinpath('tmp.txt')
        _file = open(__name, 'w', encoding='utf-8')
        _file.write('94123821131255')
        _file.flush()
        _file.close()
        _another_obj.setCommonFile(__name)

        _got_link = _text.link(_another_obj)
        #_another_text.link(_text) pydantic protects us from recursion

        _another_obj.flush(_storage)
        self.log_raw(_got_link)
        self.log_raw(_got_link.item)
        _text.text = _got_link.toInsert([])

        #_json = JSON(data = _text.to_json())
        #_json_no_links = JSON(data = _text.to_json(convert_links = False))

        #self.log_error('with removed links:')
        #self.log_raw(_json.dump(indent = 4))
        #self.log_error('with links:')
        #self.log_raw(_json_no_links.dump(indent = 4))

        self.log_success('trying to flush this into db')

        _item = _text.flush(_storage)

        self.log_error('returning object')

        _json = JSON(data = _item.getObject().to_json(convert_links = 'unwrap'))

        self.log_raw(_json.dump(indent = 4))

        return ObjectsList.fromItems([_item.getObject()])
