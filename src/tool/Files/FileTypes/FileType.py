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
