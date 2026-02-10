from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class Index(Displayment):
    for_object = 'App.Client.Client'

    async def render_as_page(self, request, context):
        categories = {
            'client.index.content': [],
            'client.app': [],
            'client.index.custom': [],
        }

        for key, val in app.app.view.displayments.items():
            menu = val[0].get_menu()
            if menu != None:
                categories[menu.category_name].append(menu)

        context.update({
            'categories': categories,
            'len': len
        })

        return aiohttp_jinja2.render_template('index.html', request, context)

    async def render_as_error(self, request, context):
        return aiohttp_jinja2.render_template('error.html', request, context)
