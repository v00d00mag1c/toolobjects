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
        after = query.get('after', 0)
        prev = query.get('prev', 0)
        try:
            after = int(after)
        except:
            after = 0

        try:
            prev = int(prev)
        except:
            prev = 0

        invert = query.get('invert') == 'on'
        operator = '>'
        params = {'q': query.get('q'), 
                  'storage': storage,
                  'show_unlisted': query.get('show_unlisted'),
                  'only_public': query.get('show_unlisted') != 'on',
                  'q.in_description': query.get('q.in_description') == 'on',
                  'limit': per_page,
                  'conditions': [],
                  'offset_conditions': [],
                  'sort': []
        }

        if linked_to not in bad:
            params['linked_to'] = linked_to

        if invert:
            operator = '<'
            params['invert'] = True

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
                #last_uuid = objs[0].getDbId()
                last_uuid = objs[-1].getDbId()
            else:
                last_uuid = objs[-1].getDbId()

        self.context.update({
            'total_count': _val.getTotalCount(),
            'items': objs,
            'last_uuid': last_uuid,
            'per_page': per_page,
            'params': params
        })

        _url2 = dict(query)
        _url2['prev'] = prev
        _url2['after'] = last_uuid

        self.context['after_url'] = self._to_url(_url2)

        if after != None and after != 0:
            _url = dict(query)
            if prev != 0:
                _url['prev'] = last_uuid
                _url['after'] = prev
            else:
                del _url['prev']
                del _url['after']

            self.context['before_url'] = self._to_url(_url)

        return self.render_template('Explorer/search.html')

    def _to_url(self, dicts):
        _val = ''
        for key, val in dicts.items():
            if key == '':
                continue
            _val += '&{0}={1}'.format(key, val)

        return _val
