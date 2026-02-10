from App.Objects.Test import Test
from Data.Random.GetRandomInt.GetRandomInt import Random
from App.DB.Search import Search
from App import app
from App.DB.Adapters.Search.Condition import Condition
from App.DB.Adapters.Search.Sort import Sort

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
            'sort': [
                Sort(
                    condition = Condition(
                        val1 = 'content',
                        json_fields = ['pubDate']
                    ),
                    descend = False,
                )
            ],
            ''''conditions': [
                Condition(
                    val1 = 'content',
                    json_fields = ['obj', 'saved_via', 'object_name'],
                    operator = '==',
                    val2 = 'Data.RSS.ChannelItem',
                )
            ],'''
            'limit': 9
        })

        return _res
