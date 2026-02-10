from App.Objects.Object import Object
from App.Storage.StorageUnit import StorageUnit
from App.DB.DBConnection import DBConnection
from pydantic import Field
from pathlib import Path
from App import app
import secrets

class StorageItem(Object):
    '''
    Implements storage with DB and storageunits.

    Notice: path is taking literally and does not creates additional dirs.
    path=f:/dir, name='dir' will use dir f:/dir.

    If 'path' not passed, it will use storage/dbs/{name} dir
    '''

    name: str = Field()
    display_name: str = Field(default = None)
    directory: str = Field(default = None)
    db: DBConnection = Field(default = None)
    _path: str = None
    _storage_dir_name = 'storage'

    def constructor(self):
        if self.directory != None:
            self._path = Path(self.directory)
            if self._path.is_file() == True:
                self.log_error(f"storage item {self.name}: path is file")
            if self._path.exists() == False:
                self._path.mkdir()

        dbs_dir = app.app.storage.joinpath('dbs')
        self._path = dbs_dir.joinpath(self.name)
        self._path.mkdir(exist_ok=True)
        self.getStorageDir().mkdir(exist_ok=True)

    def getStorageDir(self):
        return self._path.joinpath(self._storage_dir_name)

    def getStorageUnit(self) -> StorageUnit:
        _bytes = 32
        _hash = secrets.token_hex(_bytes)
        _item = StorageUnit()
        _item.fromDir(self.getStorageDir(), _hash)
        _item._constructor()

        return _item
