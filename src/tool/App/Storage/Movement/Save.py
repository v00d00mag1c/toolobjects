from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Responses.AnyResponse import AnyResponse
from App.Storage.Item.StorageItem import StorageItem
from App.Storage.StorageUUID import StorageUUID
from Data.Types.Int import Int
from Data.Types.Boolean import Boolean
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
                assertions = [NotNone()],
                orig = StorageItem
            ),
            ListArgument(
                name = 'link_to',
                default = None,
                orig = StorageUUID
            ),
            Argument(
                name = 'link_max_depth',
                default = cls.getOption('app.db.linking.depth.default'),
                orig = Int,
            ),
            Argument(
                name = 'just_copy',
                orig = Boolean,
                default = False
            ),
            Argument(
                name = 'ignore_flush_hooks',
                default = False,
                orig = Boolean
            ),
            Argument(
                name = 'ignore_errors',
                default = True,
                orig = Boolean
            ),
            Argument(
                name = 'public',
                orig = Boolean,
                default = True
            ),
        ])

    async def _implementation(self, i):
        results = 0
        just_copy = i.get('just_copy')
        ignore_errors = i.get('ignore_errors')
        link_to = list()

        for item in i.get('link_to'):
            link_to.append(item.toPython())

        _i = 0
        for storage in i.get('storage'):
            _storage_name = i.getCompare('storage').inputs[_i]
            assert storage != None, f"storage {_storage_name} not found"
            assert storage.has_db_adapter(), f"storage {storage.name} does not contains db connection"

            try:
                for item in i.get('items').getItems():
                    if just_copy == False:
                        if i.get('public'):
                            item.local_obj.make_public()

                    item.flush(storage, link_max_depth = i.get('link_max_depth'), ignore_flush_hooks = i.get('ignore_flush_hooks'), ignore_errors = ignore_errors)
                    item.save(do_commit = False)

                    results += 1

                    for link_item in link_to:
                        if link_item != None:
                            link_item.link(item)

                            self.log(f"saving: linked {item.getDbId()} to {link_item.getDbId()}")
                        else:
                            self.log('link item doesnt exists')

                if storage.adapter.auto_commit == False:
                    #self.log('{0}: commit'.format(_storage_name))
                    storage.adapter.commit()

                _i += 1
            except Exception as e:
                if ignore_errors == False:
                    raise e

                self.log_error(e, exception_prefix = 'Error when saving to {0}: '.format(_storage_name))
