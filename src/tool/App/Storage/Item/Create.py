from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Storage.Item.StorageItem import StorageItem
from App.Storage.Item.Mount import Mount
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.Types.String import String
from Data.Types.Boolean import Boolean
from Data.Types.Dict import Dict

from App.Storage.Item.CreateRoot import CreateRoot
from App import app

class Create(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'name',
                orig = String,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'dir',
                orig = String
            ),
            Argument(
                name = 'mount',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'db_args',
                orig = Dict,
                default = {
                    'auto_commit': True
                }
            ),
            Argument(
                name = 'create_root',
                orig = Boolean,
                default = True
            )
        ])

    async def _implementation(self, i):
        assert app.Storage.get(i.get('name')) == None, 'storage item with this name already exists'

        new = StorageItem(
            name = i.get('name'),
            db_type = 'App.DB.Adapters.SQLite',
            storage = {
                'directory': i.get('dir')
            },
            db = i.get('db_args')
        )
        new._init_hook()

        if i.get('mount') == True:
            await Mount().execute({
                'item': new
            })

        if i.get('create_root') == True:
            await CreateRoot().execute({
                'item': new
            })

        return ObjectsList(items = [new], unsaveable = True, supposed_to_be_single = True)
