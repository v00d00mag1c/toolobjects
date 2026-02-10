from App.Objects.Object import Object
from pydantic import Field
from App import app

class StorageUUID(Object):
    '''
    Object by id and storage name
    '''

    storage: str = Field()
    uuid: int = Field()

    @classmethod
    def asArgument(cls, val: str | dict):
        if isinstance(val, StorageUUID):
            return val

        _storage = None
        if type(val) == str:
            vals = val.split('_', 1)

            _storage = StorageUUID(storage = vals[0], uuid = vals[1])
        if type(val) == dict:
            _storage = StorageUUID(storage = val.get('storage'), uuid = val.get('uuid'))

        return _storage

    def getStorage(self):
        return app.Storage.get(self.storage)

    def getItem(self):
        if self.uuid == None:
            return None

        _storage = self.getStorage()

        assert _storage != None, "storage with name {0} not found".format(self.storage)

        return _storage.adapter.ObjectAdapter.getById(self.uuid)
