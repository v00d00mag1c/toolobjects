from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class Index(Displayment):
    for_object = 'App.Client.Client'

    async def render_as_page(self, request, context):
        context.update({
            'is_index': True,
            'len': len
        })

        return aiohttp_jinja2.render_template('index.html', request, context)

    async def render_as_error(self, request, context):
        return aiohttp_jinja2.render_template('error.html', request, context)
