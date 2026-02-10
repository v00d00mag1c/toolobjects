from App.Objects.Act import Act
from App.Objects.Object import Object
from App.Storage.StorageUnit import StorageUnit
from App.Storage.StorageUnitLink import StorageUnitLink
from App.Objects.Displayment import Displayment
from Files.File import File
from Web.URL import URL
from pydantic import Field

class FileType(Object):
    file: File = Field(default = None)
    storage_unit: StorageUnitLink = Field(default = None)

    def get_file(self):
        if self.file != None:
            return self.file

        if self.storage_unit != None:
            return self.storage_unit.getStorageUnit().toFile()

    def move(self, new: Object):
        if new.file != None:
            self.file = new.file

        if new.storage_unit != None:
            self.storage_unit = new.storage_unit

    def set_insertion_name(self, name: str):
        if self.storage_unit != None:
            self.storage_unit.path = name

    def set_storage_unit(self, storage_unit: StorageUnit):
        if storage_unit.isIndexed() == False:
            storage_unit.save()

        _lnk = self.link(storage_unit)

        self.storage_unit = StorageUnitLink(
            path = storage_unit.guessName(),
            insertion = _lnk.toInsert()
        )

    def get_url(self) -> str:
        _file = self.get_file()
        if _file != None:
            return _file.getPath()

        _common_source = self.obj.get_common_source()
        if _common_source == None or _common_source.obj.isInstance(URL) == False:
            return None

        return _common_source.obj.value

    @classmethod
    def _displayments(cls):
        class DisplayAsString(Act):
            def implementation(self, i):
                orig = i.get('orig')
                return str(orig.get_url())

        return [Displayment(
            role = ['str'],
            value = DisplayAsString
        )]
