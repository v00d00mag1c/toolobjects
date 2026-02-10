from App.Client.Displayment import Displayment
from App.Storage.VirtualPath.Navigate import Navigate
import aiohttp_jinja2

class Explorer(Displayment):
    for_object = 'App.Storage.VirtualPath.Navigate'

    async def render_as_page(self, request, context):
        query = request.rel_url.query
        path = query.get('path')

        context.update({
            'path': path,
            'items': await Navigate().execute({
                'path': path,
                'count': 20,
            }),
        })

        return aiohttp_jinja2.render_template('objects/virtual_path.html', request, context)
