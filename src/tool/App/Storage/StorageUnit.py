from App.Objects.Object import Object
from Files.File import File
from pydantic import Field
from pathlib import Path
from typing import Type, Generator
import shutil

class StorageUnit(Object):
    '''
    Also represents storage dir, but contains files info
    it relies on current db path and doesnt know it folder
    '''
    hash: str = Field(default = None)
    files: list[File] = Field(default = [])
    name: str = Field(default = None)
    ext: str = Field(default = None)
    common: str = Field(default = None)
    _common_path: str = None

    def _constructor(self):
        self.getUpper().mkdir(exist_ok=True)
        self.getDir().mkdir(exist_ok=True)

    def getCommonPath(self):
        if self._common_path == None:
            assert self.hasDb(), 'storage unit does not contains _common_path and db ref'

            _storage = self.getDb()._adapter._storage_item
            
            return _storage.getStorageDir()

        return self._common_path

    def getUpper(self):
        return Path(self.getCommonPath()).joinpath(self.hash[0:2])

    def getDir(self):
        return self.getUpper().joinpath(self.hash)

    def fromDir(self, common_path: Path, hash: str):
        self.hash = hash
        self._common_path = common_path

    def setCommonFile(self, file_path: Path):
        '''
        Sets relative file as common
        '''

        self.name = file_path.name
        self.ext = file_path.suffix[1:]
        self.common = str(file_path.relative_to(self.getDir()))

    def genFilesList(self) -> Generator[File]:
        dirs = self.getDir()

        for file in self.getDir().rglob('*'):
            if file.is_file():
                _item = File(
                    name = file.name,
                    ext = file.suffix[1:],
                    size = file.stat().st_size,
                    path = str(file.relative_to(dirs)),
                )

                yield _item

    def flush_hook(self, into: Type): # StorageItem cant be annotated anywhere :(
        _upper = into.getStorageDir().joinpath(self.hash[0:2])
        _upper.mkdir(exist_ok = True)
        _hash = _upper.joinpath(self.hash)
        _hash.mkdir(exist_ok = True)

        try:
            self.copySelf(_hash)
        except AssertionError:
            pass

    def copySelf(self, new_path: Path):
        assert str(self.getDir()) != str(new_path), 'its already here'

        shutil.copytree(str(self.getDir()), str(new_path), dirs_exist_ok = True)
        self.log(f"copied storageunit from {str(self.getDir())} to {str(new_path)}")
