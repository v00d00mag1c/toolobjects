from App.Objects.Test import Test
from Media.Text.Text import Text
from App.Storage.StorageUnit import StorageUnit
from App.Storage.Item.StorageItem import StorageItem
from Data.Types.JSON import JSON
from App import app
from App.Objects.Responses.ObjectsList import ObjectsList
from App.DB.Query.Values.Value import Value
from App.DB.Query.Condition import Condition
from App.DB.Query.Sort import Sort

class RandomSearch(Test):
    async def _implementation(self, i):
        _storage: StorageItem = app.Storage.get('common')
        _query = _storage.adapter.getQuery()

        self.log('counting')
        _query.addCondition(Condition(
            val1 = Value(
                column = 'uuid',
                func = '%',
                args = [2]
            ),
            operator = '==',
            val2 = Value(
                value = 0
            )
        ))

        self.log('the count of items with even ids is {0}'.format(_query.count()))

        _query2 = _storage.adapter.getQuery()
        _query2.addCondition(Condition(
            val1 = Value(
                column = 'uuid',
                func = '%',
                args = [2]
            ),
            operator = '!=',
            val2 = Value(
                value = 0
            )
        ))

        self.log('the count of items with odd ids is {0}'.format(_query2.count()))
        self.log('now get some random items from common db :)) (with even ids)')

        _query2 = _storage.adapter.getQuery()
        _query2.addCondition(Condition(
            val1 = Value(
                column = 'uuid',
                func = '%',
                args = [2]
            ),
            operator = '!=',
            val2 = Value(
                value = 0
            )
        ))
        _query2.addSort(Sort(
            condition = Condition(
                val1 = Value(
                    column = 'uuid',
                    func = 'random',
                )
            )
        ))
        _ops = _query2.toObjectsList()
        _ops.unsaveable = True

        return _ops
