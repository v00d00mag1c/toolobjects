from App.Objects.Extractor import Extractor
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Storage.StorageUnit import StorageUnit

class ByStorageUnit(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'object',
                orig = Object,
                assertions = [NotNone()]
            ),
            ListArgument(
                name = 'storage_unit',
                by_id = True,
                orig = StorageUnit,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        for storage_unit in i.get('storage_unit'):
            if storage_unit == None:
                self.log_error('missing storage_unit')

                continue

            _new = i.get('object').detect_from_su(storage_unit)()
            _new.set_storage_unit(storage_unit)
            _new.save()

            self.append(_new)
