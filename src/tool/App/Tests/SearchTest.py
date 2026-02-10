from App.Objects.Test import Test
from Data.Random import Random
from App.Storage.DB.Search import Search
from App import app
from App.Storage.DB.Adapters.Search.Condition import Condition

class SearchTest(Test):
    async def implementation(self, i):
        _storage = app.Storage.get('content')
        '''
        _ids = list()
        for i in range(1, 100):
            _item = await Random().execute({'min': i, 'max': i * 100})
            _item.first().flush(_storage)

            if i % 10 == 0:
                _ids.append(_item.first().getDbId())
        '''
        _srch = Search()
        _res = await _srch.execute({
            'storage': _storage,
            'conditions': [
                Condition(
                    val1 = 'content',
                    operator = '==',
                    val2 = 'Data.Number',
                    json_fields = '$.obj.saved_via.object_name'
                )
            ],
            'limit': 9
        })

        return _res
