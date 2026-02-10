from typing import Any, Generator, Self, ClassVar
from abc import ABC, abstractmethod
from App.DB.Adapters.Search.Condition import Condition
from App.DB.Adapters.Search.Sort import Sort
from App.DB.Adapters.Representation.ObjectAdapter import ObjectAdapter

class Query(ABC):
    conditions: list[Condition] = []
    sorts: list[Sort] = []
    limits: int = None
    operators: ClassVar[dict] = {
        '==': '_op_equals',
        '!=': '_op_not_equals',
        'in': '_op_in',
        'not_in': '_op_not_in',
        '<': '_op_lesser',
        '>': '_op_greater',
        '<=': '_op_lesser_or_equal',
        '>=': '_op_greater_or_equal',
        'contains': '_op_contains',
    }

    @abstractmethod
    def _applyCondition(self, condition) -> Self:
        ...

    @abstractmethod
    def _applySort(self, condition) -> Self:
        ...

    @abstractmethod
    def _op_equals(self, condition: Condition):
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
        self.limits = limit

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
        for item in self.conditions:
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
