from App.Objects.Object import Object
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Storage.Item.StorageItem import StorageItem
from pydantic import Field
from typing import Generator
from Data.Int import Int
from App import app

class Storage(Object):
    '''
    Object that contains StorageItem's
    '''

    items: list[StorageItem] = Field(default = [])
    default_names: list[str] = Field(default = [])

    @classmethod
    def mount(cls):
        storage = cls()

        app.mount('Storage', storage)

    def init_hook(self):
        _names = []
        #dbs_dir = app.app.storage.joinpath('dbs')
        #dbs_dir.mkdir(exist_ok=True)

        for item in self.getOption('storage.items'):
            try:
                if item.unused == True:
                    self.log('storage item {0} is disabled'.format(item.name), role = ['storage.item.loading'])
                    continue

                _names.append(item.name)

                item._init_hook()
                self.append(item)
                self.log('loaded custom storage item {0}'.format(item.name), role = ['storage.item.loading'])
            except Exception as e:
                self.log_error(e)

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
                    'content': ':memory:',
                    'check_same_thread': False
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
                allowed_objects = ['App.ACL.User', 'App.ACL.Tokens.Token', 'App.ACL.Permissions.Permission'],
                db = {}
            )
        ]

        for item in default_items:
            try:
                self.default_names.append(item.name)
                if item.name not in _names:
                    item._init_hook()
                    self.append(item)
            except Exception as e:
                self.log_error(e)

    def append(self, item: StorageItem):
        self.log('Mounted {0}'.format(item.name), role = ['storage.item.mount'])

        self.items.append(item)

    def remove(self, item: StorageItem):
        if item in self.items and item.name not in self.default_names:
            self.items.remove(item)

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
