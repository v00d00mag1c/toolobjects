from App.Objects.Object import Object
from App.Storage.StorageUnit import StorageUnit
from App.Storage.DB.Adapters.ConnectionAdapter import ConnectionAdapter
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
    directory: str = Field(default = None)
    db: dict = Field(default = None)

    # display_name: str = Field(default = None)

    _storage_dir_name = 'storage'

    adapter: ConnectionAdapter = Field(default = None, exclude = True)
    _path: str = None

    def getDir(self):
        return self._path

    def getStorageDir(self):
        return self._path.joinpath(self._storage_dir_name)

    def getStorageUnit(self) -> StorageUnit:
        _bytes = 32
        _hash = secrets.token_hex(_bytes)
        _item = StorageUnit()
        _item.fromDir(self.getStorageDir(), _hash)
        _item._constructor()

        return _item

    def getAdapter(self):
        assert self.hasAdapter(), "storage item does not has db connection"

        return self.adapter

    def hasAdapter(self) -> bool:
        return self.adapter != None

    def constructor(self):
        self._initStorage()
        if self.db != None:
            self.adapter = self.getDBAdapterByName(self.db.get('adapter'))

    def _initStorage(self):
        if self.directory != None:
            self._path = Path(self.directory)
            if self._path.is_file() == True:
                self.log_error(f"storage item {self.name}: path is file")
            if self._path.exists() == False:
                self._path.mkdir()
        else:
            dbs_dir = app.app.storage.joinpath('dbs')
            self._path = dbs_dir.joinpath(self.name)
            self._path.mkdir(exist_ok=True)

        self.getStorageDir().mkdir(exist_ok=True)

    def getDBAdapterByName(self, adapter_name: str):
        for adapter in app.ObjectsList.getObjectsByGroup(['App', 'Storage', 'DB', 'Adapters', 'Connection']):
            _module = adapter.getModule()
            if _module.protocol_name == adapter_name:
                item = _module(**self.db)
                item._storage_item = self
                item._constructor()

                return item
