from App.Objects.Object import Object
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Storage.StorageItem import StorageItem
from pydantic import Field
from Data.Int import Int
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
                name = 'common',
                db = {
                    'adapter': 'sqlite',
                }
            ),
            StorageItem(
                name = 'tmp',
                db = {
                    'adapter': 'sqlite',
                    'content': ':memory:'
                }
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
        '''
        Gets StorageItem by name
        '''

        for item in self.items:
            if item.name == name:
                return item

    @classmethod
    def getSettings(cls):
        return [
            ListArgument(
                name = 'storage.dbs',
                default = [],
                orig = StorageItem
            ),
            Argument(
                name = 'app.db.linking.depth.default',
                default = 29,
                orig = Int
            )
        ]
