from App.Objects.Object import Object
from App.Objects.Protocol import Protocol
from App.Objects.Object import Object
from pydantic import Field
from typing import Any, ClassVar
from snowflake import SnowflakeGenerator
from App.Logger.LogPrefix import LogPrefix

class ConnectionAdapter(Object, Protocol):
    '''
    Adapter for some object info storage (e.g. db)
    '''

    __abstract__ = True
    _unserializable = ['_storage_item', '_id_gen', 'ObjectAdapter', 'LinkAdapter']

    protocol: str = Field(default = 'none')
    delimiter: str = Field(default = ':///')
    name: str = Field(default = 'objects')
    auto_commit: bool = Field(default = True)

    _storage_item: Any = None # Storage item DI
    _id_gen: Any = None
    ObjectAdapter: Any = None
    LinkAdapter: Any = None

    def _set_id_gen(self):
        self._id_gen = SnowflakeGenerator(32)

    def flush(self, item: Object):
        unit = self.ObjectAdapter()
        unit.toDB(item)

        return unit

    def commit(self):
        pass

    def getQuery(self):
        return self.ObjectAdapter.getQuery()

    @property
    def append_prefix(self):
        return LogPrefix(
            name = 'storage',
            id = self._storage_item.name
        )
