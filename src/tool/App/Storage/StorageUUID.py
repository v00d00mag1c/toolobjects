from App.Objects.Object import Object
from typing import Self, Literal
from pydantic import Field
from App import app

class StorageUUID(Object):
    '''
    Object by id and storage name
    '''

    storage: str = Field()
    uuid: int = Field()
    model_name: Literal['object', 'link'] = Field(default = 'object')

    @classmethod
    def asArgument(cls, val: str | dict):
        if isinstance(val, StorageUUID):
            return val

        _storage_uuid = None
        if type(val) == str:
            vals = val.split('_', 1)

            assert len(vals) > 1, 'only id passed, storage name is not'

            _storage_uuid = StorageUUID(storage = vals[0], uuid = int(vals[1]))
        if type(val) == dict:
            _storage_uuid = StorageUUID(storage = val.get('storage'), uuid = val.get('uuid'))

        return _storage_uuid

    @staticmethod
    def validate(string: str) -> bool:
        if isinstance(string, str) == False:
            return False

        _vals = string.split('_')
        try:
            _int = int(_vals[-1])

            return True
        except Exception:
            return False

    @classmethod
    def fromString(cls, string: str) -> Self:
        _ids = string.split('_')
        return cls(
            storage = '_'.join(_ids[:-1]),
            uuid = _ids[-1]
        )

    def getId(self):
        return f"{self.storage}_{self.uuid}"

    def getStorage(self):
        return app.Storage.get(self.storage)

    def getItem(self):
        if self.uuid == None:
            return None

        _storage = self.getStorage()
        assert _storage != None, "storage with name {0} not found".format(self.storage)
        assert self.model_name in ['object', 'link'], 'wrong model'

        if self.model_name == 'object':
            return _storage.get_db_adapter().ObjectAdapter.getById(self.uuid)
        elif self.model_name == 'link':
            return _storage.get_db_adapter().LinkAdapter.getById(self.uuid)

    def toPython(self):
        _item = self.getItem()
        if _item == None:
            return None

        return _item.toPython()

    def _display_as_string(self):
        return str(self.getId())
