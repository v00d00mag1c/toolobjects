from App.Objects.Object import Object
from Media.Files.File import File
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
    _root_path: str = None # Path

    def get_root(self):
        if self._root_path == None:
            assert self.hasDb(), 'storage unit does not contains _root_path and db ref'

            _storage = self.getDb()._adapter._storage_item

            return _storage.storage_adapter.pathFromHash(self.hash)[1]

        return self._root_path

    def set_root(self, path: str):
        self._root_path = str(path)

    def get_common_file(self) -> File:
        _common = Path(self.common)
        for item in self.files:
            if _common != None and item.getPath(self.get_root()) == _common:
                return item

    def getFiles(self) -> Generator[File]:
        for file in self.files:
            _file = file.model_copy()
            _file.path = self.getDir()
            yield _file

    def getFirstFile(self) -> File:
        return self.files[0]

    def getDir(self):
        return self.get_root()

    def get_url(self):
        _storage = self.getDb()._adapter._storage_item

        return '/storage/{0}/{1}/'.format(_storage.name, self.getDbId())

    def setCommonFile(self, file_path: Path):
        self.name = file_path.name
        self.ext = file_path.suffix[1:]
        self.common = str(file_path.relative_to(self.getDir()))

    def genFilesList(self) -> Generator[File]:
        for file in self.getDir().rglob('*'):
            if file.is_file():
                _item = File(
                    name = file.name,
                    ext = file.suffix[1:],
                    size = file.stat().st_size,
                    path = str(self.getRelativePath(file)),
                )

                yield _item

    def getRelativePath(self, path: Path):
        dirs = self.getDir()

        return path.relative_to(dirs)

    def flush_hook(self, into: Type):
        into.storage_adapter.copy_storage_unit(self)

    def copySelf(self, new_root: Path):
        assert str(self.getDir()) != str(new_root), 'its already here'

        shutil.copytree(str(self.getDir()), str(new_root), dirs_exist_ok = True, symlinks = True)
        #self.log(f"copied storageunit from {str(self.getDir())} to {str(new_root)}")
        self.log(f"copied storageunit to the new dir")

    def toFile(self) -> File:
        _common_file = self.get_common_file()
        if _common_file == None:
            _common_file = self.getFirstFile()
        if _common_file == None:
            return None

        #_common_file.path = str(self.getRelativePath())
        _common_file.path = str(self.getDir())
        _common_file.path_hidden = True

        return _common_file

    def guessName(self) -> str:
        _common = self.get_common_file()
        if _common != None:
            return _common.name

        _any = self.getFirstFile()
        if _any != None:
            return _any.name

    def isIndexed(self) -> bool:
        return len(self.files) > 0

    def save_hook(self):
        self.files = list(self.genFilesList())
