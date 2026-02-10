from App.Storage.StorageAdapter import StorageAdapter
from App.Storage.StorageUnit import StorageUnit
from pydantic import Field
from typing import Optional
from pathlib import Path
from App import app
import secrets
import shutil

class DoubleDividedHashDirs(StorageAdapter):
    protocol_name = 'double_divided_hash_dirs'
    storage_dir_name: str = Field(default = 'storage')
    directory: Optional[str] = Field(default = None)
    _path: str = None

    def _init_hook(self):
        if self.directory != None:
            self._path = Path(self.directory)
            if self._path.is_file() == True:
                self.log_error(f"storage item {self._storage_item.name}: path is file")
            if self._path.exists() == False:
                self._path.mkdir()
        else:
            dbs_dir = app.app.storage
            self._path = dbs_dir.joinpath(self._storage_item.name)
            self._path.mkdir(exist_ok=True)

        self.getStorageDir().mkdir(exist_ok=True)

    def pathFromHash(self, hash: str):
        _dir = self.getStorageDir()
        _upper = _dir.joinpath(hash[0:2])

        return _upper, _upper.joinpath(hash)

    def get_storage_unit(self) -> StorageUnit:
        _bytes = 32

        _item = StorageUnit()
        _item.hash = secrets.token_hex(_bytes)

        _paths = self.pathFromHash(_item.hash)
        _paths[0].mkdir(exist_ok = True)
        _paths[1].mkdir(exist_ok = True)

        _item._root_path = _paths[1]

        return _item

    def copy_storage_unit(self, unit: StorageUnit, change_common: bool = True):
        _hash = self.pathFromHash(unit.hash)
        _hash[0].mkdir(exist_ok = True)
        _hash[1].mkdir(exist_ok = True)

        try:
            unit.copySelf(_hash[1])

            if change_common == True:
                unit._root_path = _hash[1]
        except AssertionError as e:
            pass
        except Exception as e:
            unit.log_error(e, exception_prefix = 'Error when moving storage unit: ')
            pass

    def _check_name(self):
        assert self._storage_item.name == 'tmp' and self.getStorageDir().relative_to(app.app.storage) != None, "clear it manually"

    def clear(self, recreate: bool = True):
        self._check_name()

        shutil.rmtree(self.getStorageDir())

        if recreate == True:
            self.getStorageDir().mkdir(exist_ok = True)

    def destroy(self):
        if self._storage_item.is_export == False:
            self._check_name()

        shutil.rmtree(self.getDir())

    def getStorageDir(self):
        return self._path.joinpath(self.storage_dir_name)

    def getDir(self):
        return self._path

    def get_all_files(self):
        for file in self.getDir().rglob("*"):
            yield file

    def get_relative_path(self, path: Path):
        return path.relative_to(self.getDir())
