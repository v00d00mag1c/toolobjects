from App.Objects.Object import Object
from App.Storage.StorageUnit import StorageUnit
from App.Storage.StorageUnitLink import StorageUnitLink
from Files.File import File
from pydantic import Field

class FileType(Object):
    file: File = Field(default = None)
    storage_unit: StorageUnitLink = Field(default = None)

    def getFile(self):
        if self.file != None:
            return self.file

        if self.storage_unit != None:
            return self.storage_unit

    def set_storage_unit(self, storage_unit: StorageUnit):
        if storage_unit.isIndexed() == False:
            storage_unit.save()

        _lnk = self.link(storage_unit)

        self.storage_unit = StorageUnitLink(
            path = storage_unit.guessName(),
            insertion = _lnk.toInsert()
        )
