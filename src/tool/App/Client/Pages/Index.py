from App.Client.Displayment import Displayment
import aiohttp_jinja2

class Index(Displayment):
    for_object = 'App.Client.Client'

    async def render_as_page(self, request, context):
        return aiohttp_jinja2.render_template('base/index.html', request, context)

    async def render_as_error(self, request, context):
        return aiohttp_jinja2.render_template('base/error.html', request, context)
