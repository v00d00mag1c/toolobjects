from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Storage.Item.StorageItem import StorageItem
from App.Storage.Item.Mount import Mount
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.Types.String import String
from Data.Types.Boolean import Boolean

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
                default = False
            )
        ])

    async def _implementation(self, i):
        news = StorageItem(
            name = i.get('name'),
            db_type = 'App.DB.Adapters.SQLite',
            storage = {
                'directory': i.get('dir')
            },
            db = {
                'auto_commit': True
            }
        )
        news._init_hook()

        if i.get('mount') == True:
            await Mount().execute({
                'item': news
            })

        return ObjectsList(items = [news], unsaveable = True, supposed_to_be_single = True)
