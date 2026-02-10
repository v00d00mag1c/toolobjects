from abc import abstractmethod
from typing import Any
from App.DB.Query.Condition import Condition
from App.DB.Query.Values.Value import Value
from App.Objects.Misc.UnknownObject import UnknownObject

class AbstractAdapter():
    _adapter: Any = None
    uuid: int = None

    def getStorageItemName(self) -> str:
        return self._adapter._storage_item.name

    @classmethod
    @abstractmethod
    def getQuery(self):
        ...

    @classmethod
    def getById(cls, uuid: int):
        return cls.getQuery().addCondition(Condition(
            val1 = Value(
                column = 'uuid'
            ),
            operator = '==',
            val2 = Value(
                value = uuid
            )
        )).first()

    @classmethod
    def getByIds(cls, uuids: list[int]):
        return cls.getQuery().addCondition(Condition(
            val1 = Value(
                column = 'uuid'
            ),
            operator = 'in',
            val2 = Value(
                value = uuids
            )
        )).getAll()

    @abstractmethod
    def toPython(self):
        ...

    @abstractmethod
    def toDB(self, object):
        ...

    @abstractmethod
    def deleteFromDB(self):
        ...

    def toUnknown(self, reason: str = None):
        unknown = UnknownObject(reason = reason)
        unknown.setDb(self)

        return unknown
