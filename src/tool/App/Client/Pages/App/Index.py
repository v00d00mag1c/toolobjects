from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class Index(Displayment):
    for_object = 'App.Client.Client'

    async def render_as_page(self, args = {}):
        self.context.update({
            'is_index': True,
        })

        return self.render_template('index.html')

    async def render_as_error(self, request, context):
        return aiohttp_jinja2.render_template('error.html', request, context)
