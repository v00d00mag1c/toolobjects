from App.Objects.Object import Object
from App.DB.ConnectionAdapter import ConnectionAdapter
from App.Storage.StorageAdapter import StorageAdapter
from App.Storage.StorageUUID import StorageUUID
from pydantic import Field
from typing import Optional
from pathlib import Path
from App import app

class StorageItem(Object):
    '''
    Implements storage with DB and storageunits.

    Notice: path is takes literally and does not creates additional dirs.
    path=f:/dir, name='dir' will use dir f:/dir.

    If 'path' not passed, it will use storage/dbs/{name} dir
    '''

    name: str = Field()
    unused: bool = Field(default = False)
    is_export: bool = Field(default = False)
    is_internal: bool = Field(default = False)

    # input
    storage_type: str = Field(default = 'App.Storage.Adapters.DoubleDividedHashDirs')
    storage: dict = Field(default = {}, repr = False)

    db_type: Optional[str] = Field(default = None)
    db: dict = Field(default = {}, repr = False)
    # /input

    root_uuid: Optional[int | str] = Field(default = None)
    allowed_objects: Optional[list[str]] = Field(default = None)
    forbidden_objects: Optional[list[str]] = Field(default = None)

    # display_name: str = Field(default = None)

    # Internal usage only
    adapter: Optional[ConnectionAdapter] = Field(default = None, exclude = True)
    storage_adapter: Optional[StorageAdapter] = Field(default = None, exclude = True)
    _unserializable = ['storage_adapter', 'adapter', '']

    def get_db_adapter(self) -> ConnectionAdapter:
        assert self.has_db_adapter(), "storage item {0} does not has db connection".format(self.name)

        return self.adapter

    def get_storage_adapter(self) -> StorageAdapter:
        assert self.has_storage_adapter(), "storage item {0} does not has storage".format(self.name)

        return self.storage_adapter

    def _get_name(self) -> str:
        return self.name

    def has_db_adapter(self) -> bool:
        return self.adapter != None

    def has_storage_adapter(self) -> bool:
        return self.storage_adapter != None

    def delete(self):
        self.adapter.delete_everything()
        self.adapter.destroy()
        self.storage_adapter.destroy()

    def destroy(self):
        self.adapter.destroy()
        self.storage_adapter.destroy()

    def path_matches(self, path: Path):
        return path.resolve().relative_to(self.storage_adapter.getStorageDir())

    def get_root_collection(self):
        if self.root_uuid != None:
            try:
                if self.name in self.root_uuid:
                    return StorageUUID.fromString(self.root_uuid).toPython()
                else:
                    return StorageUUID(storage = self.name, uuid = self.root_uuid).toPython()
            except Exception as e:
                self.log_error(e)

    def _init_hook(self):
        if self.storage_type != None:
            self.storage_adapter = self._unwrap(self.storage_type, self.storage)

        if self.db_type != None:
            self.adapter = self._unwrap(self.db_type, self.db)

    def _unwrap(self, name: str, unwrap: dict = {}):
        _obj = app.ObjectsList.getByName(name)

        assert _obj != None, 'adapter with name {0} not found'.format(name)

        _item = _obj.getModule()(**unwrap)
        _item._storage_item = self
        _item._init_hook()

        return _item

    @classmethod
    def asArgument(cls, val: str):
        if type(val) == str:
            return app.Storage.get(val)

        return super().asArgument(val)
