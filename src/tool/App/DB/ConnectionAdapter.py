from App.Objects.Object import Object
from App.Objects.Protocol import Protocol
from App.Objects.Object import Object
from App.DB.Query.Condition import Condition
from App.DB.Query.Values.Value import Value
from pydantic import Field
from typing import Any, ClassVar
from snowflake import SnowflakeGenerator
from App.Logger.LogPrefix import LogPrefix
from abc import abstractmethod

class ConnectionAdapter(Object, Protocol):
    '''
    Adapter for some object info storage (e.g. db)
    '''

    __abstract__ = True
    _unserializable = ['_storage_item', '_id_gen', 'ObjectAdapter', 'LinkAdapter']

    name: str = Field(default = 'objects')
    auto_commit: bool = Field(default = False)

    objects_table_name: str = Field(default = 'objects')
    links_table_name: str = Field(default = 'links')

    _storage_item: Any = None # Storage item DI
    _id_gen: Any = None
    ObjectAdapter: Any = None
    LinkAdapter: Any = None

    def _set_id_gen(self):
        self._id_gen = SnowflakeGenerator(32)

    # you MUST flush content column later!
    def flush(self, item: Object):
        unit = self.ObjectAdapter()
        unit.toDB(item)

        return unit

    def commit(self):
        pass

    def getQuery(self):
        return self.ObjectAdapter.getQuery()

    def get_rows_count(self):
        query = self.getQuery()

        return query.count()

    def get_links_count(self):
        query = self.LinkAdapter.getQuery()

        return query.count()

    @property
    def append_prefix(self):
        return LogPrefix(
            name = 'storage',
            id = self._storage_item.name
        )

    @abstractmethod
    def destroy(self):
        ...
