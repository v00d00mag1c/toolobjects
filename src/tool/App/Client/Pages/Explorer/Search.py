from App.Client.Displayment import Displayment
from App.DB.Search.Search import Search as RealSearch
from App.DB.Query.Condition import Condition
from App.DB.Query.Sort import Sort
from App.DB.Query.Values.Value import Value
from App import app

class Search(Displayment):
    for_object = 'App.DB.Search'

    async def render_as_page(self, args = {}):
        bad = ['', None, 0]
        query = self.request.rel_url.query
        per_page = query.get('per_page', 30)
        storage = query.get('storage')
        act = query.get('act')
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

        ascend = query.get('ascend') == 'on'
        operator = '<'
        params = {'q': query.get('q'), 
                  'storage': storage,
                  'show_unlisted': query.get('show_unlisted'),
                  'only_public': query.get('show_unlisted') != 'on',
                  'q.in_description': query.get('q.in_description') == 'on',
                  'limit': per_page,
                  'display_as': query.get('display_as'),
                  'display_page_as': query.get('display_page_as'),
                  'conditions': [],
                  'offset_conditions': [],
                  'ascend': ascend,
                  'show_tmp': query.get('show_tmp', 'on') == 'on',
                  'storage_root_if_no_collection': True,
                  'sort': []
        }

        if linked_to not in bad:
            params['linked_to'] = linked_to

        if ascend:
            operator = '>'
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
            descend = ascend == False
        ))

        if query.get('only_object', '') != '':
            params['only_object'] = query.get('only_object')

        _e = RealSearch()
        _val = await _e.execute(params)
        objs = list(_val.getItems())
        last_uuid = None
        _items = list()
        _fallback = 'App.Objects.Object'
        display_as = params.get('display_as')
        if display_as in bad:
            display_as = _fallback

        display_page_as = params.get('display_page_as')
        if display_page_as in bad:
            display_page_as = 'App.Objects.Object'

        if len(objs) > 0:
            last_uuid = objs[-1].getDbId()
            #last_uuid = objs[0].getDbId()

        # getting html of the list
        collection_display = self.get_for(display_page_as)
        if collection_display is None:
            #self.throw_message('no displayment for this', 'error')
            collection_display = self.get_for(_fallback)

        collection_display = collection_display(request = self.request, context = self.context)
        search_html = await collection_display.render_as_collection(objs, {
            'display_as': display_as
        }, None)
        self.context.update({
            'total_count': _val.getTotalCount(),
            'search_html': search_html,
            'last_uuid': last_uuid,
            'per_page': per_page,
            'params': params,
            'act': act,
            'show_search': query.get('q') != '',
            'ref': query.get('ref')
        })

        if act == 'linked_to':
            linked_to_type = query.get('linked_to_type')

            match (linked_to_type):
                case 'item':
                    self.context.update({
                        '_item': app.Storage.get(storage)
                    })
                case _:
                    self.context.update({
                        '_object': linked_to
                    })

            self.context.update({
                'act': act
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
