from App.Client.Displayment import Displayment
from App.DB.Search.Search import Search as RealSearch
from App.DB.Query.Condition import Condition
from App.DB.Query.Sort import Sort
from App.DB.Query.Values.Value import Value

class Search(Displayment):
    for_object = 'App.DB.Search'

    async def render_as_page(self, request, context):
        bad = ['', None]
        query = request.rel_url.query
        per_page = query.get('per_page', 30)
        storage = query.get('storage')
        linked_to = query.get('linked_to')
        after = query.get('after')
        invert = query.get('invert') == 'on'
        operator = '>'
        params = {'q': query.get('q'), 
                  'storage': storage,
                  'only_public': query.get('public') == 'on',
                  'limit': per_page,
                  'conditions': [],
                  'offset_conditions': [],
                  'sort': []
        }

        if linked_to not in bad:
            params['linked_to'] = linked_to

        if invert:
            operator = '<'

        if after not in bad:
            params['offset_conditions'].append(Condition(
                val1 = Value(
                    column = 'uuid'
                ),
                operator = operator,
                val2 = Value(
                    value = int(after)
                )
            ))

        params['sort'].append(Sort(
            condition = Condition(
                val1 = Value(
                    column = 'uuid'
                )
            ),
            descend = invert
        ))

        if query.get('only_object', '') != '':
            params['only_object'] = query.get('only_object')

        _e = RealSearch()
        _val = await _e.execute(params)
        objs = list(_val.getItems())
        last_uuid = None

        if len(objs) > 0:
            if invert:
                last_uuid = objs[0].getDbId()
            else:
                last_uuid = objs[-1].getDbId()

        _url = dict(query)
        _url['after'] = after
        _url2 = dict(query)
        _url2['after'] = last_uuid

        self.context.update({
            'total_count': _val.getTotalCount(),
            'items': objs,
            'last_uuid': last_uuid,
            'after_url': self._to_url(_url2),
            'per_page': per_page
        })

        if after != None:
            self.context['before_url'] = self._to_url(_url)

        return self.render_template('Explorer/search.html')

    def _to_url(self, dicts):
        _val = ''
        for key, val in dicts.items():
            if key == '':
                continue
            _val += '&{0}={1}'.format(key, val)

        return _val
