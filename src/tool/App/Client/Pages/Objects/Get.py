from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class Get(Displayment):
    for_object = 'App.Objects.Index.Get'

    async def render_as_page(self, request, context):
        query = request.rel_url.query
        do_load = query.get('load') == '1'
        obj = app.ObjectsList.getByName(query.get('name'))

        if do_load:
            obj.loadModuleLater()

        assert obj != None, 'object not found'

        context.update({
            'obj': obj,
            'False': False
        })

        return aiohttp_jinja2.render_template('Objects/object.html', request, context)
