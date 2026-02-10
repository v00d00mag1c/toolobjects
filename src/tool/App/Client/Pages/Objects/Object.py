from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class Object(Displayment):
    for_object = 'App.Objects.Object'

    async def render_as_page(self, request, context):
        query = request.rel_url.query
        act = query.get('act')
        objs = self.get_objs(query.get('uuids', '').split(','))
        include_nones = query.get('include_none') == '1'

        assert len(objs) > 0, 'objects not found'

        context.update({
            'objects': objs
        })

        match(act):
            case 'view_json':
                _json = list()
                for item in objs:
                    _json.append(item.to_json(exclude_none = include_nones, exclude_defaults = include_nones))

                return self.return_json(_json)
            case 'self_displayment':
                htmls = list()
                for item in objs:
                    _class = app.app.view.displayments.get(item._getNameJoined())
                    if _class == None:
                        htmls.append(
                            (item, aiohttp_jinja2.render_string('Components/message.html', request, {'message': 'not found displayment for ' + item._getNameJoined()}))
                        )
                        continue
                    else:
                        displayment = _class[0]()
                        displayment.request = request
                        htmls.append((item, await displayment.render_as_object(item)))

                context['htmls'] = htmls

                return aiohttp_jinja2.render_template('Objects/displayments.html', request, context)

        return aiohttp_jinja2.render_template('Objects/db_object.html', request, context)
