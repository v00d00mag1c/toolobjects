from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from Data.Int import Int
from App.DB.Adapters.Search.Condition import Condition
from App.DB.Adapters.Search.Sort import Sort
from App.Storage.StorageItem import StorageItem
from App.Storage.StorageUUID import StorageUUID

class Search(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'storage',
                orig = StorageItem,
                assertions = [NotNoneAssertion()]
            ),
            ListArgument(
                name = 'conditions',
                default = [],
                orig = Condition
            ),
            ListArgument(
                name = 'sort',
                default = [],
                orig = Sort
            ),
            Argument(
                name = 'limit',
                orig = Int,
                default = -1
            ),
            ListArgument(
                name = 'linked_to',
                default = None,
                orig = StorageUUID
            ),
            ListArgument(
                name = 'not_linked_to',
                default = None,
                orig = StorageUUID
            ),
            ListArgument(
                name = 'uuids',
                default = None,
                orig = StorageUUID
            ),
        ])

    async def implementation(self, i) -> ObjectsList:
        _objects = ObjectsList(items = [], unsaveable = True)
        _storage = i.get('storage')

        _query = _storage.adapter.getQuery()
        for condition in i.get('conditions'):
            _query.addCondition(condition)

        for key in ['linked_to', 'not_linked_to']:
            _operator = {'linked_to': 'in', 'not_linked_to': 'not_in'}[key]
            _ids = list()
            if len(i.get(key)) == 0:
                continue

            for link in i.get(key):
                _item = link.getItem()
                if _item == None:
                    self.log(f"{link.getId()}: not exists in this db")

                for linked_item in link.getItem().toPython().getLinked():
                    if linked_item.item.hasDb() == False:
                        continue

                    _ids.append(linked_item.item.getDb().uuid)

            _query.addCondition(Condition(
                val1 = 'uuid',
                operator = _operator,
                val2 = _ids
            ))

        if len(i.get('uuids')) > 0:
            _ids_check = list()
            for item_id in i.get('uuids'):
                _ids_check.append(item_id.uuid)

            _query.addCondition(Condition(
                val1 = 'uuid',
                operator = 'in',
                val2 = _ids_check
            ))

        for condition in i.get('sort'):
            _query.addSort(condition)

        if i.get('limit') > 0:
            _query.limit(i.get('limit'))

        for item in _query.getAll():
            try:
                _objects.append(item.toPython())
            except Exception as e:
                self.log_error(e, exception_prefix = f"{item.uuid} not printing: ")

        _objects.total_count = _query.count()
        return _objects
