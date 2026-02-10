from typing import Any, Generator, Self, ClassVar
from abc import ABC, abstractmethod
from App.Objects.Object import Object
from App.Objects.Responses.ObjectsList import ObjectsList
from App.DB.Query.Condition import Condition
from App.DB.Query.Sort import Sort
from App.DB.Query.Values.Value import Value
from App.DB.Representation.ObjectAdapter import ObjectAdapter
from App.Objects.Mixins.BaseModel import BaseModel

class Query(BaseModel, ABC):
    conditions: list[Condition] = []
    sorts: list[Sort] = []
    _limit: int = None
    operators: ClassVar[list] = []
    functions: ClassVar[list] = []

    @abstractmethod
    def _applyCondition(self, condition) -> Self:
        ...

    @abstractmethod
    def _applySort(self, condition) -> Self:
        ...

    @abstractmethod
    def first(self) -> ObjectAdapter:
        ...
    '''
    @abstractmethod
    def page(self, page: int, per_page: int) -> None:
        ...
    '''
    @abstractmethod
    def getAll(self) -> Generator[ObjectAdapter]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...

    def limit(self, limit: int) -> Self:
        self._limit = limit

        return self

    def getLimit(self) -> int:
        return self._limit

    def addCondition(self, condition: Condition) -> Self:
        self.conditions.append(condition)

        return self

    def addSort(self, sort: Sort) -> Self:
        self.sorts.append(sort)

        return self

    def _applyConditions(self) -> Self:
        for item in self.conditions:
            if item.applied == True:
                continue

            self._applyCondition(item)
            item.applied = True

    def _applySorts(self) -> Self:
        for item in self.sorts:
            if item.applied == True:
                continue

            self._applySort(item)
            item.applied = True

    @abstractmethod
    def _applyLimits(self) -> Self:
        ...

    def _apply(self) -> Self:
        self._applyConditions()
        self._applySorts()
        self._applyLimits()

    def toObjectsList(self) -> ObjectsList:
        _item = ObjectsList()

        for item in self.getAll():
            _item.append(item.toPython())

        return _item

    def __init_subclass__(cls):
        cls._init_operators()

    @classmethod
    def _init_operators(cls):
        pass

    def where_object(self, obj: Object) -> Self:
        self.addCondition(Condition(
            val1 = Value(
                column = 'content',
                json_fields = ['obj', 'saved_via', 'object_name'],
            ),
            operator = '==',
            val2 = Value(
                value = obj._getClassNameJoined()
            ),
        ))

        return self
