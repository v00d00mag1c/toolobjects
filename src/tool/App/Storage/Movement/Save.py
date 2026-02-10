from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Responses.AnyResponse import AnyResponse
from App.Storage.StorageItem import StorageItem
from App.Storage.StorageUUID import StorageUUID
from Data.Int import Int
from Data.Boolean import Boolean
from App import app

class Save(Act):
    '''
    Saves entries to StorageItem by name
    '''

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'items',
                orig = ObjectsList
            ),
            ListArgument(
                name = 'storage',
                assertions = [NotNoneAssertion()],
                orig = StorageItem
            ),
            ListArgument(
                name = 'link_to',
                orig = StorageUUID
            ),
            Argument(
                name = 'link_max_depth',
                orig = Int,
                default = cls.getOption('app.db.linking.depth.default')
            ),
            Argument(
                name = 'ignore_flush_hooks',
                default = False,
                orig = Boolean
            )
        ])

    async def implementation(self, i):
        results = 0
        link_to = list()
        for item in i.get('link_to'):
            link_to.append(item.toPython())

        _i = 0
        for storage in i.get('storage'):
            _storage_name = i.getCompare('storage').inputs[_i]
            assert storage != None, f"storage {_storage_name} not found"
            assert storage.has_db_adapter(), f"storage {storage.name} does not contains db connection"

            for item in i.get('items').getItems():
                item.flush(storage, link_max_depth = i.get('link_max_depth'), ignore_flush_hooks = i.get('ignore_flush_hooks'))

                self.log(f"flushed item to db {storage.name}, uuid: {item.getDbId()}")
                results += 1

                for link_item in link_to:
                    link_item.link(item)

                    self.log(f"saving: linked {item.getDbId()} to {link_item.getDbId()}")

            if storage.adapter.auto_commit == False:
                self.log('{0}: commit'.format(_storage_name))
                storage.adapter.commit()

            _i += 1

        return AnyResponse(data = results)
