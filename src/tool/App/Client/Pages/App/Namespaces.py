from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class ObjectsList(Displayment):
    for_object = 'App.Objects.Index.GetList'

    async def render_as_page(self, request, context):
        items = None

        context.update({
            'namespaces': app.ObjectsList.namespaces,
            'objects': items
        })

        return aiohttp_jinja2.render_template('objects/namespaces.html', request, context)
