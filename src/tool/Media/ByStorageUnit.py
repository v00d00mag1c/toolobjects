from App.Objects.Extractor import Extractor
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Argument import Argument
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
            Argument(
                name = 'storage_unit',
                by_id = True,
                orig = StorageUnit,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        _new = i.get('object')()
        _new.set_storage_unit(i.get('storage_unit'))

        self.append(_new)
