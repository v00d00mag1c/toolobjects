from App.Objects.Object import Object
from typing import Self, Literal
from pydantic import Field
from App import app

from App.Objects.Displayments.StringDisplayment import StringDisplayment

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

            _storage_uuid = StorageUUID(storage = vals[0], uuid = vals[1])
        if type(val) == dict:
            _storage_uuid = StorageUUID(storage = val.get('storage'), uuid = val.get('uuid'))

        return _storage_uuid

    @staticmethod
    def validate(string: str) -> bool:
        if isinstance(string, str) == False:
            return False

        return len(string.split('_')) == 2

    @classmethod
    def fromString(cls, string: str) -> Self:
        _ids = string.split('_', 1)
        return cls(
            storage = _ids[0],
            uuid = _ids[1]
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

    class DisplayAsString():
        def implementation(self, i):
            orig = i.get('orig')
            return str(orig.getId())

    @classmethod
    def _displayments(cls):
        return [StringDisplayment(
            value = cls.DisplayAsString
        )]
