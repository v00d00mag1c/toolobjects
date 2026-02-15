from App.Objects.Act import Act
from App.Objects.Object import Object
from App.Storage.StorageUnit import StorageUnit
from App.Storage.StorageUnitLink import StorageUnitLink
from Media.Files.File import File
from Web.URL import URL
from pydantic import Field

class FileType(Object):
    file: File = Field(default = None)
    storage_unit: StorageUnitLink = Field(default = None)

    def get_any(self):
        if self.file != None:
            return self.file

        if self.storage_unit != None:
            self.storage_unit.setDb(self.getDb())
            return self.storage_unit

    def get_file(self, follow_path: bool = False):
        if self.file != None:
            return self.file

        if self.storage_unit != None:
            # ???
            self.storage_unit.setDb(self.getDb())

            if follow_path:
                return self.storage_unit.get_file()
            else:
                return self.storage_unit.get_storage_unit().toFile()

    def move(self, new: Object):
        '''
        Copies "file" fields to this object
        '''

        if new.file != None:
            self.file = new.file.model_copy()

        if new.storage_unit != None:
            self.storage_unit = new.storage_unit.model_copy()

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

    def getPath(self):
        _s = self.get_file()
        if _s != None:
            return _s.getPath()

        return _s

    def get_url(self, from_server: bool = False) -> str:
        if from_server == False:
            return self.getPath()
        else:
            _f = None
            if self.storage_unit != None:
                self.storage_unit.setDb(self.getDb())
                _f = self.storage_unit.get_storage_unit()

            if _f != None:
                return _f.get_url() + self.storage_unit.path

        _common_source = self.obj.get_common_source()
        if _common_source == None or _common_source.obj.isInstance(URL) == False:
            return None

        return _common_source.obj.value

    def _display_as_string(self):
        return str(self.get_url())
