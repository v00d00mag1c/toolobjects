from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class Execute(Displayment):
    for_object = 'App.Objects.Operations.DefaultExecutorWheel'

    async def render_as_page(self, request, context):
        query = request.rel_url.query
        obj = app.ObjectsList.getByName(query.get('name'))

        assert obj != None, 'object not found'

        context.update({
            'obj': obj
        })

        return aiohttp_jinja2.render_template('Objects/object.html', request, context)
