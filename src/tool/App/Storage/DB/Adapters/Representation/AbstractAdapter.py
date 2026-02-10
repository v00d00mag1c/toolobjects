from abc import abstractmethod
from typing import Any
from App.Storage.DB.Adapters.Search.Condition import Condition

class AbstractAdapter():
    _adapter: Any = None
    uuid: int = None

    @classmethod
    @abstractmethod
    def getQuery(self):
        ...

    @classmethod
    def getById(cls, uuid: int):
        return cls.getQuery().addCondition(Condition(
            val1 = 'uuid',
            operator = '==',
            val2 = uuid
        )).first()

    @classmethod
    def getByIds(cls, uuids: list[int]):
        return cls.getQuery().addCondition(Condition(
            val1 = 'uuid',
            operator = 'in',
            val2 = uuids
        )).getAll()

    @abstractmethod
    def toPython(self):
        ...

    @abstractmethod
    def toDB(self, object):
        pass
