from App.Client.Displayment import Displayment
from App.Objects.Operations.DefaultExecutorWheel import DefaultExecutorWheel
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from Data.Types.JSON import JSON
from App.Objects.Responses.ObjectsList import ObjectsList
from App import app
import aiohttp_jinja2

class Execute(Displayment):
    for_object = 'App.Objects.Operations.DefaultExecutorWheel'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        name = query.get('name')

        _obj = app.ObjectsList.getByName(name)

        assert _obj != None, 'not found object'
        assert _obj.is_inited, 'not inited'

        obj = _obj.getModule()

        self.context.update({
            'post_data': {}
        })

        if self.request.method == 'POST':
            _params = dict(await self.request.post())
            _vals = {
                'i': obj._getNameJoined(),
                'auth': self.auth
            }
            for key, val in _params.items():
                if val == None or val == '':
                    continue

                _vals[key] = val

            stay = _params.get('stay') == '1'

            results = await DefaultExecutorWheel().execute(i = _vals)
            json = results.to_json()

            if stay == False:
                return self.return_json(json)
            else:
                if isinstance(results, ObjectsList):
                    data_htmls = list()
                    for item in results.getItems():
                        _item = self.get_for('App.Objects.Object')(request = self.request, context = self.context)
                        data_htmls.append(await _item.render_as_list_item(item, {'show_id': True}))
                    self.context.update({
                        'data_htmls': data_htmls
                    })
                else:
                    self.context.update({
                        'data': JSON(data = json).dump(4)
                    })

                self.context.update({
                    'obj': obj,
                    'post_data': _params
                })

        self.context.update({
            'obj': obj
        })

        self.context['arguments'] = ArgumentDict()
        if hasattr(obj, 'getArguments'):
            self.context.update({
                'arguments': obj.getArguments(include_usage = True)
            })

        _args = DefaultExecutorWheel.getArguments()
        self.context['arguments'].join(_args, except_those = ['i'])

        return self.render_template('Objects/Execute/nonjs_execute.html')
