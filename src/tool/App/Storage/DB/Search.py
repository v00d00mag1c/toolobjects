from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Responses.ObjectsList import ObjectsList
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Arguments.Argument import Argument
from Data.Int import Int
from App.Storage.DB.Adapters.Search.Condition import Condition
from App.Storage.StorageItem import StorageItem

class Search(Act):
    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'storage',
                orig = StorageItem,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'conditions',
                default = [],
                is_multiple = True,
                orig = Condition
            ),
            Argument(
                name = 'limit',
                orig = Int,
                default = -1
            ),
            Argument(
                name = 'linked_to',
                is_multiple = True,
                default = [],
                orig = Int
            )
        ])

    async def implementation(self, i) -> ObjectsList:
        _objects = ObjectsList(items = [])
        _storage = i.get('storage')
        _links = i.get('linked_to')

        _query = _storage.adapter.getQuery()
        for condition in i.get('conditions'):
            _query.addCondition(condition)

        if i.get('limit') > 0:
            _query.limit(i.get('limit'))

        for item in _query.getAll():
            _objects.append(item.toPython())

        return _objects
