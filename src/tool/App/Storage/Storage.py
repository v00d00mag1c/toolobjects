from App.Objects.Object import Object
from App.Arguments.Objects.Orig import Orig
from App.Storage.StorageItem import StorageItem
from pydantic import Field
from App import app

class StorageArgument(Orig):
    def constructor(self):
        def _on_string(val: str):
            return app.Storage.get(val)

        super().constructor()

        self.orig = StorageItem
        self.on_string = _on_string
        self.on_string_format = '{name}'

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
