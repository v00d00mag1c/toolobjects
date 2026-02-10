from App.Objects.Extractor import Extractor
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Argument import Argument
from App.Storage.StorageUnit import StorageUnit

class ByStorageUnit(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'storage_unit',
                by_id = True,
                orig = StorageUnit,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'list',
                by_id = True,
                orig = Collection
            ),
            Argument(
                name = 'make_thumbnail',
                default = False,
                orig = Boolean
            )
        ])

    async def _implementation(self, i):
        pass
