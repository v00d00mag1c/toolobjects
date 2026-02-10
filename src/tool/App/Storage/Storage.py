from App.Objects.Object import Object
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Storage.StorageItem import StorageItem
from pydantic import Field
from typing import Generator
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

    def init_hook(self):
        _names = []
        #dbs_dir = app.app.storage.joinpath('dbs')
        #dbs_dir.mkdir(exist_ok=True)

        for item in self.getOption('storage.items'):
            _names.append(item.name)

            item._init_hook()
            self.append(item)

        default_items = [
            StorageItem(
                name = 'common',
                db_type = 'App.DB.Adapters.SQLite',
                db = {}
            ),
            StorageItem(
                name = 'tmp',
                db_type = 'App.DB.Adapters.SQLite',
                db = {
                    'content': ':memory:'
                }
            ),
            StorageItem(
                name = 'logs',
                allowed_objects = ['App.Logger.Log'],
                db_type = 'App.DB.Adapters.SQLite',
                db = {}
            ),
            StorageItem(
                name = 'bin',
                db_type = 'App.DB.Adapters.SQLite',
                db = {}
            ),
            StorageItem(
                name = 'users',
                db_type = 'App.DB.Adapters.SQLite',
                allowed_objects = ['App.ACL.User', 'App.ACL.Permissions.Permission'],
                db = {}
            )
        ]

        for item in default_items:
            if item.name not in _names:
                item._init_hook()
                self.append(item)

    def append(self, item: StorageItem):
        self.items.append(item)

    def getAll(self) -> Generator[StorageItem]:
        for item in self.items:
            yield item

    def get(self, name: str) -> StorageItem:
        '''
        Gets StorageItem by name
        '''

        for item in self.items:
            if item.name == name:
                return item

    @classmethod
    def _settings(cls):
        return [
            ListArgument(
                name = 'storage.items',
                default = [],
                orig = StorageItem
            ),
            Argument(
                name = 'app.db.linking.depth.default',
                default = 29,
                orig = Int
            )
        ]
