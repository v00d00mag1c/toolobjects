from App.Objects.Object import Object
from App.Storage.StorageItem import StorageItem
from pydantic import Field
from App import app

class Storage(Object):
    '''
    Object that contains StorageItem's
    '''

    items: list[StorageItem] = Field(default = [])

    @classmethod
    def mount(cls):
        storage = cls()

        app.mount('Storage', storage)

    def constructor(self):
        dbs_dir = app.app.storage.joinpath('dbs')
        dbs_dir.mkdir(exist_ok=True)

        default_items = [
            StorageItem(
                name = 'content',
                db = {
                    'protocol': 'sqlite'
                }
            ),
            StorageItem(
                name = 'tmp'
            ),
            StorageItem(
                name = 'instance'
            )
        ]

        for item in default_items:
            self.append(item)

    def append(self, item: StorageItem):
        self.items.append(item)

    def get(self, name: str) -> StorageItem:
        for item in self.items:
            if item.name == name:
                return item

    @classmethod
    def getSettings(cls):
        from App.Arguments.Objects.List import List
        from App.Arguments.Objects.Orig import Orig

        return [
            List(
                name = 'storage.dbs',
                default = [],
                orig = Orig(
                    name = 'storage.dbs.db',
                    orig = StorageItem
                )
            )
        ]
