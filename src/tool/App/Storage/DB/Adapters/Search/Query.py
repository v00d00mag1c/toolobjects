from typing import Any, Generator, Self, ClassVar
from abc import ABC, abstractmethod
from App.Storage.DB.Adapters.Search.Condition import Condition
from App.Storage.DB.Adapters.Representation.ObjectAdapter import ObjectAdapter

class Query(ABC):
    _query: Any = None
    _model: Any = None
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

    def addCondition(self, condition: Condition) -> Self:
        for key, val in self.operators.items():
            if condition.operator == key:
                self._query = getattr(self, val)(condition)

                return self

        # Fallback (manual func)
        self._query = getattr(self, condition.operator)(condition)
        return self

    @abstractmethod
    def _op_equals(self, condition: Condition):
        ...

    @abstractmethod
    def addSorting(self, condition: Condition) -> Self:
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
    def limit(self, limit: int) -> Self:
        ...
